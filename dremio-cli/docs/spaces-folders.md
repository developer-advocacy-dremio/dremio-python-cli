# Space and Folder Management

This guide covers space and folder management operations for organizing your Dremio catalog.

## Overview

**Spaces** and **Folders** are containers for organizing your data:

- **Cloud**: Spaces are top-level folders in the project catalog
- **Software**: Spaces are traditional SPACE containers, folders are FOLDER containers

The CLI handles these differences transparently.

## Space Commands

### Create Space

Create a new space.

```bash
alt-dremio-cli space create --name <NAME> [OPTIONS]
```

**Options:**
- `--name TEXT` - Space name (required)
- `--description TEXT` - Space description

**Examples:**

```bash
# Create simple space
alt-dremio-cli space create --name "Analytics"

# Create with description
alt-dremio-cli space create --name "Sales" --description "Sales data and reports"

# Cloud: Creates top-level folder
alt-dremio-cli --profile cloud space create --name "Marketing"

# Software: Creates traditional SPACE
alt-dremio-cli --profile software space create --name "DataScience"
```

### List Spaces

List all spaces.

```bash
alt-dremio-cli space list
```

**Examples:**

```bash
# List all spaces
alt-dremio-cli space list

# JSON output
alt-dremio-cli --output json space list

# YAML output
alt-dremio-cli --output yaml space list
```

### Get Space

Retrieve space details by ID.

```bash
alt-dremio-cli space get <SPACE_ID>
```

**Arguments:**
- `SPACE_ID` - The space ID (UUID)

**Examples:**

```bash
# Get space details
alt-dremio-cli space get 66c76a3e-0335-463b-8622-1720f8546537

# Get in JSON format
alt-dremio-cli --output json space get 66c76a3e-0335-463b-8622-1720f8546537
```

### Delete Space

Delete a space.

```bash
alt-dremio-cli space delete <SPACE_ID> [OPTIONS]
```

**Arguments:**
- `SPACE_ID` - The space ID (UUID)

**Options:**
- `--tag TEXT` - Version tag for optimistic concurrency control

**Examples:**

```bash
# Delete space (with confirmation)
alt-dremio-cli space delete 66c76a3e-0335-463b-8622-1720f8546537

# Delete without confirmation
alt-dremio-cli space delete 66c76a3e-0335-463b-8622-1720f8546537 --yes

# Delete with specific tag
alt-dremio-cli space delete 66c76a3e-0335-463b-8622-1720f8546537 --tag "version-tag-123"
```

## Folder Commands

### Create Folder

Create a new folder.

```bash
alt-dremio-cli folder create --path <PATH> [OPTIONS]
```

**Options:**
- `--path TEXT` - Folder path as JSON array or slash-separated (required)
- `--description TEXT` - Folder description

**Examples:**

```bash
# Create folder with slash-separated path
alt-dremio-cli folder create --path "Analytics/Reports"

# Create with JSON array path
alt-dremio-cli folder create --path '["Analytics", "Reports", "2024"]'

# Create with description
alt-dremio-cli folder create --path "Sales/Data" --description "Sales data folder"

# Create nested folders
alt-dremio-cli folder create --path "Analytics/Reports/Monthly"
alt-dremio-cli folder create --path "Analytics/Reports/Quarterly"
```

### List Folders

List folders.

```bash
alt-dremio-cli folder list [OPTIONS]
```

**Options:**
- `--parent TEXT` - Parent folder/space ID or path

**Examples:**

```bash
# List all folders
alt-dremio-cli folder list

# List folders in specific parent
alt-dremio-cli folder list --parent "Analytics"

# List by parent ID
alt-dremio-cli folder list --parent abc-123-def-456

# JSON output
alt-dremio-cli --output json folder list
```

### Get Folder

Retrieve folder details by ID.

```bash
alt-dremio-cli folder get <FOLDER_ID>
```

**Arguments:**
- `FOLDER_ID` - The folder ID (UUID)

**Examples:**

```bash
# Get folder details
alt-dremio-cli folder get 116f8103-159d-4640-b64a-68469bcb21b1

# Get in JSON format
alt-dremio-cli --output json folder get 116f8103-159d-4640-b64a-68469bcb21b1
```

### Get Folder by Path

Retrieve folder details by path.

```bash
alt-dremio-cli folder get-by-path <PATH>
```

