"""Dremio Cloud API client."""

from typing import Any, Dict, Optional

from dremio_cli.client.base import BaseClient


class CloudClient(BaseClient):
    """Client for Dremio Cloud API."""

    def __init__(
        self,
        base_url: str,
        project_id: str,
        token: str,
        timeout: int = 30,
    ):
        """Initialize Cloud client.
        
        Args:
            base_url: Base URL for Dremio Cloud API
            project_id: Project ID
            token: Authentication token
            timeout: Request timeout in seconds
        """
        super().__init__(base_url, token, timeout)
        self.project_id = project_id

    def _project_endpoint(self, endpoint: str) -> str:
        """Build project-scoped endpoint.
        
        Args:
            endpoint: Endpoint path
            
        Returns:
            Project-scoped endpoint
        """
        return f"/projects/{self.project_id}/{endpoint.lstrip('/')}"

    # Catalog operations
    def get_catalog(self, include: Optional[str] = None) -> Dict[str, Any]:
        """Get catalog."""
        params = {"include": include} if include else None
        return self.get(self._project_endpoint("catalog"), params=params)

    def get_catalog_item(self, item_id: str, include: Optional[str] = None) -> Dict[str, Any]:
        """Get catalog item by ID."""
        params = {"include": include} if include else None
        return self.get(self._project_endpoint(f"catalog/{item_id}"), params=params)

    def get_catalog_item_by_path(self, path: str, include: Optional[str] = None) -> Dict[str, Any]:
        """Get catalog item by path."""
        params = {"include": include} if include else None
        return self.get(self._project_endpoint(f"catalog/by-path/{path}"), params=params)

    # Source operations
    def create_source(self, source_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a source."""
        return self.post(self._project_endpoint("catalog"), data=source_data)

    def update_source(self, source_id: str, source_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a source."""
        return self.put(self._project_endpoint(f"catalog/{source_id}"), data=source_data)

    def delete_source(self, source_id: str) -> None:
        """Delete a source."""
        return self.delete(self._project_endpoint(f"catalog/{source_id}"))
