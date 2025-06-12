"""
Django management command to run the Firebase MCP server.
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from mcp.server import FastMCP

# Import all tool modules to register the tools
from ...tools import auth, firestore, storage


class Command(BaseCommand):
    help = 'Run the Firebase MCP server'

    def handle(self, *args, **options):
        # Create FastMCP instance
        mcp = FastMCP("Firebase")

        # Register all tools from auth module
        mcp.tool()(auth.verify_id_token)
        mcp.tool()(auth.create_custom_token)
        mcp.tool()(auth.get_user)
        mcp.tool()(auth.delete_user)

        # Register all tools from firestore module
        mcp.tool()(firestore.get_document)
        mcp.tool()(firestore.create_document)
        mcp.tool()(firestore.update_document)
        mcp.tool()(firestore.delete_document)
        mcp.tool()(firestore.list_collections)
        mcp.tool()(firestore.query_collection)

        # Register all tools from storage module
        mcp.tool()(storage.upload_file)
        mcp.tool()(storage.download_file)
        mcp.tool()(storage.delete_file)
        mcp.tool()(storage.list_files)

        # Run the server based on transport configuration
        transport = settings.MCP_TRANSPORT

        if transport == "stdio":
            self.stdout.write(
                self.style.SUCCESS(
                    'Starting Firebase MCP server with stdio transport')
            )
            mcp.run(transport="stdio")
        elif transport == "http":
            self.stdout.write(
                self.style.SUCCESS(
                    'Starting Firebase MCP server with HTTP transport')
            )
            mcp.run(transport="streamable-http")
        else:
            raise ValueError(f"Unsupported transport: {transport}")