**Arguments:**
- `PATH` - The folder path (dot-separated or slash-separated)

**Examples:**

```bash
# Get by slash-separated path
alt-dremio-cli folder get-by-path "Analytics/Reports"

# Get by dot-separated path
alt-dremio-cli folder get-by-path "Analytics.Reports.Monthly"

# Get by JSON array path
alt-dremio-cli folder get-by-path '["Analytics", "Reports", "2024"]'
```

### Delete Folder

Delete a folder.

```bash
alt-dremio-cli folder delete <FOLDER_ID> [OPTIONS]
```

**Arguments:**
- `FOLDER_ID` - The folder ID (UUID)

**Options:**
- `--tag TEXT` - Version tag for optimistic concurrency control

**Examples:**

```bash
# Delete folder (with confirmation)
alt-dremio-cli folder delete 116f8103-159d-4640-b64a-68469bcb21b1

# Delete without confirmation
alt-dremio-cli folder delete 116f8103-159d-4640-b64a-68469bcb21b1 --yes
```

## Scenarios

### Creating an Organized Catalog

```bash
# 1. Create top-level spaces
alt-dremio-cli space create --name "Raw" --description "Raw data from sources"
alt-dremio-cli space create --name "Curated" --description "Cleaned and transformed data"
alt-dremio-cli space create --name "Analytics" --description "Business analytics views"

# 2. Create folder structure in Raw
alt-dremio-cli folder create --path "Raw/Customers"
alt-dremio-cli folder create --path "Raw/Orders"
alt-dremio-cli folder create --path "Raw/Products"

# 3. Create folder structure in Curated
alt-dremio-cli folder create --path "Curated/Dimensions"
alt-dremio-cli folder create --path "Curated/Facts"

# 4. Create folder structure in Analytics
alt-dremio-cli folder create --path "Analytics/Sales"
alt-dremio-cli folder create --path "Analytics/Marketing"
alt-dremio-cli folder create --path "Analytics/Finance"
```

### Medallion Architecture

```bash
# Bronze layer (raw data)
alt-dremio-cli space create --name "Bronze" --description "Raw data ingestion"
alt-dremio-cli folder create --path "Bronze/source_system_1"
alt-dremio-cli folder create --path "Bronze/source_system_2"

# Silver layer (cleaned data)
alt-dremio-cli space create --name "Silver" --description "Cleaned and validated data"
alt-dremio-cli folder create --path "Silver/customers"
alt-dremio-cli folder create --path "Silver/orders"
alt-dremio-cli folder create --path "Silver/products"

# Gold layer (business aggregates)
alt-dremio-cli space create --name "Gold" --description "Business-ready datasets"
alt-dremio-cli folder create --path "Gold/customer_360"
alt-dremio-cli folder create --path "Gold/sales_metrics"
alt-dremio-cli folder create --path "Gold/inventory_status"
```

### Department-Based Organization

```bash
# Create department spaces
alt-dremio-cli space create --name "Sales" --description "Sales department data"
alt-dremio-cli space create --name "Marketing" --description "Marketing department data"
alt-dremio-cli space create --name "Finance" --description "Finance department data"

# Create project folders within departments
alt-dremio-cli folder create --path "Sales/Q1_2024"
alt-dremio-cli folder create --path "Sales/Q2_2024"
alt-dremio-cli folder create --path "Marketing/Campaigns"
alt-dremio-cli folder create --path "Marketing/Analytics"
alt-dremio-cli folder create --path "Finance/Reports"
alt-dremio-cli folder create --path "Finance/Forecasts"
```

### Migration and Cleanup

```bash
# List all spaces
alt-dremio-cli --output json space list > spaces.json

# List all folders
alt-dremio-cli --output json folder list > folders.json

# Find empty folders
cat folders.json | jq '.[] | select(.datasetCount == 0)'

# Delete empty folders
for folder_id in $(cat folders.json | jq -r '.[] | select(.datasetCount == 0) | .id'); do
  alt-dremio-cli folder delete $folder_id --yes
done
```

## Common Workflows

### 1. Create Hierarchical Structure

