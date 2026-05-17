#!/usr/bin/env python3
"""
Translate documentation files using OpenRouter API.
Reads base docs (without language suffix) and translates them to configured target languages.
"""

import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
import yaml

# OpenRouter API
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"

# Provider ranking — earlier providers are tried first when discovering free models.
PROVIDER_PREFERENCE = [
    "deepseek", "qwen", "google", "meta-llama", "openai",
    "mistralai", "nvidia", "z-ai", "nousresearch", "minimax", "arcee-ai",
]

# Skip ID fragments unsuitable for prose translation (code-only, reasoning-trace, vision).
SKIP_PATTERNS = ("coder", "thinking", "reasoning", "vision", "-vl")

# Minimum context window to consider (smaller models truncate docs).
MIN_CONTEXT = 8192

# Minimum parameter count (in billions) for translation-quality output.
MIN_PARAMS_B = 10.0

# Regex pulling a parameter count out of model IDs like "llama-3.3-70b-instruct".
PARAM_SIZE_RE = re.compile(r"-(\d+(?:\.\d+)?)b[-:]")

# Static fallback used only when the catalog API is unreachable.
FALLBACK_MODELS = [
    "deepseek/deepseek-v4-flash:free",
    "qwen/qwen3-next-80b-a3b-instruct:free",
    "meta-llama/llama-3.3-70b-instruct:free",
]

# Config
DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
CONFIG_PATH = Path(__file__).resolve().parent / "translation_config.yaml"
# Parallel workers (env TRANSLATE_PARALLEL_JOBS, default 8)
MAX_WORKERS = int(os.environ.get("TRANSLATE_PARALLEL_JOBS", "8"))

# System prompt for translations (from user spec)
SYSTEM_PROMPT = """You are a senior technical documentation localization engineer.

Your task is to translate GitHub Wiki Markdown documentation into the target language.

STRICT REQUIREMENTS:

1. Preserve ALL Markdown structure exactly:
   - Headings (#, ##, ###)
   - Lists (ordered/unordered)
   - Code fences (```), including language hints
   - Inline code (`code`)
   - Links [text](url)
   - Tables
   - Blockquotes
   - HTML blocks
   - Anchors and fragment links
   - Emoji
   - Horizontal rules

2. NEVER:
   - Modify code examples
   - Translate identifiers, API names, class names, function names
   - Translate code comments unless explicitly requested
   - Change formatting
   - Add explanations
   - Remove sections
   - Add new content
   - Improve the documentation

3. Translate ONLY human-readable prose.

4. Maintain professional technical tone suitable for developer documentation.

5. Preserve terminology consistency across the entire document.

6. If a term is commonly used untranslated in the target language (e.g. API, DSL, Redis, JVM, KSP), keep it in English.

7. Output ONLY the translated Markdown. No explanations.

If input is malformed Markdown, preserve it exactly and translate only readable text."""

# User prompt template
USER_PROMPT_TEMPLATE = """Target language: {language_name}

Translation rules:
- Keep technical terminology consistent
- Keep product and library names unchanged
- Do not translate code blocks
- Do not translate identifiers
- Do not reformat anything

Here is the Markdown content:

---
{content}
---

STRUCTURAL INTEGRITY MODE:

You must produce output that is byte-structurally compatible with the input Markdown.

Rules:
- The number of code blocks must match exactly.
- The number of headings must match exactly.
- All fenced code blocks must remain unchanged.
- All URLs must remain identical.
- All inline code spans must remain identical.
- Do not merge or split paragraphs.
- Do not normalize spacing."""


