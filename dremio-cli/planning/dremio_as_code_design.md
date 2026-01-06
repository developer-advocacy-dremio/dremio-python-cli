# Dremio-as-Code Design Document

## Objective
Enable "GitOps" style management of Dremio objects. Users should be able to define their Dremio state (PDS, VDS, Sources, Spaces, Folders, Reflections, Scripts, Roles, Users) in local files (YAML/JSON) and sync them to Dremio.

## Core Concepts

### 1. Scope & Configuration
To support large projects and team isolation, we will strictly enforce a **Scope**.
A `dremio.yaml` file at the root of the local project defines this scope.

**`dremio.yaml`**
```yaml
version: "1.0"
scope:
  path: "dremio-catalog.finance"  # Only sync this subtree
  type: "SPACE"                   # Options: SPACE, ICEBERGCATALOG, SOURCE
ignore:
  - "*.tmp"
```

### 2. State Representation
We will use a directory structure mirroring the Dremio namespace structure.
We will ALSO maintain a **local state snapshot** file (`.dremio_state.json`) to track the last known synced state. This allows us to detect deletions and changes efficiently without querying the entire Dremio estate every time, provided we stick to the scope.

**Directory Structure:**
```
my_project/
  ├── dremio.yaml              # Project config & Scope
  ├── .dremio_state.json       # Managed state snapshot (DO NOT EDIT)
  ├── folder/                  # Maps to "dremio-catalog.finance.folder"
  │   ├── view1.sql            # SQL content implies View
  │   └── view1.yaml           # Metadata (reflections, context)
  └── subfolder/
```

### 3. Catalog Types
The system will distinguish between:
*   **Space**: Traditional Dremio Space (Views, Folders).
*   **IcebergCatalog**: Treated as a **Source** in Dremio, but functions as a Catalog (Iceberg tables, Views) this would include things like Dremio Open Catalog, Snowflake Open Catalog, Databricks Unity Catalog, Iceberg Rest Connector and AWS Glue when it coes to sources in Dremio. Use `type: ICEBERGCATALOG` in `source.yaml`. (There is no Spaces in Cloud, only Dremio Open Catalog, and each top level folder in that catalog is a source. In software, Dremio Open Catalog is a source and each folder is a subfolder)

### 4. Commands

#### `dremio sync pull`
- **Goal**: Update local files AND state snapshot from Dremio.
- **Logic**:
    1.  Read `scope` from `dremio.yaml`.
    2.  Traverse Dremio API from that root path.
    3.  Write/Update local YAML/SQL files.
    4.  Update `.dremio_state.json`.

#### `dremio sync push`
- **Goal**: Apply local changes to Dremio.
- **Logic**:
    1.  Read local files & `dremio.yaml`.
    2.  Compare against `.dremio_state.json` AND/OR live API (configurable safety).
    3.  Compute Diff (Create, Update, Delete).
    4.  Apply changes to Dremio.
    5.  Update `.dremio_state.json`.

### 5. File Formats & Secrets

**Secrets**: Use `${ENV_VAR}` syntax.
**Reflections**: Embedded in dataset YAML.

**Example `view.yaml`:**
```yaml
type: VIEW
path: ["folder", "view1"] # Relative to scope
sql_file: "view1.sql"      # Pointer to SQL file
context: ["source"]
reflections:
  - name: "raw_ref"
    type: RAW
    fields: ["id", "amount"]
```

**Example `source.yaml` (if syncing a Source root):**
```yaml
type: SOURCE
name: "my-source"
config:
  accessKey: "${AWS_ACCESS_KEY}" 
  secretKey: "${AWS_SECRET_KEY}"
```

### 4. Implementation Strategy

#### Phase 1: Diff Engine
- Implement a `StateBuilder` that reads local files into a standard memory object.
- Implement a `CatalogFetcher` that builds the same memory object from API.
- Implement a `Differ` that compares two memory objects.

#### Phase 2: Apply Logic
- Implement `Apply` methods for each resource type (Create, Update, Delete).
- Handle dependencies (create Spaces before Views).

#### Phase 3: CLI Integration
- Add `dremio sync` command group.

## Challenges & Open Questions
1.  **Start/End State**: Do we track state in a `.dremio_state` file to know what changed? Or always diff against live API? (Diff against live is safer but slower).
2.  **Sensitive Data**: Credentials in Sources. We should support `${ENV_VAR}` substitution.
3.  **IDs vs Paths**: Dremio APIs often need IDs. We must resolve Paths to IDs dynamically during `push`.
4.  **Reflections**: Reflections are tied to datasets. They should be defined within the dataset's metadata file.

## Roadmap
1.  **Prototype**: `sync pull` to backup a space.
2.  **Prototype**: `sync push` to restore/update a space.
3.  **Full Scale**: Support Sources, RBAC, etc.
