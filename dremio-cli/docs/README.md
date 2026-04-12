# Dremio CLI Documentation

Complete documentation for the Dremio Command Line Interface.

## 📚 Table of Contents

### Getting Started
- **[Installation](installation.md)** - Install and set up the Dremio CLI
- **[Profiles](profiles.md)** - Configure connection profiles for Cloud and Software

### Core Operations
- **[Catalog](catalog.md)** - Browse and navigate the Dremio catalog
- **[SQL](sql.md)** - Execute SQL queries, explain plans, validate syntax
- **[Jobs](jobs.md)** - Monitor and manage query jobs

### Data Management
- **[Sources](sources.md)** - Manage data source connections
- **[Views](views.md)** - Create and manage virtual datasets
- **[Tables](tables.md)** - Promote and configure physical datasets
- **[Reflections](reflections.md)** - Manage reflections for acceleration
- **[Scripts](scripts.md)** - Manage scripts (Cloud only)
- **[Spaces & Folders](spaces-folders.md)** - Organize your data catalog

### Collaboration & Governance
- **[Tags & Wiki](tags-wiki.md)** - Document and categorize datasets
- **[Grants](grants.md)** - Manage access control and permissions

### Productivity
- **[Favorites](favorites.md)** - Save frequently used queries
- **[History](history.md)** - View and re-run commands

### Administration
- **[Users](users.md)** - User account management
- **[Roles](roles.md)** - Role-based access control

- **[Dremio-as-Code Guide](dac.md)** - GitOps for Dremio


## 🚀 Quick Start

```bash
# Install
pip install alt-dremio-cli

# Configure profile
alt-dremio-cli profile create --name myprofile --type software \
  --base-url https://dremio.company.com \
  --username admin --password secret

# List catalog
alt-dremio-cli catalog list

# Execute SQL
alt-dremio-cli sql execute "SELECT * FROM customers LIMIT 10"

# Create a view
alt-dremio-cli view create --path "Analytics.customer_summary" \
  --sql "SELECT id, name, email FROM customers"
```

## 📖 Documentation Guide

### By Use Case

**Data Exploration:**
1. [Catalog](catalog.md) - Browse available data
2. [SQL](sql.md) - Query your data
3. [Jobs](jobs.md) - Monitor query execution

**Data Engineering:**
1. [Sources](sources.md) - Connect to data systems
2. [Tables](tables.md) - Configure physical datasets
3. [Views](views.md) - Create virtual datasets

**Data Governance:**
1. [Tags & Wiki](tags-wiki.md) - Document datasets
2. [Grants](grants.md) - Control access
3. [Users](users.md) & [Roles](roles.md) - Manage users

**Organization:**
1. [Spaces & Folders](spaces-folders.md) - Structure your catalog
2. [Tags & Wiki](tags-wiki.md) - Categorize and document

## 🔧 Command Reference

### Catalog Operations
```bash
alt-dremio-cli catalog list              # List catalog items
alt-dremio-cli catalog get <id>          # Get item details
alt-dremio-cli catalog get-by-path <path> # Get by path
```

### SQL Operations
```bash
alt-dremio-cli sql execute <query>       # Execute SQL
alt-dremio-cli sql explain <query>       # Show execution plan
alt-dremio-cli sql validate <query>      # Validate syntax
```

### Source Management
```bash
alt-dremio-cli source list               # List sources
alt-dremio-cli source create             # Create source
alt-dremio-cli source refresh <id>       # Refresh metadata
```

### View Management
```bash
alt-dremio-cli view list                 # List views
alt-dremio-cli view create               # Create view
alt-dremio-cli view update <id>          # Update view
```

### Job Management
```bash
alt-dremio-cli job list                  # List jobs
alt-dremio-cli job get <id>              # Get job details
alt-dremio-cli job results <id>          # Get results
alt-dremio-cli job cancel <id>           # Cancel job
```

### Space & Folder Management
```bash
alt-dremio-cli space create --name <name>  # Create space
alt-dremio-cli folder create --path <path> # Create folder
```

### Access Control
```bash
alt-dremio-cli grant list <id>           # List grants
alt-dremio-cli grant add <id>            # Add grant
alt-dremio-cli user list                 # List users
alt-dremio-cli role list                 # List roles
```

## 🌐 Platform Support

| Feature | Software | Cloud |
|---------|----------|-------|
| Catalog Operations | ✅ | ✅ |
| SQL Execution | ✅ | ⚠️ Limited |
| Job Management | ✅ | ✅ |
| View Management | ✅ | ✅ |
| Source Management | ✅ | ✅ |
| Space/Folder Management | ✅ | ✅ |
| Tags & Wiki | ✅ | ✅ |
| Grant Management | ✅ | ✅ |
| User Management | ✅ | ⚠️ Via Console |
| Role Management | ✅ | ⚠️ Via Console |
| Table Operations | ✅ | ✅ |

## 💡 Tips & Best Practices

1. **Use profiles** - Configure multiple profiles for different environments
2. **JSON output** - Use `--output json` for scripting
3. **Verbose mode** - Add `--verbose` for debugging
4. **File-based operations** - Store SQL queries and configs in files
5. **Async execution** - Use `--async` for long-running queries

## 📝 Examples

### Data Pipeline
```bash
# 1. Create source
alt-dremio-cli source create --name MyDB --type POSTGRES --config-file db.json

# 2. Create space
alt-dremio-cli space create --name Analytics

# 3. Create view
alt-dremio-cli view create --path "Analytics.sales_summary" \
  --sql "SELECT date, SUM(amount) FROM sales GROUP BY date"

# 4. Grant access
alt-dremio-cli grant add <view-id> --grantee-type ROLE \
  --grantee-id analyst --privileges SELECT
```

### Monitoring
```bash
# List recent jobs
alt-dremio-cli job list --max-results 10

# Get job details
alt-dremio-cli job get <job-id>

# Download profile
alt-dremio-cli job profile <job-id> --download profile.zip
```

### Documentation
```bash
# Add wiki
alt-dremio-cli wiki set <id> --file README.md

# Add tags
alt-dremio-cli tag set <id> --tags "production,sensitive,pii"
```

## 🔗 Additional Resources

- [Dremio Documentation](https://docs.dremio.com)
- [Dremio Cloud API Reference](https://docs.dremio.com/cloud/reference/api/)
- [Dremio Software API Reference](https://docs.dremio.com/software/rest-api/)

## 🆘 Getting Help

```bash
# General help
alt-dremio-cli --help

# Command help
alt-dremio-cli <command> --help

# Subcommand help
alt-dremio-cli <command> <subcommand> --help
```

## 📄 License

See LICENSE file for details.
