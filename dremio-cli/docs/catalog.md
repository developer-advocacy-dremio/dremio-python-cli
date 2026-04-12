# Catalog Operations

This guide covers catalog operations including listing, retrieving, and navigating the Dremio catalog.

## Commands

### List Catalog

List all items in the catalog.

```bash
alt-dremio-cli catalog list [OPTIONS]
```

**Options:**
- `--include TEXT` - Include additional fields (e.g., `permissions`, `datasetCount`)

**Examples:**

```bash
# List all catalog items
alt-dremio-cli catalog list

# List with permissions
alt-dremio-cli catalog list --include permissions

# List with dataset count
alt-dremio-cli catalog list --include datasetCount

# JSON output
alt-dremio-cli --output json catalog list

# Use specific profile
alt-dremio-cli --profile software catalog list
```

### Get Catalog Item by ID

Retrieve a specific catalog item by its ID.

```bash
alt-dremio-cli catalog get <ITEM_ID> [OPTIONS]
```

**Arguments:**
- `ITEM_ID` - The catalog item ID (UUID)

**Options:**
- `--include TEXT` - Include additional fields

**Examples:**

```bash
# Get catalog item
alt-dremio-cli catalog get 4cc92138-34e8-4c84-ad03-abfb23b6d5f3

# Get with SQL definition
alt-dremio-cli catalog get 4cc92138-34e8-4c84-ad03-abfb23b6d5f3 --include sql

# Get with permissions
alt-dremio-cli catalog get 4cc92138-34e8-4c84-ad03-abfb23b6d5f3 --include permissions

# YAML output
alt-dremio-cli --output yaml catalog get 4cc92138-34e8-4c84-ad03-abfb23b6d5f3
```

### Get Catalog Item by Path

Retrieve a catalog item by its path.

```bash
alt-dremio-cli catalog get-by-path <PATH> [OPTIONS]
```

**Arguments:**
- `PATH` - The catalog path (dot-separated or slash-separated)

**Options:**
- `--include TEXT` - Include additional fields

**Examples:**

```bash
# Get by dot-separated path
alt-dremio-cli catalog get-by-path "MySpace.MyTable"

# Get by slash-separated path
alt-dremio-cli catalog get-by-path "MySpace/MyFolder/MyView"

# Cloud: source.namespace.object
alt-dremio-cli catalog get-by-path "evangelism-2026.testing.my_table"

# Software: space.object or catalog.namespace.object
alt-dremio-cli catalog get-by-path "Analytics.sales_data"
alt-dremio-cli catalog get-by-path "dremio-catalog.alexmerced.testing"

# With additional fields
alt-dremio-cli catalog get-by-path "MySpace.MyView" --include sql
```

## Scenarios

### Exploring the Catalog

```bash
# 1. List all top-level items
alt-dremio-cli catalog list

# 2. Find a specific space or source
alt-dremio-cli catalog list | grep "MySpace"

# 3. Get details about a space
alt-dremio-cli catalog get-by-path "MySpace"

# 4. Explore nested items
alt-dremio-cli catalog get-by-path "MySpace/Reports"
```

### Finding Datasets

```bash
# List all items with dataset counts
alt-dremio-cli catalog list --include datasetCount

# Get specific dataset
alt-dremio-cli catalog get-by-path "Sales.customers"

# Check dataset permissions
alt-dremio-cli catalog get-by-path "Sales.customers" --include permissions
```

### Working with Views

```bash
# Get view definition
alt-dremio-cli catalog get-by-path "Analytics.monthly_summary" --include sql

# Get view metadata
alt-dremio-cli --output json catalog get-by-path "Analytics.monthly_summary"
```

### Cross-Environment Comparison

```bash
# Compare catalog between environments
alt-dremio-cli --profile dev catalog list > dev_catalog.json
alt-dremio-cli --profile prod catalog list > prod_catalog.json
diff dev_catalog.json prod_catalog.json
```

## Output Formats

### Table (Default)

