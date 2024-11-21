#!/usr/bin/env python3

import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List


def find_crackme_directories() -> List[Path]:
    current_dir = Path(__file__).parent
    pattern = re.compile(r'^\d{2}-[a-zA-Z0-9_-]+$')

    dirs = []
    for item in current_dir.iterdir():
        if item.is_dir() and pattern.match(item.name):
            readme = item / "README.md"
            if readme.exists():
                dirs.append(item)

    return sorted(dirs)


def extract_metadata(readme_path: Path) -> Dict[str, str]:
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    metadata = {
        'name': '',
        'difficulty': 'Unknown',
        'protection': 'Unknown',
        'status': 'UNKNOWN',
        'number': ''
    }

    # Extract from title
    title_match = re.search(r'#\s*Crackme Solution:\s*(.+)', content)
    if title_match:
        metadata['name'] = title_match.group(1).strip()

    # Extract from metadata table
    difficulty_match = re.search(r'\*\*Difficulty:\*\*\s*(.+)', content)
    if difficulty_match:
        metadata['difficulty'] = difficulty_match.group(1).strip()

    # Extract protection from metadata table
    protection_match = re.search(r'\|\s*\*\*Protection\*\*\s*\|\s*(.+?)\s*\|', content)
    if protection_match:
        metadata['protection'] = protection_match.group(1).strip()

    # Extract status
    status_match = re.search(r'\*\*Status:\*\*\s*(.+)', content)
    if status_match:
        status = status_match.group(1).strip().upper()
        if 'SOLVED' in status or 'CRACKED' in status:
            metadata['status'] = 'SOLVED'
        elif 'WIP' in status or 'PROGRESS' in status:
            metadata['status'] = 'WIP'
        else:
            metadata['status'] = 'UNKNOWN'

    # Extract number from directory name
    dir_name = readme_path.parent.name
    num_match = re.match(r'^(\d{2})-', dir_name)
    if num_match:
        metadata['number'] = num_match.group(1)

    return metadata


def generate_statistics(crackmes: List[Dict[str, str]]) -> Dict[str, any]:
    stats = {
        'total_solved': 0,
        'easy': 0,
        'medium': 0,
        'hard': 0,
        'techniques': set()
    }

    for crackme in crackmes:
        if crackme['status'] == 'SOLVED':
            stats['total_solved'] += 1

            difficulty = crackme['difficulty'].lower()
            if 'easy' in difficulty:
                stats['easy'] += 1
            elif 'medium' in difficulty:
                stats['medium'] += 1
            elif 'hard' in difficulty:
                stats['hard'] += 1

    return stats


def generate_table_row(metadata: Dict[str, str]) -> str:
    num = metadata['number']
    name = metadata['name']
    difficulty = metadata['difficulty']
    protection = metadata['protection']
    status = metadata['status']
    link = f"[Writeup](./{metadata['number']}-{metadata['name'].lower().replace(' ', '-')}/README.md)"

    # Get actual directory name for link
    current_dir = Path(__file__).parent
    for item in current_dir.iterdir():
        if item.is_dir() and item.name.startswith(f"{num}-"):
            link = f"[Writeup](./{item.name}/README.md)"
            break

    return f"| {num} | {name} | {difficulty} | {protection} | {status} | {link} |"


def update_readme(crackmes: List[Dict[str, str]], stats: Dict[str, any]):
    readme_path = Path(__file__).parent / "README.md"

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update table
    table_header = "| # | Name | Difficulty | Protection | Status | Writeup |\n|---|------|------------|------------|--------|---------|"
    table_rows = [generate_table_row(cm) for cm in crackmes]
    new_table = table_header + "\n" + "\n".join(table_rows)

    content = re.sub(
        r'\|\s*#\s*\|.*?\|\s*Writeup\s*\|.*?(?=\n\n|\n##)',
        new_table,
        content,
        flags=re.DOTALL
    )

    # Update statistics
    stats_pattern = r'(## Statistics\s*\n\s*\n- Total Solved: )\d+'
    content = re.sub(stats_pattern, rf'\g<1>{stats["total_solved"]}', content)

    content = re.sub(r'(- Easy: )\d+', rf'\g<1>{stats["easy"]}', content)
    content = re.sub(r'(- Medium: )\d+', rf'\g<1>{stats["medium"]}', content)
    content = re.sub(r'(- Hard: )\d+', rf'\g<1>{stats["hard"]}', content)

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"README.md updated")
    print(f"Total Solved: {stats['total_solved']}")
    print(f"Easy: {stats['easy']}, Medium: {stats['medium']}, Hard: {stats['hard']}")

def fix_obsidian_image_links():
    base_dir = Path(__file__).parent
    
    # Find all README.md files in all subdirectories
    readme_files = list(base_dir.glob("**/README.md"))

    if not readme_files:
        return

    files_modified = 0

    for readme_path in readme_files:
        content = readme_path.read_text(encoding='utf-8')
        pattern = r'!\[\[([^\]]+\.(?:png|jpe?g|webp|gif|svg))(?:\|([^\]]+))?\]\]'

        def replace_match(match):
            filename = match.group(1).strip()
            alt_text = match.group(2)
            encoded_filename = filename.replace(" ", "%20")
            raw_url = f"https://raw.githubusercontent.com/fdsmlx/crackme-solutions/main/resources/{encoded_filename}"

            if alt_text:
                alt = alt_text
            else:
                alt = Path(filename).stem.replace("%20", " ").replace("_", " ")

            return f"![{alt}]({raw_url})"

        new_content = re.sub(pattern, replace_match, content, flags=re.IGNORECASE)

        if new_content != content:
            readme_path.write_text(new_content, encoding='utf-8')
            files_modified += 1

    if files_modified > 0:
        print(f"Fixed {files_modified} image links")

def main():
    print("Scanning directories...")

    dirs = find_crackme_directories()
    print(f"Found {len(dirs)} crackme(s)")

    crackmes = []
    for dir_path in dirs:
        readme = dir_path / "README.md"
        metadata = extract_metadata(readme)
        crackmes.append(metadata)

    stats = generate_statistics(crackmes)
    update_readme(crackmes, stats)
    fix_obsidian_image_links()

    print("Done")


if __name__ == "__main__":
    main()
