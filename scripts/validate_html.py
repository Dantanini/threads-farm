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

if errors:
    for e in errors:
        print(f'❌ {e}')
    sys.exit(1)
else:
    print('✅ HTML structure valid')
