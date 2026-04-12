# User Management

This guide covers user management operations for administering user accounts in Dremio.

## Overview

**User Management** allows administrators to create, update, and manage user accounts. This is primarily available in Dremio Software.

## Commands

### List Users

```bash
alt-dremio-cli user list
```

### Get User

```bash
alt-dremio-cli user get <USER_ID>
```

### Create User

```bash
alt-dremio-cli user create --name "John Doe" --email john@company.com [--username john] [--password secret]
alt-dremio-cli user create --from-file user.json
```

### Update User

```bash
alt-dremio-cli user update <USER_ID> --from-file updated_user.json
```

### Delete User

```bash
alt-dremio-cli user delete <USER_ID>
```

## Examples

```bash
# List all users
alt-dremio-cli user list

# Create user
alt-dremio-cli user create --name "Jane Analyst" --email jane@company.com

# Get user details
alt-dremio-cli user get user-123

# Delete user
alt-dremio-cli user delete user-123
```

## User File Format

```json
{
  "name": "John Doe",
  "email": "john@company.com",
  "userName": "john",
  "password": "initial_password"
}
```

## Notes

- User management requires administrative privileges
- Primarily available in Dremio Software
- Cloud has different user management (via cloud console)
