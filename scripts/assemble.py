import argparse
import os
import json

def assemble_resume(template_path, data_json, output_path):
    """
    Assembles a resume by replacing placeholders in an HTML template with data from a JSON file.
    Replaces brittle sed-based logic to handle special characters safely (PM-1he).
    """
    if not os.path.exists(template_path):
        print(f"Error: Template not found at {template_path}")
        return

    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()

    with open(data_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Dictionary should contain keys like "FULL_NAME", "EMAIL", "PROFESSIONAL_SUMMARY", etc.
    # The template placeholders are expected to be in the format {{KEY}}
    # Replace placeholders with data
    for key, value in data.items():
        placeholder = f"{{{{{key}}}}}"
        html = html.replace(placeholder, str(value))

    # PM-25d: Assembly Safety Gate (Regex check for leftover placeholders post-replacement)
    import re
    leftovers = re.findall(r"\{\{.*?\}\}", html)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    if leftovers:
        raise ValueError(f"PlaceholderLeakageError: {len(leftovers)} tags remained.")

    print(f"✅ Resume assembled successfully: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assemble HTML resume from template and JSON data.")
    parser.add_argument("--template", required=True, help="Path to Base_Template.html")
    parser.add_argument("--data", required=True, help="Path to the JSON data file for replacements")
    parser.add_argument("--output", required=True, help="Path to save the generated resume.html")

    args = parser.parse_args()
    assemble_resume(args.template, args.data, args.output)