```bash
alt-dremio-cli catalog list
```

Output:
```
┌────────────────────┬──────┬─────────────┬──────────┐
│ ID                 │ Path │ Type        │ Created  │
├────────────────────┼──────┼─────────────┼──────────┤
│ abc-123-def-456    │ ...  │ SPACE       │ 2024-... │
│ xyz-789-ghi-012    │ ...  │ SOURCE      │ 2024-... │
└────────────────────┴──────┴─────────────┴──────────┘
```

### JSON

```bash
alt-dremio-cli --output json catalog list
```

Output:
```json
{
  "data": [
    {
      "id": "abc-123-def-456",
      "path": ["MySpace"],
      "type": "CONTAINER",
      "containerType": "SPACE",
      "createdAt": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### YAML

```bash
alt-dremio-cli --output yaml catalog list
```

Output:
```yaml
data:
  - id: abc-123-def-456
    path:
      - MySpace
    type: CONTAINER
    containerType: SPACE
    createdAt: '2024-01-01T00:00:00Z'
```

## Path Formats

### Cloud

```
source.namespace.object
```

Examples:
- `evangelism-2026.testing.my_table`
- `my-s3-source.data.customers`

### Software

```
space.object
catalog.namespace.object
```

Examples:
- `Analytics.sales_data`
- `dremio-catalog.alexmerced.testing`
- `@user@company.com.my_view`

## Common Use Cases

### 1. Inventory Management

```bash
# Export full catalog inventory
alt-dremio-cli --output json catalog list > catalog_inventory.json

# Count items by type
alt-dremio-cli --output json catalog list | jq '[.data[] | .containerType] | group_by(.) | map({type: .[0], count: length})'
```

### 2. Finding Specific Items

```bash
# Find all spaces
alt-dremio-cli --output json catalog list | jq '.data[] | select(.containerType == "SPACE")'

# Find all sources
alt-dremio-cli --output json catalog list | jq '.data[] | select(.containerType == "SOURCE")'

# Find all views
alt-dremio-cli --output json catalog list | jq '.data[] | select(.type == "VIRTUAL_DATASET")'
```

### 3. Validation

```bash
# Verify item exists
alt-dremio-cli catalog get-by-path "MySpace.MyTable" && echo "Exists" || echo "Not found"

# Check if path is accessible
alt-dremio-cli catalog get-by-path "Sales.customers" --include permissions
```

### 4. Migration Planning

```bash
# List all items in source environment
alt-dremio-cli --profile source catalog list --include datasetCount > source_catalog.json

# List all items in target environment
alt-dremio-cli --profile target catalog list --include datasetCount > target_catalog.json

# Compare and plan migration
diff source_catalog.json target_catalog.json
```

## Tips

1. **Use JSON output for scripting**:
   ```bash
   alt-dremio-cli --output json catalog list | jq '.data[] | .path'
   ```

2. **Filter results with grep**:
   ```bash
   alt-dremio-cli catalog list | grep "Analytics"
   ```

3. **Save catalog snapshots**:
   ```bash
   alt-dremio-cli --output json catalog list > catalog_$(date +%Y%m%d).json
   ```

4. **Check permissions before operations**:
   ```bash
   alt-dremio-cli catalog get-by-path "MySpace.MyTable" --include permissions
   ```

## Error Handling

### Item Not Found

```bash
$ alt-dremio-cli catalog get-by-path "NonExistent.Table"
Error: Resource not found
```

**Solution**: Verify the path exists:
```bash
alt-dremio-cli catalog list | grep "NonExistent"
```

### Permission Denied

```bash
$ alt-dremio-cli catalog get abc-123
Error: Access forbidden
```

**Solution**: Check your profile has appropriate permissions.

### Invalid Path Format

```bash
$ alt-dremio-cli catalog get-by-path "Invalid Path With Spaces"
Error: Invalid path format
```

**Solution**: Use proper path separators:
```bash
alt-dremio-cli catalog get-by-path "Space.Folder.Object"
```