def load_config() -> list[dict]:
    """Load target languages from config file."""
    with open(CONFIG_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("languages", [])


def discover_free_models() -> list[str]:
    """Fetch OpenRouter catalog and return ranked free models suitable for translation."""
    try:
        resp = requests.get(OPENROUTER_MODELS_URL, timeout=30)
        resp.raise_for_status()
        models = resp.json()["data"]
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Model discovery failed ({e}), using static fallback list.", flush=True)
        return FALLBACK_MODELS

    def is_eligible(m: dict) -> bool:
        model_id = m.get("id", "")
        if not model_id.endswith(":free"):
            return False
        pricing = m.get("pricing") or {}
        if pricing.get("prompt") != "0" or pricing.get("completion") != "0":
            return False
        if (m.get("context_length") or 0) < MIN_CONTEXT:
            return False
        arch = m.get("architecture") or {}
        input_mods = arch.get("input_modalities") or []
        output_mods = arch.get("output_modalities") or []
        if "text" not in input_mods or "text" not in output_mods:
            return False
        slug = model_id.lower()
        if any(p in slug for p in SKIP_PATTERNS):
            return False
        size_match = PARAM_SIZE_RE.search(slug)
        if size_match and float(size_match.group(1)) < MIN_PARAMS_B:
            return False
        return True

    def rank(m: dict) -> tuple[int, int]:
        provider = m["id"].split("/", 1)[0]
        try:
            pref = PROVIDER_PREFERENCE.index(provider)
        except ValueError:
            pref = len(PROVIDER_PREFERENCE)
        # Tie-break by context length (larger first).
        return (pref, -(m.get("context_length") or 0))

    eligible = sorted((m for m in models if is_eligible(m)), key=rank)
    ids = [m["id"] for m in eligible]
    if not ids:
        print("No eligible free models discovered, using static fallback list.", flush=True)
        return FALLBACK_MODELS
    print(f"Discovered {len(ids)} free models. Top 5: {', '.join(ids[:5])}", flush=True)
    return ids


def get_base_docs() -> list[Path]:
    """Find docs without language suffix (e.g. Actions.md, not Actions.zh.md)."""
    base_docs = []
    for f in DOCS_DIR.glob("*.md"):
        if not re.search(r"\.\w{2}\.md$", f.name):
            base_docs.append(f)
    return sorted(base_docs)


def translate_content(
    content: str,
    language_name: str,
    token: str,
    models: list[str],
) -> str:
    """Call OpenRouter API to translate content. Tries models in fallback order."""
    user_prompt = USER_PROMPT_TEMPLATE.format(
        language_name=language_name,
        content=content,
    )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    last_error = None
    for model in models:
        payload = {
            "model": model,
            "messages": messages,
        }
        try:
            resp = requests.post(
                OPENROUTER_URL,
                json=payload,
                headers=headers,
                timeout=120,
            )
            if resp.status_code == 401:
                print("Error: Invalid OR_TOKEN (401). Check your API key.", flush=True)
                sys.exit(1)
            if resp.status_code == 429:
                last_error = resp
                print(f"Rate limited on {model}, trying next model...", flush=True)
                continue
            if resp.status_code >= 500:
                last_error = resp
                print(f"Server error on {model} ({resp.status_code}), trying next model...", flush=True)
                continue
            resp.raise_for_status()
            data = resp.json()
            text = data["choices"][0]["message"]["content"]
            return text.strip()
        except requests.RequestException as e:
            last_error = e
            print(f"Request failed on {model}: {e}, trying next model...", flush=True)
            continue
    raise RuntimeError(f"All models failed. Last error: {last_error}")


def _translate_one(
    doc_name: str,
    stem: str,
    content: str,
    lang: dict,
    token: str,
    models: list[str],
) -> tuple[Path, str]:
    """Translate one (doc, language) pair. Returns (out_path, translated_content)."""
    locale = lang["locale"]
    name = lang["name"]
    out_path = DOCS_DIR / f"{stem}.{locale}.md"
    translated = translate_content(content, name, token, models)
    return (out_path, translated)


def main() -> None:
    token = os.environ.get("OR_TOKEN")
    if not token:
        print("Error: OR_TOKEN environment variable is not set.", flush=True)
        sys.exit(1)

    languages = load_config()
    base_docs = get_base_docs()

    if not base_docs:
        print("No base docs found.", flush=True)
        return

    models = discover_free_models()

    # Build list of (doc_name, stem, content, lang) for parallel execution
    tasks = []
    for doc_path in base_docs:
        with open(doc_path, encoding="utf-8") as f:
            content = f.read()
        for lang in languages:
            tasks.append((doc_path.name, doc_path.stem, content, lang))

    total = len(tasks)
    doc_names = [d.name for d in base_docs]
    lang_names = [f"{l['locale']} ({l['name']})" for l in languages]
    print(f"Base docs: {', '.join(doc_names)}", flush=True)
    print(f"Target languages: {', '.join(lang_names)}", flush=True)
    print(f"Translating {total} docs with {MAX_WORKERS} parallel workers...", flush=True)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(_translate_one, name, stem, content, lang, token, models): (name, lang)
            for name, stem, content, lang in tasks
        }
        done = 0
        for future in as_completed(futures):
            doc_name, lang = futures[future]
            done += 1
            try:
                out_path, translated = future.result()
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(translated)
                print(f"[{done}/{total}] {doc_name} -> {lang['name']} ({lang['locale']})", flush=True)
            except Exception as e:
                print(f"[{done}/{total}] {doc_name} -> {lang['name']}: FAILED - {e}", flush=True)
                raise

    print(f"Done. Translated {total} docs.", flush=True)


if __name__ == "__main__":
    main()
