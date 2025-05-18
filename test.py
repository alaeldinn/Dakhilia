import requests
from bs4 import BeautifulSoup

# Fetch all versions of a package from pub.dev
def fetch_package_versions(package_name):
    url = f"https://pub.dev/packages/{package_name}/versions"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        version_links = soup.select('a[href^="/packages/{package_name}/versions/"]')
        versions = [link.text.strip() for link in version_links]
        return versions
    else:
        raise Exception(f"Failed to fetch package versions. Status code: {response.status_code}")

# Check if a class exists in a specific version of the package
def check_class_in_version(package_name, version, class_name):
    url = f"https://pub.dev/packages/{package_name}/versions/{version}"
    response = requests.get(url)
    if response.status_code == 200:
        # Use regex for more accurate matching
        import re
        pattern = rf"class\s+{class_name}\s*{{|{class_name}\("
        return bool(re.search(pattern, response.text))
    else:
        raise Exception(f"Failed to fetch package details for version {version}. Status code: {response.status_code}")

def main():
    package_name = "flutter_quill"
    class_name = "quill"

    try:
        print(f"Fetching versions of {package_name}...")
        versions = fetch_package_versions(package_name)
        print(f"Found {len(versions)} versions of {package_name}.")

        print(f"Checking for the existence of {class_name}...")
        for version in versions:
            exists = check_class_in_version(package_name, version, class_name)
            if exists:
                print(f"Class {class_name} found in version: {version}")
            else:
                print(f"Class {class_name} NOT found in version: {version}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()