"""
Verify farmer data against Threads profiles.
Only checks handles that were modified in the current PR.
Outputs warnings for mismatches, does not block merge.
"""
import json
import subprocess
import sys
import urllib.request
import re


def get_changed_handles():
    """Get handles that were added or modified in this PR."""
    try:
        # Get diff of farmers.json against base branch
        result = subprocess.run(
            ['git', 'diff', 'origin/develop', '--', 'data/farmers.json'],
            capture_output=True, text=True
        )
        diff = result.stdout

        # Extract handles from added lines
        handles = set()
        for line in diff.split('\n'):
            if line.startswith('+') and not line.startswith('+++'):
                match = re.search(r'"handle"\s*:\s*"(@[^"]+)"', line)
                if match:
                    handles.add(match.group(1))
        return handles
    except Exception as e:
        print(f'⚠️ Could not parse git diff: {e}')
        return set()


def fetch_threads_page(handle):
    """Fetch Threads profile page content."""
    username = handle.lstrip('@')
    url = f'https://www.threads.com/@{username}'
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return None


def verify_handle(handle, product):
    """Check if product keywords appear on the Threads page."""
    page = fetch_threads_page(handle)
    if not page:
        return 'skip', f'Could not fetch page for {handle}'

    # Extract keywords from product field
    # Remove parenthetical notes like (鹿谷), (夏季6月中)
    clean_product = re.sub(r'[（(][^）)]*[）)]', '', product)
    # Split by common delimiters
    keywords = re.split(r'[、,/\s]+', clean_product)
    keywords = [k.strip() for k in keywords if len(k.strip()) >= 2]

    if not keywords:
        return 'skip', f'{handle}: no keywords to verify'

    found = []
    not_found = []
    for kw in keywords:
        if kw in page:
            found.append(kw)
        else:
            not_found.append(kw)

    if not_found and not found:
        return 'warn', f'{handle}: none of [{", ".join(keywords)}] found on profile'
    elif not_found:
        return 'info', f'{handle}: found [{", ".join(found)}], not found [{", ".join(not_found)}]'
    else:
        return 'ok', f'{handle}: all keywords verified [{", ".join(found)}]'


def main():
    # Load current farmers data
    with open('data/farmers.json') as f:
        farmers = json.load(f)

    # Get changed handles
    changed = get_changed_handles()
    if not changed:
        print('✅ No farmer data changes to verify')
        return

    print(f'Verifying {len(changed)} changed handle(s): {", ".join(changed)}')
    print()

    warnings = []
    for farmer in farmers:
        if farmer['handle'] not in changed:
            continue
        if not farmer.get('product'):
            print(f'⏭️ {farmer["handle"]}: no product listed, skipping')
            continue

        level, msg = verify_handle(farmer['handle'], farmer['product'])
        if level == 'ok':
            print(f'✅ {msg}')
        elif level == 'info':
            print(f'ℹ️ {msg}')
        elif level == 'warn':
            print(f'⚠️ {msg}')
            warnings.append(msg)
        else:
            print(f'⏭️ {msg}')

    print()
    if warnings:
        print(f'⚠️ {len(warnings)} warning(s) — please verify manually:')
        for w in warnings:
            print(f'  - {w}')
        # Exit 0 so it doesn't block merge
    else:
        print('✅ All changed entries verified')


if __name__ == '__main__':
    main()
