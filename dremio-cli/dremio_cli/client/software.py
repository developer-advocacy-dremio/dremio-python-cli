"""Dremio Software API client."""

from typing import Any, Dict, Optional

from dremio_cli.client.base import BaseClient


class SoftwareClient(BaseClient):
    """Client for Dremio Software API."""

    def __init__(
        self,
        base_url: str,
        token: str,
        timeout: int = 30,
    ):
        """Initialize Software client.
        
        Args:
            base_url: Base URL for Dremio Software API
            token: Authentication token
            timeout: Request timeout in seconds
        """
        super().__init__(base_url, token, timeout)

    # Catalog operations
    def get_catalog(
        self,
        include: Optional[str] = None,
        exclude: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get catalog."""
        params = {}
        if include:
            params["include"] = include
        if exclude:
            params["exclude"] = exclude
        return self.get("catalog", params=params if params else None)

    def get_catalog_item(
        self,
        item_id: str,
        include: Optional[str] = None,
        exclude: Optional[str] = None,
        max_children: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get catalog item by ID."""
        params = {}
        if include:
            params["include"] = include
        if exclude:
            params["exclude"] = exclude
        if max_children:
            params["maxChildren"] = max_children
        return self.get(f"catalog/{item_id}", params=params or None)

    def get_catalog_item_by_path(
        self,
        path: str,
        include: Optional[str] = None,
        exclude: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get catalog item by path."""
        params = {}
        if include:
            params["include"] = include
        if exclude:
            params["exclude"] = exclude
        return self.get(f"catalog/by-path/{path}", params=params or None)

    # Source operations
    def create_source(self, source_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a source."""
        return self.post("catalog", data=source_data)

    def update_source(self, source_id: str, source_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a source."""
        return self.put(f"catalog/{source_id}", data=source_data)

    def delete_source(self, source_id: str) -> None:
        """Delete a source."""
        return self.delete(f"catalog/{source_id}")

    # SQL operations
    def execute_sql(self, sql: str, context: Optional[list] = None) -> Dict[str, Any]:
        """Execute SQL query."""
        data = {"sql": sql}
        if context:
            data["context"] = context
        return self.post("sql", data=data)

    # Job operations
    def get_job(self, job_id: str) -> Dict[str, Any]:
        """Get job by ID."""
        return self.get(f"job/{job_id}")

    def get_job_results(
        self,
        job_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get job results."""
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        return self.get(f"job/{job_id}/results", params=params or None)

    def cancel_job(self, job_id: str) -> None:
        """Cancel a job."""
        return self.post(f"job/{job_id}/cancel")

    # Job management operations
    def list_jobs(
        self,
        max_results: Optional[int] = None,
        filter_expr: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List jobs.
        
        Args:
            max_results: Maximum number of results
            filter_expr: Filter expression (e.g., 'state=COMPLETED')
            sort: Sort field (prefix with - for descending)
            
        Returns:
            Jobs list response
        """
        params = {}
        if max_results:
            params["maxResults"] = max_results
        if filter_expr:
            params["filter"] = filter_expr
        if sort:
            params["sort"] = sort
        return self.get("job", params=params if params else None)

    def get_job_profile(self, job_id: str) -> Any:
        """Get job profile for performance analysis.
        
        Args:
            job_id: Job ID
            
        Returns:
            Job profile data
        """
        return self.get(f"job/{job_id}/download")

    def get_job_reflections(self, job_id: str) -> Dict[str, Any]:
        """Get reflection information for a job.
        
        Args:
            job_id: Job ID
            
        Returns:
            Job reflection information
        """
        return self.get(f"job/{job_id}/reflection")

    # View operations
    def create_view(self, view_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a view.
        
        Args:
            view_data: View definition
            
        Returns:
            Created view
        """
        return self.post("catalog", data=view_data)

    def update_view(self, view_id: str, view_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a view.
        
        Args:
            view_id: View ID
            view_data: Updated view definition
            
        Returns:
            Updated view
        """
        return self.put(f"catalog/{view_id}", data=view_data)

    def delete_view(self, view_id: str, tag: str) -> None:
        """Delete a view.
        
        Args:
            view_id: View ID
            tag: Version tag for optimistic concurrency
        """
        return self.delete(f"catalog/{view_id}?tag={tag}")

    # Space operations
    def create_space(self, space_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a space.
        
        Args:
            space_data: Space definition with 'name' and optional 'description'
            
        Returns:
            Created space
        """
        # Create SPACE container
        data = {
            "entityType": "space",
            "name": space_data["name"],
        }
        if "description" in space_data:
            data["description"] = space_data["description"]
        
        return self.post("catalog", data=data)

    def delete_space(self, space_id: str, tag: str) -> None:
        """Delete a space.
        
        Args:
            space_id: Space ID
            tag: Version tag for optimistic concurrency
        """
        return self.delete(f"catalog/{space_id}?tag={tag}")

    # Folder operations
    def create_folder(self, folder_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a folder.
        
        Args:
            folder_data: Folder definition with 'path' and optional 'description'
            
        Returns:
            Created folder
        """
        # Create FOLDER container
        data = {
            "entityType": "folder",
            "path": folder_data["path"],
        }
        if "description" in folder_data:
            data["description"] = folder_data["description"]
        
        return self.post("catalog", data=data)

    def delete_folder(self, folder_id: str, tag: str) -> None:
        """Delete a folder.
        
        Args:
            folder_id: Folder ID
            tag: Version tag for optimistic concurrency
        """
        return self.delete(f"catalog/{folder_id}?tag={tag}")

    # Tag operations
    def set_tags(self, catalog_id: str, tags: list) -> None:
        """Set tags on a catalog object.
        
        Args:
            catalog_id: Catalog object ID
            tags: List of tag strings
        """
        return self.post(f"catalog/{catalog_id}/collaboration/tag", data={"tags": tags})

    def get_tags(self, catalog_id: str) -> dict:
        """Get tags from a catalog object.
        
        Args:
            catalog_id: Catalog object ID
            
        Returns:
            Tags data
        """
        return self.get(f"catalog/{catalog_id}/collaboration/tag")

    def delete_tags(self, catalog_id: str) -> None:
        """Delete tags from a catalog object.
        
        Args:
            catalog_id: Catalog object ID
        """
        return self.delete(f"catalog/{catalog_id}/collaboration/tag")

    # Wiki operations
    def set_wiki(self, catalog_id: str, text: str) -> None:
        """Set wiki on a catalog object.
        
        Args:
            catalog_id: Catalog object ID
            text: Wiki markdown text
        """
        return self.post(f"catalog/{catalog_id}/collaboration/wiki", data={"text": text})

    def get_wiki(self, catalog_id: str) -> dict:
        """Get wiki from a catalog object.
        
        Args:
            catalog_id: Catalog object ID
            
        Returns:
            Wiki data
        """
        return self.get(f"catalog/{catalog_id}/collaboration/wiki")

    def delete_wiki(self, catalog_id: str) -> None:
        """Delete wiki from a catalog object.
        
        Args:
            catalog_id: Catalog object ID
        """
        return self.delete(f"catalog/{catalog_id}/collaboration/wiki")
