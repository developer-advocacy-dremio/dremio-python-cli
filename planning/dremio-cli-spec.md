# Dremio CLI - Project Specification

## Executive Summary

This document specifies a comprehensive Command-Line Interface (CLI) for Dremio that supports both **Dremio Cloud** and **Dremio Software** deployments. The CLI will provide two operational modes:
1. **Command-based mode**: Execute single commands directly from the shell
2. **REPL mode**: Interactive shell for executing multiple commands in a session

The CLI will manage multiple profiles stored in `~/.dremio/profiles.yaml`, allowing users to easily switch between different Dremio environments.

---

## Table of Contents

1. [Project Goals](#project-goals)
2. [Architecture Overview](#architecture-overview)
3. [Profile Management](#profile-management)
4. [Authentication](#authentication)
5. [Command Structure](#command-structure)
6. [API Coverage](#api-coverage)
7. [Implementation Considerations](#implementation-considerations)
8. [Future Enhancements](#future-enhancements)

---

## Project Goals

### Primary Objectives
- Provide a unified CLI for both Dremio Cloud and Dremio Software
- Support all REST API operations available in both platforms
- Enable efficient workflow automation through scriptable commands
- Provide an interactive REPL for exploratory operations
- Manage multiple environment profiles seamlessly
- Deliver excellent user experience with helpful error messages and documentation

### Non-Goals
- GUI or web-based interface
- Direct database connectivity (use Dremio's query APIs instead)
- Custom query language (use Dremio's SQL API)

---

## Architecture Overview

### Technology Stack
- **Language**: Python 3.9+
- **CLI Framework**: Click (for command parsing and REPL)
- **HTTP Client**: requests or httpx
- **Configuration**: PyYAML
- **Output Formatting**: rich (for beautiful terminal output)
- **Testing**: pytest

### Project Structure
```
dremio-cli/
├── dremio_cli/
│   ├── __init__.py
│   ├── __main__.py              # Entry point
│   ├── cli.py                   # Main CLI group and REPL
│   ├── config.py                # Profile management
│   ├── client/
│   │   ├── __init__.py
│   │   ├── base.py              # Base client class
│   │   ├── cloud.py             # Dremio Cloud client
│   │   ├── software.py          # Dremio Software client
│   │   └── auth.py              # Authentication handlers
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── profile.py           # Profile management commands
│   │   ├── catalog.py           # Catalog operations
│   │   ├── source.py            # Source management
│   │   ├── space.py             # Space management
│   │   ├── folder.py            # Folder operations
│   │   ├── table.py             # Table operations
│   │   ├── view.py              # View operations
│   │   ├── udf.py               # User-defined functions
│   │   ├── job.py               # Job management
│   │   ├── reflection.py        # Reflection management
│   │   ├── user.py              # User management
│   │   ├── role.py              # Role management
│   │   ├── sql.py               # SQL execution
│   │   ├── search.py            # Search operations
│   │   ├── script.py            # Script management
│   │   ├── engine.py            # Engine management (Software)
│   │   ├── wlm.py               # Workload management
│   │   ├── tag.py               # Tag operations
│   │   ├── wiki.py              # Wiki operations
│   │   ├── grant.py             # Grant/privilege management
│   │   ├── lineage.py           # Lineage operations
│   │   ├── maintenance.py       # Data maintenance tasks
│   │   └── token.py             # Token management
│   ├── formatters/
│   │   ├── __init__.py
│   │   ├── table.py             # Table output formatter
│   │   ├── json.py              # JSON output formatter
│   │   └── yaml.py              # YAML output formatter
│   └── utils/
│       ├── __init__.py
│       ├── exceptions.py        # Custom exceptions
│       ├── validators.py        # Input validators
│       └── helpers.py           # Helper functions
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_commands/
│   └── test_client/
├── docs/
│   ├── installation.md
│   ├── quickstart.md
│   ├── commands/
│   └── examples/
├── setup.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Profile Management

### Profile Configuration File

**Location**: `~/.dremio/profiles.yaml`

**Structure**:
```yaml
default_profile: production

profiles:
  production:
    type: cloud  # or 'software'
    base_url: https://api.dremio.cloud/v0
    project_id: abc-123-def-456
    auth:
      type: pat  # personal access token
      token: dremio_pat_xxxxxxxxxxxxx
    
  staging:
    type: cloud
    base_url: https://api.dremio.cloud/v0
    project_id: xyz-789-uvw-012
    auth:
      type: oauth
      token: oauth_token_here
      refresh_token: refresh_token_here
      expires_at: 2024-12-31T23:59:59Z
  
  local-dev:
    type: software
    base_url: http://localhost:9047/api/v3
    auth:
      type: username_password
      username: dremio
      password: dremio123
      # Token will be cached here after first login
      token: _dremio4ksrt534vk7fkq64xh55g7776b
      token_expires: 2024-12-25T12:00:00Z
  
  on-prem:
    type: software
    base_url: https://dremio.company.com/api/v3
    auth:
      type: pat
      token: dremio_pat_xxxxxxxxxxxxx
```

### Profile Management Commands

```bash
# List all profiles
dremio profile list

# Show current active profile
dremio profile current

# Create a new profile (interactive)
dremio profile create <profile-name>

# Create a new profile (non-interactive)
dremio profile create <profile-name> \
  --type cloud \
  --base-url https://api.dremio.cloud/v0 \
  --project-id abc-123 \
  --auth-type pat \
  --token dremio_pat_xxx

# Update an existing profile
dremio profile update <profile-name> --base-url https://new-url.com

# Delete a profile
dremio profile delete <profile-name>

# Set default profile
dremio profile set-default <profile-name>

# Use a specific profile for a single command
dremio --profile staging catalog list

# Test profile connection
dremio profile test <profile-name>
```

---

## Authentication

### Supported Authentication Methods

#### Dremio Cloud
1. **Personal Access Token (PAT)** - Recommended
2. **OAuth Access Token**

#### Dremio Software
1. **Personal Access Token (PAT)** - Recommended
2. **OAuth Access Token** (Enterprise)
3. **Username/Password** (generates authentication token)

### Token Management

The CLI will:
- Store tokens securely in the profile configuration
- Automatically refresh OAuth tokens when expired
- Re-authenticate username/password credentials when tokens expire
- Provide commands to manually refresh or revoke tokens

```bash
# Refresh authentication for current profile
dremio auth refresh

# Refresh authentication for specific profile
dremio auth refresh --profile production

# Revoke current token
dremio auth revoke

# Login interactively (for username/password)
dremio auth login --profile local-dev
```

---

## Command Structure

### Global Options

All commands support these global options:
```bash
--profile <name>        # Use specific profile
--output <format>       # Output format: table, json, yaml (default: table)
--verbose, -v           # Verbose output
--quiet, -q             # Suppress non-essential output
--help, -h              # Show help
```

### REPL Mode

Start interactive mode:
```bash
dremio repl

# Or with specific profile
dremio repl --profile staging
```

REPL features:
- Command history
- Tab completion
- Multi-line input support
- Syntax highlighting
- Profile switching within REPL
- Exit with `exit` or `quit` or Ctrl+D

---

## API Coverage

### 1. Catalog Operations

#### Dremio Cloud
```bash
# Retrieve catalog
dremio catalog list [--include permissions|datasetCount]

# Get catalog item by ID
dremio catalog get <id> [--include permissions]

# Get catalog item by path
dremio catalog get-by-path <path> [--include permissions]
```

#### Dremio Software
```bash
# Same as Cloud, plus:
dremio catalog list [--include permissions|datasetCount] [--exclude children]
```

---

### 2. Source Management

#### Common Operations (Both Cloud & Software)
```bash
# List sources
dremio source list

# Create a source
dremio source create \
  --name MySource \
  --type S3 \
  --config '{"bucketName": "my-bucket", ...}'

# Create from file
dremio source create --from-file source-config.json

# Get source by ID
dremio source get <id>

# Get source by path
dremio source get-by-path <path>

# Update source
dremio source update <id> \
  --name NewName \
  --config '{"bucketName": "new-bucket"}'

# Update from file
dremio source update <id> --from-file updated-config.json

# Delete source
dremio source delete <id>

# Test source connection
dremio source test <id>

# Refresh source metadata
dremio source refresh <id>
```

#### Source Types
Support for all Dremio source types:
- S3, Azure Data Lake, Google Cloud Storage
- Snowflake, Redshift, BigQuery
- PostgreSQL, MySQL, Oracle, SQL Server
- MongoDB, Elasticsearch
- AWS Glue, Hive, Iceberg
- And many more...

---

### 3. Space Management

```bash
# List spaces
dremio space list

# Create space
dremio space create <name>

# Get space by ID
dremio space get <id> [--max-children 25] [--page-token <token>]

# Get space by path
dremio space get-by-path <path>

# Update space
dremio space update <id> --name <new-name>

# Delete space
dremio space delete <id>
```

---

### 4. Folder Management

```bash
# Create folder
dremio folder create --path '["MySource", "MyFolder"]'

# Get folder by ID
dremio folder get <id>

# Get folder by path
dremio folder get-by-path <path>

# Update folder
dremio folder update <id> --path '["MySource", "RenamedFolder"]'

# Delete folder
dremio folder delete <id>

# List folder contents
dremio folder list <id>
```

---

### 5. File Operations

```bash
# Get file by path
dremio file get-by-path <path>

# List files in folder
dremio file list <folder-path>
```

---

### 6. Table Management

```bash
# Format file/folder as table
dremio table create \
  --path '["MySource", "data", "file.csv"]' \
  --format Text \
  --field-delimiter ","

# Create from file
dremio table create --from-file table-config.json

# Get table by ID
dremio table get <id>

# Get table by path
dremio table get-by-path <path>

# Update table
dremio table update <id> --from-file updated-config.json

# Refresh table reflections
dremio table refresh <id>

# Delete table (revert to file/folder)
dremio table delete <id>

# Get table schema
dremio table schema <id>

# Analyze table
dremio table analyze <id>
```

---

### 7. View Management

```bash
# Create view
dremio view create \
  --path '["MySpace", "MyView"]' \
  --sql "SELECT * FROM MySource.MyTable"

# Create from file
dremio view create --from-file view-definition.json

# Get view by ID
dremio view get <id>

# Get view by path
dremio view get-by-path <path>

# Update view
dremio view update <id> \
  --sql "SELECT * FROM MySource.MyTable WHERE id > 100"

# Refresh view reflections
dremio view refresh <id>

# Delete view
dremio view delete <id>
```

---

### 8. User-Defined Functions (UDF)

```bash
# Create UDF
dremio udf create \
  --path '["MySource", "my_function"]' \
  --body "SELECT 1" \
  --return-type INTEGER

# Get UDF by ID
dremio udf get <id>

# Get UDF by path
dremio udf get-by-path <path>

# Update UDF
dremio udf update <id> --body "SELECT 2"

# Delete UDF
dremio udf delete <id>

# List UDFs
dremio udf list [--path <container-path>]
```

---

### 9. SQL Execution

```bash
# Execute SQL query
dremio sql execute "SELECT * FROM MySource.MyTable LIMIT 10"

# Execute from file
dremio sql execute --file query.sql

# Execute with parameters
dremio sql execute "SELECT * FROM table WHERE id = ?" --params 123

# Get query results in different formats
dremio sql execute "SELECT * FROM table" --output json
dremio sql execute "SELECT * FROM table" --output csv

# Save results to file
dremio sql execute "SELECT * FROM table" --output-file results.json
```

---

### 10. Job Management

```bash
# List jobs
dremio job list [--max-results 100] [--filter '{"jobState": ["COMPLETED"]}']

# Get job by ID
dremio job get <job-id>

# Get job results
dremio job results <job-id> [--limit 500] [--offset 0]

# Cancel job
dremio job cancel <job-id>

# Get job profile
dremio job profile <job-id>

# Download job profile
dremio job profile <job-id> --download profile.zip
```

---

### 11. Reflection Management (Software)

```bash
# List reflections
dremio reflection list [--dataset-id <id>]

# Get reflection summary
dremio reflection summary \
  [--filter '{"reflectionType": ["RAW"]}'] \
  [--order-by reflectionName]

# Create raw reflection
dremio reflection create-raw <dataset-id> \
  --name MyRawReflection \
  --display-fields '["field1", "field2"]'

# Create aggregation reflection
dremio reflection create-agg <dataset-id> \
  --name MyAggReflection \
  --dimensions '["field1"]' \
  --measures '["field2"]'

# Get reflection by ID
dremio reflection get <id>

# Update reflection
dremio reflection update <id> --enabled true

# Delete reflection
dremio reflection delete <id>

# Refresh reflection
dremio reflection refresh <id>

# Get reflection recommendations
dremio reflection recommendations <dataset-id>
```

---

### 12. User Management (Software)

```bash
# List users
dremio user list [--max-results 100]

# Create user
dremio user create \
  --username john.doe \
  --first-name John \
  --last-name Doe \
  --email john.doe@company.com \
  --password SecurePass123

# Get user by ID
dremio user get <user-id>

# Update user
dremio user update <user-id> \
  --first-name Jonathan \
  --email jonathan.doe@company.com

# Delete user
dremio user delete <user-id>

# Change user password
dremio user change-password <user-id> --password NewPassword123

# Get user privileges
dremio user privileges <user-id>

# Grant privileges to user
dremio user grant <user-id> \
  --catalog-id <catalog-id> \
  --privileges SELECT,ALTER
```

---

### 13. Role Management (Software - Enterprise)

```bash
# List roles
dremio role list

# Create role
dremio role create --name DataAnalyst

# Get role by ID
dremio role get <role-id>

# Update role
dremio role update <role-id> --name SeniorDataAnalyst

# Delete role
dremio role delete <role-id>

# Add users to role
dremio role add-users <role-id> --user-ids <id1>,<id2>

# Remove users from role
dremio role remove-users <role-id> --user-ids <id1>,<id2>

# Get role privileges
dremio role privileges <role-id>

# Grant privileges to role
dremio role grant <role-id> \
  --catalog-id <catalog-id> \
  --privileges SELECT,ALTER
```

---

### 14. Tag Management

```bash
# Create/update tags on catalog object
dremio tag set <catalog-id> --tags tag1,tag2,tag3

# Get tags for catalog object
dremio tag get <catalog-id>

# Delete all tags from catalog object
dremio tag delete <catalog-id>

# Search by tag
dremio search --filter '{"tags": ["tag1"]}'
```

---

### 15. Wiki Management

```bash
# Create/update wiki for catalog object
dremio wiki set <catalog-id> --text "# My Wiki\nDescription here"

# Create from markdown file
dremio wiki set <catalog-id> --file wiki.md

# Get wiki for catalog object
dremio wiki get <catalog-id>

# Delete wiki from catalog object
dremio wiki delete <catalog-id>
```

---

### 16. Grant/Privilege Management

```bash
# List available privileges for catalog object type
dremio grant privileges --type SOURCE

# Get grants for catalog object
dremio grant get <catalog-id>

# Set grants for catalog object
dremio grant set <catalog-id> \
  --grants '[
    {
      "granteeType": "USER",
      "id": "user-id",
      "privileges": ["SELECT", "ALTER"]
    }
  ]'

# Set from file
dremio grant set <catalog-id> --from-file grants.json

# Add grant
dremio grant add <catalog-id> \
  --grantee-type USER \
  --grantee-id <user-id> \
  --privileges SELECT,ALTER

# Remove grant
dremio grant remove <catalog-id> \
  --grantee-type USER \
  --grantee-id <user-id>
```

---

### 17. Lineage Operations

```bash
# Get lineage graph for dataset
dremio lineage get <dataset-id>

# Get lineage with depth limit
dremio lineage get <dataset-id> --depth 3

# Export lineage to file
dremio lineage get <dataset-id> --output-file lineage.json

# Visualize lineage (generate diagram)
dremio lineage visualize <dataset-id> --output lineage.png
```

---

### 18. Search Operations (Software)

```bash
# Search catalog
dremio search "my query" [--max-results 25]

# Search with filters
dremio search "sales" --filter '{"type": ["VIRTUAL_DATASET"]}'

# Search by type
dremio search --type PHYSICAL_DATASET

# Search in specific path
dremio search "orders" --path '["MySource"]'
```

---

### 19. Script Management (Software)

```bash
# List scripts
dremio script list [--created-by <user-id>] [--search <term>]

# Create script
dremio script create \
  --name "My Analysis" \
  --content "SELECT * FROM table" \
  --context '["MySpace"]'

# Get script by ID
dremio script get <script-id>

# Update script
dremio script update <script-id> \
  --name "Updated Analysis" \
  --content "SELECT * FROM table WHERE date > '2024-01-01'"

# Delete script
dremio script delete <script-id>
```

---

### 20. Engine Management (Software - Enterprise)

```bash
# List engines
dremio engine list

# Create engine
dremio engine create \
  --name MyEngine \
  --size SMALL \
  --auto-stop-minutes 30

# Get engine by ID
dremio engine get <engine-id>

# Update engine
dremio engine update <engine-id> --size MEDIUM

# Start engine
dremio engine start <engine-id>

# Stop engine
dremio engine stop <engine-id>

# Delete engine
dremio engine delete <engine-id>

# Get engine metrics
dremio engine metrics <engine-id>
```

---

### 21. Workload Management (Software - Enterprise)

```bash
# List queues
dremio wlm queue list

# Create queue
dremio wlm queue create \
  --name HighPriority \
  --max-memory-percent 50 \
  --max-cpu-percent 50

# Get queue by ID
dremio wlm queue get <queue-id>

# Update queue
dremio wlm queue update <queue-id> --max-memory-percent 60

# Delete queue
dremio wlm queue delete <queue-id>

# List rules
dremio wlm rule list

# Create routing rule
dremio wlm rule create \
  --name "Route Analytics" \
  --queue-id <queue-id> \
  --condition '{"user": ["analyst1", "analyst2"]}'
```

---

### 22. Data Maintenance (Software)

```bash
# List maintenance tasks
dremio maintenance list [--source <source-name>] [--type OPTIMIZE]

# Create OPTIMIZE task
dremio maintenance create-optimize \
  --source prod \
  --table-id "folder1.folder2.table1"

# Create EXPIRE_SNAPSHOTS task
dremio maintenance create-expire \
  --source prod \
  --table-id "folder1.folder2.table1"

# Get task by ID
dremio maintenance get <task-id>

# Update task
dremio maintenance update <task-id> --enabled false

# Delete task
dremio maintenance delete <task-id>

# Run task immediately
dremio maintenance run <task-id>
```

---

### 23. Token Management (Software - Enterprise)

```bash
# Create personal access token
dremio token create \
  --name "CI/CD Token" \
  --expires-in-days 90

# List personal access tokens
dremio token list

# Get token by ID
dremio token get <token-id>

# Revoke token
dremio token revoke <token-id>

# Create OAuth token
dremio token oauth \
  --grant-type password \
  --username dremio \
  --password dremio123
```

---

### 24. Dataset Operations

```bash
# Get dataset details
dremio dataset get <id>

# Promote dataset
dremio dataset promote <id>

# Get dataset graph
dremio dataset graph <id>

# Get dataset summary
dremio dataset summary <id>
```

---

### 25. External Token Providers (Software - Enterprise)

```bash
# List external token providers
dremio external-token list

# Create external token provider
dremio external-token create \
  --name MyProvider \
  --type OAUTH \
  --config '{"authUrl": "...", "tokenUrl": "..."}'

# Get provider by ID
dremio external-token get <provider-id>

# Update provider
dremio external-token update <provider-id> --from-file config.json

# Delete provider
dremio external-token delete <provider-id>

# Test provider
dremio external-token test <provider-id>
```

---

### 26. LDAP Authorization (Software - Enterprise)

```bash
# Sync LDAP groups
dremio ldap sync

# Get LDAP configuration
dremio ldap config

# Test LDAP connection
dremio ldap test
```

---

### 27. Node Collections (Software)

```bash
# List node collections
dremio node-collection list

# Create node collection
dremio node-collection create \
  --name "Analytics Nodes" \
  --tags '["analytics"]'

# Get node collection by ID
dremio node-collection get <collection-id>

# Update node collection
dremio node-collection update <collection-id> --tags '["analytics", "production"]'

# Delete node collection
dremio node-collection delete <collection-id>
```

---

## Implementation Considerations

### Error Handling

- Provide clear, actionable error messages
- Include API error details when available
- Suggest corrections for common mistakes
- Support `--verbose` flag for detailed error information

### Output Formatting

Support multiple output formats:
- **Table** (default): Human-readable tabular format using `rich`
- **JSON**: Machine-readable JSON output
- **YAML**: Human-readable YAML output
- **CSV**: For data export (where applicable)

### Pagination

- Automatically handle pagination for list operations
- Support `--max-results` to limit results
- Support `--all` flag to fetch all pages
- Show progress indicator for multi-page fetches

### Validation

- Validate inputs before making API calls
- Provide helpful suggestions for invalid inputs
- Support `--dry-run` flag to validate without executing

### Configuration

- Support environment variables for common settings:
  - `DREMIO_PROFILE`: Default profile to use
  - `DREMIO_OUTPUT_FORMAT`: Default output format
  - `DREMIO_BASE_URL`: Override base URL
  - `DREMIO_TOKEN`: Override authentication token

### Logging

- Support `--verbose` for detailed logging
- Log all API requests/responses in verbose mode
- Support `--log-file` to write logs to file

### Testing

- Unit tests for all command modules
- Integration tests against mock API
- End-to-end tests against real Dremio instances (optional)
- Test coverage > 80%

---

## Future Enhancements

### Phase 2 Features

1. **Bulk Operations**
   - Bulk import/export of catalog objects
   - Batch operations from CSV/JSON files
   - Parallel execution for performance

2. **Advanced Scripting**
   - Support for command scripts (`.dremio` files)
   - Variable substitution in scripts
   - Conditional execution

3. **Monitoring & Observability**
   - Real-time job monitoring
   - Performance metrics dashboard
   - Alert configuration

4. **Data Migration**
   - Migrate objects between Dremio instances
   - Export/import entire catalogs
   - Schema comparison tools

5. **CI/CD Integration**
   - GitHub Actions integration
   - GitLab CI templates
   - Jenkins plugins

6. **Interactive Wizards**
   - Source creation wizard
   - Reflection optimization wizard
   - Security configuration wizard

7. **Shell Completion**
   - Bash completion
   - Zsh completion
   - Fish completion

8. **Plugin System**
   - Custom command plugins
   - Custom formatters
   - Custom validators

---

## Installation & Distribution

### Installation Methods

```bash
# Via pip
pip install dremio-cli

# Via pipx (recommended)
pipx install dremio-cli

# From source
git clone https://github.com/your-org/dremio-cli
cd dremio-cli
pip install -e .
```

### Distribution

- Publish to PyPI
- Provide Docker image
- Provide standalone binaries (PyInstaller)
- Homebrew formula (macOS)
- apt/yum repositories (Linux)

---

## Documentation

### Required Documentation

1. **Installation Guide**
   - System requirements
   - Installation methods
   - Initial configuration

2. **Quick Start Guide**
   - First profile setup
   - Basic commands
   - Common workflows

3. **Command Reference**
   - Complete command documentation
   - Examples for each command
   - Parameter descriptions

4. **API Coverage Matrix**
   - Mapping of CLI commands to API endpoints
   - Feature parity between Cloud and Software

5. **Cookbook**
   - Common use cases
   - Best practices
   - Troubleshooting guide

6. **Developer Guide**
   - Contributing guidelines
   - Development setup
   - Testing procedures

---

## Success Metrics

### Adoption Metrics
- Number of installations
- Active users
- Command usage frequency

### Quality Metrics
- Test coverage > 80%
- Zero critical bugs
- Response time < 100ms for local operations

### User Satisfaction
- Documentation completeness
- Issue resolution time
- Community engagement

---

## Timeline & Milestones

### Phase 1: Core Foundation (Weeks 1-4)
- [ ] Project setup and architecture
- [ ] Profile management implementation
- [ ] Authentication system
- [ ] Basic catalog operations
- [ ] Source management
- [ ] Output formatting

### Phase 2: Extended Operations (Weeks 5-8)
- [ ] Table and view management
- [ ] SQL execution
- [ ] Job management
- [ ] User and role management
- [ ] Tag and wiki operations
- [ ] Grant management

### Phase 3: Advanced Features (Weeks 9-12)
- [ ] Reflection management
- [ ] Engine management
- [ ] Workload management
- [ ] Data maintenance
- [ ] Search operations
- [ ] Lineage visualization

### Phase 4: Polish & Release (Weeks 13-16)
- [ ] REPL mode refinement
- [ ] Comprehensive testing
- [ ] Documentation completion
- [ ] Performance optimization
- [ ] Package distribution
- [ ] Public release

---

## Appendix

### API Endpoint Mapping

#### Dremio Cloud API Endpoints
- Base URL: `https://api.dremio.cloud/v0/`
- Project-scoped: `/v0/projects/{project_id}/...`

#### Dremio Software API Endpoints
- Base URL: `{hostname}/api/v3/`
- Direct endpoints: `/api/v3/...`

### Supported Source Types

**Cloud Storage:**
- Amazon S3
- Azure Data Lake Storage (Gen1 & Gen2)
- Google Cloud Storage
- HDFS

**Data Warehouses:**
- Snowflake
- Amazon Redshift
- Google BigQuery
- Azure Synapse Analytics

**Databases:**
- PostgreSQL
- MySQL
- Oracle
- SQL Server
- MongoDB
- Elasticsearch

**Data Lakes:**
- AWS Glue
- Hive Metastore
- Apache Iceberg
- Delta Lake

**And many more...**

---

## Conclusion

This specification provides a comprehensive blueprint for building a powerful, user-friendly CLI for Dremio that supports both Cloud and Software deployments. The CLI will enable users to efficiently manage their Dremio environments, automate workflows, and integrate Dremio into their data pipelines.

The modular architecture ensures maintainability and extensibility, while the focus on user experience guarantees that the CLI will be a valuable tool for both beginners and advanced users.
