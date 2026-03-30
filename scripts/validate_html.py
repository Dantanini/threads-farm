"""Validate HTML structure for CI."""
import sys
import re
import os

with open('index.html') as f:
    html = f.read()

errors = []

# Check fetch path exists
match = re.search(r"fetch\(['\"]([^'\"]+)['\"]\)", html)
if not match:
    errors.append('No fetch() call found in index.html')
else:
    path = match.group(1)
    if not os.path.exists(path):
        errors.append(f'fetch path "{path}" does not exist')
    else:
        print(f'✅ fetch path "{path}" exists')

# Check no inline farmer data (should be in JSON)
if re.search(r'const farmers\s*=\s*\[', html):
    errors.append('Farmer data is still inline in HTML — should be in data/farmers.json')

# Check basic HTML structure
for tag in ['<html', '<head', '<body', '</html>', '</body>']:
    if tag not in html:
        errors.append(f'Missing {tag} tag')

# Check essential UI elements exist
for element_id in ['search', 'region-filters', 'card-list']:
    if element_id not in html:
        errors.append(f'Missing element id "{element_id}"')

# Check no hardcoded category array (should be dynamic from data)
if re.search(r"const CATEGORIES\s*=", html):
    errors.append('CATEGORIES is hardcoded — should use getCategories() from data to avoid missing categories')

# Check fallback data loading pattern (stale-while-revalidate)
# Stage 1: farmers.json must be fetched first
fallback_fetch = re.search(r"fetch\(['\"]data/farmers\.json['\"]\)", html)
# Stage 2: Sheet API must be fetched after
sheet_fetch = re.search(r"fetch\(SHEET_API\)", html)
# SHEET_API constant must exist
sheet_const = re.search(r"const SHEET_API\s*=", html)

if not fallback_fetch:
    errors.append('Missing fallback fetch for data/farmers.json')
if not sheet_const:
    errors.append('Missing SHEET_API constant')
if not sheet_fetch:
    errors.append('Missing Sheet API fetch call')
if fallback_fetch and sheet_fetch:
    if fallback_fetch.start() > sheet_fetch.start():
        errors.append('Fallback (farmers.json) must be fetched BEFORE Sheet API (stale-while-revalidate)')
    else:
        print('PASS: Fallback logic correct (farmers.json first, then Sheet API)')

if errors:
    for e in errors:
        print(f'❌ {e}')
    sys.exit(1)
else:
    print('✅ HTML structure valid')
