# Dremio CLI

A comprehensive command-line interface for Dremio Cloud and Dremio Software.

## 🚀 Features

- **100% API Coverage** - Complete support for all Dremio APIs
- **Dual Platform Support** - Works with both Dremio Cloud and Software
- **Profile Management** - Easily switch between environments
- **Rich Output** - Table, JSON, and YAML formatting
- **Comprehensive Documentation** - Detailed guides for every feature

## 📦 Installation

```bash
pip install alt-dremio-cli
```

## ⚡ Quick Start

```bash
# Configure a profile
alt-dremio-cli profile create --name myprofile --type software \
  --base-url https://dremio.company.com \
  --username admin --password secret

# List catalog
alt-dremio-cli catalog list

# Execute SQL
alt-dremio-cli sql execute "SELECT * FROM customers LIMIT 10"

# Create a view
alt-dremio-cli view create --path "Analytics.summary" \
  --sql "SELECT * FROM customers WHERE region = 'US'"
```

## 📚 Documentation

**[Complete Documentation (GitHub) →](https://github.com/developer-advocacy-dremio/dremio-python-cli/tree/main/dremio-cli/docs)**

*(Use the link above if browsing on PyPI)*


### Core Guides

- **[Installation](docs/installation.md)** - Setup and configuration
- **[Profiles](docs/profiles.md)** - Manage connection profiles
- **[Catalog](docs/catalog.md)** - Browse and navigate data
- **[SQL](docs/sql.md)** - Execute queries and analyze plans
- **[Jobs](docs/jobs.md)** - Monitor query execution

### Data Management

- **[Sources](docs/sources.md)** - Connect to data systems
- **[Views](docs/views.md)** - Create virtual datasets
- **[Tables](docs/tables.md)** - Manage physical datasets
- **[Spaces & Folders](docs/spaces-folders.md)** - Organize your catalog

### Governance & Security

- **[Tags & Wiki](docs/tags-wiki.md)** - Document and categorize
- **[Grants](docs/grants.md)** - Access control and permissions
- **[Users](docs/users.md)** - User management
- **[Roles](docs/roles.md)** - Role-based access control
- **[Reflections](docs/reflections.md)** - Manage reflections
- **[Scripts](docs/scripts.md)** - Manage scripts (Cloud only)

### Dremio-as-Code (GitOps)

- **[Overview](docs/dac.md)** - Getting Started with DAC
- **[Sources](docs/dac_sources.md)** - Manage Sources
- **[Tables](docs/dac_tables.md)** - Manage Physical Tables
- **[Validations](docs/dac_validations.md)** - Data Quality Checks
- **[Reflections](docs/dac_reflections.md)** - Manage Reflections
- **[Governance](docs/dac_governance.md)** - Managing Access Control

### Productivity

- **[Favorites](docs/favorites.md)** - Save frequently used queries
- **[History](docs/history.md)** - View and re-run commands
- **[REPL](docs/repl.md)** - Interactive SQL Shell (Enhanced)
- **[Monitor](docs/monitor.md)** - Real-time System Monitor
- **[Catalog Explorer](docs/tui.md)** - Interactive Catalog TUI
- **[Init](docs/init.md)** - Interactive Configuration Wizard
- **[Completion](docs/completion.md)** - Shell Completion Scripts
- **[Lineage](docs/lineage.md)** - Visualize dataset dependencies

## 🎯 Key Features

### Catalog Operations
Browse and navigate your Dremio catalog with ease.

```bash
alt-dremio-cli catalog list
alt-dremio-cli catalog get <id>
alt-dremio-cli catalog get-by-path "MySpace.MyFolder.MyView"
```

### SQL Execution
Execute queries, explain plans, and validate syntax.

```bash
alt-dremio-cli sql execute "SELECT * FROM table"
alt-dremio-cli sql execute --file query.sql --async
alt-dremio-cli sql explain "SELECT * FROM table"
alt-dremio-cli sql validate "SELECT * FROM table"
```

### Source Management
Connect to and manage data sources.

```bash
alt-dremio-cli source list
alt-dremio-cli source create --name MyDB --type POSTGRES --config-file db.json
alt-dremio-cli source refresh <id>
```

### View Management
Create and manage virtual datasets.

```bash
alt-dremio-cli view create --path "Analytics.summary" --sql "SELECT * FROM data"
alt-dremio-cli view update <id> --sql "SELECT * FROM updated_data"
alt-dremio-cli view list --space Analytics
```

### Job Management
Monitor and manage query jobs.

```bash
alt-dremio-cli job list
alt-dremio-cli job get <id>
alt-dremio-cli job results <id> --output-file results.json
alt-dremio-cli job profile <id> --download profile.zip
```

### Access Control
Manage permissions and grants.

```bash
alt-dremio-cli grant list <catalog-id>
alt-dremio-cli grant add <id> --grantee-type ROLE --grantee-id analyst --privileges SELECT
alt-dremio-cli user list
alt-dremio-cli role list
```

## 🔧 Configuration

### Profile-Based Configuration

```bash
# Create profile
alt-dremio-cli profile create --name prod --type cloud \
  --base-url https://api.dremio.cloud \
  --project-id <project-id> \
  --token <pat-token>

# Use profile
alt-dremio-cli --profile prod catalog list

# Set default profile
alt-dremio-cli profile set-default prod
```

### Environment Variables

```bash
# Set in .env file
DREMIO_BASE_URL=https://dremio.company.com
DREMIO_USERNAME=admin
DREMIO_PASSWORD=secret
```

## 📊 Output Formats

```bash
# Table format (default)
alt-dremio-cli catalog list

# JSON format
alt-dremio-cli --output json catalog list

# YAML format
alt-dremio-cli --output yaml catalog list
```

## 🌐 Platform Support

| Feature | Software | Cloud |
|---------|----------|-------|
| Catalog Operations | ✅ | ✅ |
| SQL Execution | ✅ | ⚠️ Limited |
| Job Management | ✅ | ✅ |
| View Management | ✅ | ✅ |
| Source Management | ✅ | ✅ |
| Grant Management | ✅ | ✅ |
| User/Role Management | ✅ | ⚠️ Via Console |

## 💻 Development

```bash
# Clone repository
git clone https://github.com/developer-advocacy-dremio/dremio-python-cli.git
cd dremio-python-cli/dremio-cli

# Install in development mode
pip install -e .

# Run tests
pytest

# Run live tests
python scripts/test_sql_operations.py
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Documentation](docs/README.md)
- [Dremio Documentation](https://docs.dremio.com)
- [Dremio Cloud](https://www.dremio.com/cloud/)
- [Dremio Software](https://www.dremio.com/platform/)

## 🆘 Support

For issues and questions:
- GitHub Issues: [Report an issue](https://github.com/developer-advocacy-dremio/dremio-python-cli/issues)
- Documentation: [Read the docs](docs/README.md)
- Community: [Dremio Community](https://community.dremio.com)
