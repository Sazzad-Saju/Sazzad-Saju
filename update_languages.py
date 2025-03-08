import requests
import re
import os

# GitHub username
GITHUB_USERNAME = "Sazzad-Saju"

# ⚠️ Replace with your new **GitHub Token** (Keep it Private!)
GITHUB_TOKEN = "github token"

# GitHub API URL for repos
GITHUB_API_URL = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"

# Headers for authentication
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# README markers
START_MARKER = "<!--START_LANGUAGES-->"
END_MARKER = "<!--END_LANGUAGES-->"

# Badge mapping for popular languages (Modify as needed)
BADGE_TEMPLATE = "![{lang}](https://img.shields.io/badge/{lang}-{color}?style=for-the-badge&logo={logo}&logoColor=white)"
BADGE_COLORS = {
    "Python": "3776AB",
    "JavaScript": "F7DF1E",
    "Java": "007396",
    "C++": "00599C",
    "C": "A8B9CC",
    "PHP": "777BB4",
    "Ruby": "CC342D",
    "HTML": "E34F26",
    "CSS": "1572B6",
    "Shell": "4EAA25",
    "PowerShell": "5391FE",
    "Vue": "4FC08D",
    "SCSS": "C69",
    "TypeScript": "3178C6",
    "Julia": "9558B2",
    "Less": "1D365D",
}

def get_languages():
    """Fetch all unique languages used across GitHub repositories."""
    response = requests.get(GITHUB_API_URL, headers=HEADERS)

    if response.status_code != 200:
        print(f"❌ GitHub API Error: {response.json()}")
        return []

    repos = response.json()
    language_set = set()

    for repo in repos:
        lang_url = repo.get("languages_url")
        if lang_url:
            lang_response = requests.get(lang_url, headers=HEADERS)
            if lang_response.status_code == 200:
                languages = lang_response.json()
                print(f"🔍 Checking {repo['name']} - Languages: {languages}")  # Debugging
                language_set.update(languages.keys())

    return sorted(language_set)

def generate_language_section(languages):
    """Generate the language section for the README with badges or text."""
    language_list = []
    
    for lang in languages:
        if lang in BADGE_COLORS:
            badge = BADGE_TEMPLATE.format(lang=lang, color=BADGE_COLORS[lang], logo=lang.lower())
            language_list.append(badge)
        else:
            language_list.append(f"- {lang}")  # Fallback to text if no badge available
    
    return "\n".join(language_list)

def update_readme(languages):
    """Update the README.md file with new language list inside markers."""
    readme_file = "README.md"

    if not os.path.exists(readme_file):
        print("❌ ERROR: README.md file not found!")
        return

    with open(readme_file, "r", encoding="utf-8") as file:
        content = file.read()

    lang_section = generate_language_section(languages)
    new_section = f"{START_MARKER}\n{lang_section}\n{END_MARKER}"

    # Replace only the section inside markers
    new_content = re.sub(
        f"{START_MARKER}.*?{END_MARKER}", 
        new_section, 
        content, 
        flags=re.DOTALL
    )

    with open(readme_file, "w", encoding="utf-8") as file:
        file.write(new_content)

    print("✅ README.md updated successfully!")

if __name__ == "__main__":
    languages = get_languages()
    if languages:
        update_readme(languages)
        print("🎯 Updated language list:", languages)
    else:
        print("⚠️ No languages found!")
