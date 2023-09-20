import re


def extract_current_version(filename):
    with open(filename, "r") as file:
        content = file.read()

    match = re.search(r'__version__\s*=\s*["\'](.*?)["\']', content)
    if match:
        return match.group(1)
    raise ValueError(f"Version not found in {filename}")


def increment_version(version, release_type):
    major, minor, patch = map(int, version.split("."))
    if release_type == "major":
        major += 1
        minor, patch = 0, 0
    elif release_type == "minor":
        minor += 1
        patch = 0
    elif release_type == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid release type: {release_type}")
    return f"{major}.{minor}.{patch}"


def update_file_version(filename, new_version):
    pattern = r'(\s*version\s*=\s*)["\'](.*?)["\']'
    replacement = f'\\1"{new_version}"'

    with open(filename, "r") as file:
        content = file.read()

    new_content = re.sub(pattern, replacement, content)

    with open(filename, "w") as file:
        file.write(new_content)


def main(release_type):
    current_version = extract_current_version("commandgpt/__init__.py")
    new_version = increment_version(current_version, release_type)

    update_file_version("commandgpt/__init__.py", new_version)
    update_file_version("setup.py", new_version)
    update_file_version("pyproject.toml", new_version)

    print(f"Version updated to {new_version} across files.")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ["major", "minor", "patch"]:
        print("Usage: python update_version.py <major/minor/patch>")
        exit(1)

    main(sys.argv[1])