```bash
# Create parent space
alt-dremio-cli space create --name "DataWarehouse"

# Create level 1 folders
alt-dremio-cli folder create --path "DataWarehouse/Staging"
alt-dremio-cli folder create --path "DataWarehouse/Production"

# Create level 2 folders
alt-dremio-cli folder create --path "DataWarehouse/Staging/Daily"
alt-dremio-cli folder create --path "DataWarehouse/Staging/Weekly"
alt-dremio-cli folder create --path "DataWarehouse/Production/Current"
alt-dremio-cli folder create --path "DataWarehouse/Production/Archive"

# Create level 3 folders
alt-dremio-cli folder create --path "DataWarehouse/Production/Current/2024"
alt-dremio-cli folder create --path "DataWarehouse/Production/Current/2023"
```

### 2. Batch Folder Creation

```bash
# Create folders from list
FOLDERS=(
  "Analytics/Reports/Daily"
  "Analytics/Reports/Weekly"
  "Analytics/Reports/Monthly"
  "Analytics/Dashboards/Executive"
  "Analytics/Dashboards/Operational"
)

for folder in "${FOLDERS[@]}"; do
  alt-dremio-cli folder create --path "$folder"
done
```

### 3. Folder Inventory

```bash
# Export folder structure
alt-dremio-cli --output json folder list > folder_inventory.json

# Generate tree view
cat folder_inventory.json | jq -r '.[] | .path | join("/")' | sort

# Count folders by parent
cat folder_inventory.json | jq -r '.[] | .path[0]' | sort | uniq -c
```

### 4. Space and Folder Cleanup

```bash
# Get space ID
SPACE_ID=$(dremio --output json space list | jq -r '.[] | select(.path[0] == "OldSpace") | .id')

# List all folders in space
alt-dremio-cli --output json folder list --parent $SPACE_ID > space_folders.json

# Delete all folders (bottom-up)
cat space_folders.json | jq -r '.[] | .id' | tac | while read folder_id; do
  alt-dremio-cli folder delete $folder_id --yes
done

# Delete space
alt-dremio-cli space delete $SPACE_ID --yes
```

## Tips

1. **Plan your structure**: Design folder hierarchy before creating
   ```
   Space/
   ├── Category1/
   │   ├── Subcategory1/
   │   └── Subcategory2/
   └── Category2/
   ```

2. **Use consistent naming**: Follow naming conventions
   ```bash
   alt-dremio-cli space create --name "analytics"  # lowercase
   alt-dremio-cli folder create --path "analytics/reports"  # lowercase
   ```

3. **Document structure**: Keep a README or diagram
   ```bash
   alt-dremio-cli --output json folder list | jq -r '.[] | .path | join("/")' > structure.txt
   ```

4. **Clean up regularly**: Remove unused folders
   ```bash
   alt-dremio-cli folder list | grep "old_"
   ```

## Error Handling

### Space Already Exists

```bash
$ alt-dremio-cli space create --name "Analytics"
Error: Space already exists
```

**Solution**: Use a different name or delete existing space.

### Parent Not Found

```bash
$ alt-dremio-cli folder create --path "NonExistent/folder"
Error: Parent path does not exist
```

**Solution**: Create parent first:
```bash
alt-dremio-cli space create --name "NonExistent"
alt-dremio-cli folder create --path "NonExistent/folder"
```

### Cannot Delete Non-Empty

```bash
$ alt-dremio-cli space delete abc-123
Error: Cannot delete non-empty space
```

**Solution**: Delete contents first:
```bash
# Delete all folders in space
alt-dremio-cli folder list --parent abc-123
# Delete each folder, then delete space
```

## Platform Differences

### Cloud
- Spaces are top-level folders
- Path: `source.namespace.folder`
- Example: `evangelism-2026.Analytics.Reports`

### Software
- Spaces are SPACE containers
- Folders are FOLDER containers
- Path: `space.folder` or `catalog.namespace.folder`
- Example: `Analytics.Reports` or `dremio-catalog.namespace.folder`

## Best Practices

1. **Organize by purpose**: Group related data together
2. **Use descriptive names**: Make structure self-documenting
3. **Limit nesting depth**: Keep hierarchy manageable (3-4 levels max)
4. **Document structure**: Maintain documentation of organization
5. **Regular cleanup**: Remove unused spaces and folders
6. **Consistent naming**: Follow naming conventions
7. **Plan for growth**: Design scalable structure
8. **Use folders for projects**: Separate temporary from permanent data
