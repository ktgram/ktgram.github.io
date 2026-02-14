#!/usr/bin/env python3
"""
Translate documentation files using OpenRouter API.
Reads base docs (without language suffix) and translates them to configured target languages.
"""

import os
import re
import sys
from pathlib import Path

import requests
import yaml

# OpenRouter API
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Model fallback chain (primary first, then fallbacks)
MODELS = [
    "arcee-ai/trinity-large-preview:free",
    "deepseek/deepseek-r1-0528:free",
    "stepfun/step-3.5-flash:free",
]

# Config
DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
CONFIG_PATH = Path(__file__).resolve().parent / "translation_config.yaml"

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
    for model in MODELS:
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
                print(f"Error: Invalid OR_TOKEN (401). Check your API key.")
                sys.exit(1)
            if resp.status_code == 429:
                last_error = resp
                print(f"Rate limited on {model}, trying next model...")
                continue
            if resp.status_code >= 500:
                last_error = resp
                print(f"Server error on {model} ({resp.status_code}), trying next model...")
                continue
            resp.raise_for_status()
            data = resp.json()
            text = data["choices"][0]["message"]["content"]
            return text.strip()
        except requests.RequestException as e:
            last_error = e
            print(f"Request failed on {model}: {e}, trying next model...")
            continue
    raise RuntimeError(f"All models failed. Last error: {last_error}")


def main() -> None:
    token = os.environ.get("OR_TOKEN")
    if not token:
        print("Error: OR_TOKEN environment variable is not set.")
        sys.exit(1)

    languages = load_config()
    base_docs = get_base_docs()

    if not base_docs:
        print("No base docs found.")
        return

    total = len(base_docs) * len(languages)
    done = 0
    for doc_path in base_docs:
        stem = doc_path.stem
        with open(doc_path, encoding="utf-8") as f:
            content = f.read()

        for lang in languages:
            locale = lang["locale"]
            name = lang["name"]
            out_path = DOCS_DIR / f"{stem}.{locale}.md"
            done += 1
            print(f"[{done}/{total}] Translating {doc_path.name} -> {name} ({locale})...")

            try:
                translated = translate_content(content, name, token)
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(translated)
            except Exception as e:
                print(f"  Failed: {e}")
                raise

    print(f"Done. Translated {total} docs.")


if __name__ == "__main__":
    main()
