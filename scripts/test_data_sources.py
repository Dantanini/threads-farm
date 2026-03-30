"""
Test: verify data sources (farmers.json + Google Sheet API)
Ensures fallback data is valid and API returns compatible format.

Run: python scripts/test_data_sources.py
"""
import json
import sys
import urllib.request

SHEET_API = 'https://script.google.com/macros/s/AKfycbyh3jm4c_hkrIzIXnur7BEp5oAUzjm7kA17Yh00Qavbxnvf5UD77YgILJSct4Xae5U/exec'
REQUIRED_FIELDS = ['handle', 'product', 'region']
ALL_FIELDS = ['handle', 'name', 'product', 'region', 'price', 'buy', 'cert', 'min', 'ship', 'url', 'category', 'verified', 'created_at', 'updated_at']
VALID_REGIONS = ['', '宜蘭', '基隆', '台北', '新北', '桃園', '新竹', '苗栗', '台中', '彰化', '南投', '雲林', '嘉義', '台南', '高雄', '屏東', '台東', '花蓮', '澎湖', '金門', '馬祖']
VALID_CATEGORIES = ['', '蔬菜', '水果', '米糧', '蛋肉', '蜂蜜', '調味', '加工品', '海鮮']

errors = []
warnings = []


def validate_entry(entry, source, index):
    """Validate a single farmer entry."""
    handle = entry.get('handle', '')

    # Required fields
    if not handle:
        errors.append(f'[{source}] Row {index}: missing handle')
        return
    if not handle.startswith('@'):
        errors.append(f'[{source}] {handle}: handle must start with @')

    # Region enum
    region = entry.get('region', '')
    if region not in VALID_REGIONS:
        errors.append(f'[{source}] {handle}: invalid region "{region}"')

    # Category enum
    category = entry.get('category', '')
    if category and category not in VALID_CATEGORIES:
        errors.append(f'[{source}] {handle}: invalid category "{category}"')


def validate_dataset(data, source):
    """Validate a full dataset."""
    if not isinstance(data, list):
        errors.append(f'[{source}] Data is not an array')
        return

    if len(data) == 0:
        errors.append(f'[{source}] Data is empty')
        return

    print(f'[{source}] {len(data)} entries loaded')

    # Check for duplicates
    handles = [d.get('handle', '') for d in data]
    dupes = set([h for h in handles if handles.count(h) > 1])
    if dupes:
        warnings.append(f'[{source}] Duplicate handles: {dupes}')

    # Validate each entry
    for i, entry in enumerate(data):
        validate_entry(entry, source, i)


def test_fallback():
    """Test 1: farmers.json is valid and loadable."""
    print('\n=== Test: farmers.json (fallback) ===')
    try:
        with open('data/farmers.json', encoding='utf-8') as f:
            data = json.load(f)
        validate_dataset(data, 'farmers.json')
        return data
    except json.JSONDecodeError as e:
        errors.append(f'[farmers.json] Invalid JSON: {e}')
        return None
    except FileNotFoundError:
        errors.append('[farmers.json] File not found')
        return None


def test_sheet_api():
    """Test 2: Google Sheet API returns valid JSON with compatible format."""
    print('\n=== Test: Google Sheet API ===')
    try:
        req = urllib.request.Request(SHEET_API, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        validate_dataset(data, 'Sheet API')
        return data
    except Exception as e:
        warnings.append(f'[Sheet API] Could not fetch: {e}')
        return None


def test_compatibility(fallback, sheet):
    """Test 3: Sheet data is compatible with fallback format."""
    print('\n=== Test: Compatibility ===')
    if not fallback or not sheet:
        warnings.append('[Compatibility] Skipped — one source unavailable')
        return

    # Check field consistency
    if sheet:
        sheet_fields = set()
        for entry in sheet:
            sheet_fields.update(entry.keys())
        extra = sheet_fields - set(ALL_FIELDS)
        if extra:
            warnings.append(f'[Compatibility] Sheet has extra fields: {extra}')

    # Check count difference
    diff = abs(len(sheet) - len(fallback))
    if diff > 20:
        warnings.append(f'[Compatibility] Large count difference: Sheet={len(sheet)}, fallback={len(fallback)} (diff={diff})')
    else:
        print(f'[Compatibility] Count: Sheet={len(sheet)}, fallback={len(fallback)} (diff={diff})')

    print('[Compatibility] OK')


def main():
    fallback = test_fallback()
    sheet = test_sheet_api()
    test_compatibility(fallback, sheet)

    print('\n=== Summary ===')
    if errors:
        print(f'FAIL: {len(errors)} error(s):')
        for e in errors:
            print(f'  - {e}')
    if warnings:
        print(f'WARN: {len(warnings)} warning(s):')
        for w in warnings:
            print(f'  - {w}')
    if not errors and not warnings:
        print('PASS: All tests passed')

    if errors:
        sys.exit(1)


if __name__ == '__main__':
    main()
