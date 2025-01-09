import os
import deepl
import sys

def translate_markdown_files(input_directory, output_directory, target_languages, auth_key):
    # Initialize the DeepL translator
    translator = deepl.Translator(auth_key)

    # Loop through each Markdown file in the directory
    for filename in os.listdir(input_directory):
        if filename.endswith('.md'):
            with open(os.path.join(input_directory, filename), 'r', encoding='utf-8') as file:
                content = file.read()

            # Translate the content
            for lang in target_languages:
                translated_text = translator.translate_text(content, target_lang=lang)

                # Save the translated file with a specific pattern
                translated_filename = f"{os.path.splitext(filename)[0]}.{lang}.md"
                with open(os.path.join(output_directory, translated_filename), 'w', encoding='utf-8') as translated_file:
                    translated_file.write(translated_text.text)

if __name__ == "__main__":
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    target_languages = sys.argv[3].split(',')
    auth_key = os.environ['DEEPL_AUTH_KEY']

    translate_markdown_files(input_directory, output_directory, target_languages, auth_key)