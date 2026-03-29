"""Validate farmers.json against schema.json"""
import json
import sys
import re


def main():
    with open('data/schema.json') as f:
        schema = json.load(f)

    with open('data/farmers.json') as f:
        data = json.load(f)

    # Get allowed values from schema
    region_enum = schema['items']['properties']['region']['enum']
    category_enum = schema['items']['properties']['category']['enum']
    required_fields = schema['items']['required']
    all_fields = set(schema['items']['properties'].keys())

    errors = []

    for i, farmer in enumerate(data):
        # Check required fields
        for field in required_fields:
            if field not in farmer or not farmer[field]:
                # region can be empty string
                if field == 'region':
                    continue
                errors.append(f'Row {i} ({farmer.get("handle","?")}): missing required field "{field}"')

        # Check handle format
        if not farmer.get('handle', '').startswith('@'):
            errors.append(f'Row {i}: handle must start with @ (got "{farmer.get("handle","")}")')

        # Check region enum
        if 'region' in farmer and farmer['region'] not in region_enum:
            errors.append(f'Row {i} ({farmer["handle"]}): invalid region "{farmer["region"]}"')

        # Check category enum if present
        if 'category' in farmer and farmer['category'] not in category_enum:
            errors.append(f'Row {i} ({farmer["handle"]}): invalid category "{farmer["category"]}"')

        # Check verified format if present
        if farmer.get('verified') and not re.match(r'^\d{4}-\d{2}-\d{2}$', farmer['verified']):
            errors.append(f'Row {i} ({farmer["handle"]}): invalid verified date format "{farmer["verified"]}"')

        # Check for unknown fields
        unknown = set(farmer.keys()) - all_fields
        if unknown:
            errors.append(f'Row {i} ({farmer["handle"]}): unknown fields {unknown}')

    if errors:
        print(f'❌ {len(errors)} schema error(s):')
        for e in errors:
            print(f'  - {e}')
        sys.exit(1)
    else:
        print(f'✅ Schema valid — {len(data)} entries, all fields conform')


if __name__ == '__main__':
    main()
