import sys
from typing import List

def parse_config(file_name: str) -> dict:
    with open(file_name, 'r') as file:
        content = file.read()
    content = content.strip('{} ')
    templates = {}
    for item in content.split(','):
        key, value = item.split(':')
        key = key.strip()
        value = value.strip().strip('"')
        templates[key] = value
    return templates

def generate_versions(template: str) -> List[str]:
    parts = template.split('.')
    versions = set()

    for i in range(2):
        new_version = []
        for part in parts:
            if part == '*':
                new_version.append(str(i))
            else:
                new_version.append(part)
        versions.add('.'.join(new_version))

    return list(versions)

def filter_versions(versions: List[str], version_to_compare: str) -> List[str]:
    return [version for version in versions if version < version_to_compare]

def main(version: str, config_file: str):
    templates = parse_config(config_file)

    all_versions = []
    for template in templates.values():
        all_versions.extend(generate_versions(template))

    all_versions = sorted(set(all_versions))

    print("generated versions:")
    for v in all_versions:
        print(v)

    older_versions = filter_versions(all_versions, version)
    print("\nold versions:")
    for v in older_versions:
        print(v)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("for using: python 3_generate_versions.py <current_version> <config_file_path>")
        sys.exit(1)

    version_input = sys.argv[1]
    config_filename = sys.argv[2]
    main(version_input, config_filename)