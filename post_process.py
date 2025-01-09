import os
import re

# Define the path to your documentation folder
docs_path = 'docs'  # Change this to your actual docs folder path

def update_headings(content):
    # Change all H1 headings to H2
    content = re.sub(r'^(# )(.+)', r'## \2', content, flags=re.MULTILINE)

    # Increment the depth of all other headings
    def increment_headings(match):
        level = match.group(1).count('#')  # Count the number of '#' characters
        new_level = level + 1  # Increment the level
        return '#' * new_level + ' ' + match.group(2)  # Return the new heading

    content = re.sub(r'^(#+) (.+)', increment_headings, content, flags=re.MULTILINE)

    return content

# Iterate through all files in the docs directory
for root, dirs, files in os.walk(docs_path):
    for file in files:
        file_path = os.path.join(root, file)

        # Check if the file is index.md
        if file == 'index.md':
            title = 'Home'  # Set title to Home for index.md
        elif file.endswith('.md'):
            title = os.path.splitext(file)[0].replace('_', ' ').replace('-', ' ').replace('\
', '<br/>').title()  # Convert filename to title
        else:
            continue  # Skip non-md files

        # Read the current content of the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if the front matter already exists
        if content.startswith('---'):
            # If front matter exists, update it
            end_of_front_matter = content.find('---', 3) + 3
            front_matter = content[:end_of_front_matter]
            new_front_matter = front_matter.replace(
                front_matter.splitlines()[1], f'title: {title}'
            )
            new_content = new_front_matter + content[end_of_front_matter:]
        else:
            # If no front matter exists, add it
            new_content = f'---\ntitle: {title}\n---\n\n' + content

        # Update headings in the content
        new_content = update_headings(new_content)

        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

print("Titles generated based on file names and headings updated.")