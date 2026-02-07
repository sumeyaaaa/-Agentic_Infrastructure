"""
MCP Connection Tester

This test verifies that the Tenx MCP Sense (tenxfeedbackanalytics) server
is properly configured and accessible.

Note: This test follows TDD principles - it may fail initially if MCP tools
are not available in the test environment, but it defines the contract
for MCP connectivity.
"""

import pytest
import json
import os
from pathlib import Path


class TestMCPConnection:
    """Test suite for MCP server connection and configuration."""

    def test_mcp_config_file_exists(self):
        """Verify that .cursor/mcp.json exists."""
        mcp_config_path = Path(".cursor/mcp.json")
        assert mcp_config_path.exists(), ".cursor/mcp.json must exist"

    def test_mcp_config_is_valid_json(self):
        """Verify that .cursor/mcp.json contains valid JSON."""
        mcp_config_path = Path(".cursor/mcp.json")
        with open(mcp_config_path, "r") as f:
            config = json.load(f)
        assert isinstance(config, dict), "MCP config must be a JSON object"

    def test_mcp_config_has_tenx_server(self):
        """Verify that tenxfeedbackanalytics server is configured."""
        mcp_config_path = Path(".cursor/mcp.json")
        with open(mcp_config_path, "r") as f:
            config = json.load(f)
        
        # Check for mcpServers key (Cursor format)
        if "mcpServers" in config:
            assert "tenxfeedbackanalytics" in config["mcpServers"], \
                "tenxfeedbackanalytics must be configured in mcpServers"
            server_config = config["mcpServers"]["tenxfeedbackanalytics"]
        # Check for servers key (VS Code format)
        elif "servers" in config:
            assert "tenxfeedbackanalytics" in config["servers"], \
                "tenxfeedbackanalytics must be configured in servers"
            server_config = config["servers"]["tenxfeedbackanalytics"]
        else:
            pytest.fail("MCP config must have either 'mcpServers' or 'servers' key")

    def test_mcp_config_has_correct_url(self):
        """Verify that the MCP server URL is correct."""
        mcp_config_path = Path(".cursor/mcp.json")
        with open(mcp_config_path, "r") as f:
            config = json.load(f)
        
        # Get server config
        if "mcpServers" in config:
            server_config = config["mcpServers"]["tenxfeedbackanalytics"]
        elif "servers" in config:
            server_config = config["servers"]["tenxfeedbackanalytics"]
        else:
            pytest.fail("MCP config must have server configuration")
        
        assert "url" in server_config, "Server config must have 'url' field"
        assert server_config["url"] == "https://mcppulse.10academy.org/proxy", \
            "MCP server URL must be https://mcppulse.10academy.org/proxy"

    def test_mcp_config_has_required_headers(self):
        """Verify that required headers are present."""
        mcp_config_path = Path(".cursor/mcp.json")
        with open(mcp_config_path, "r") as f:
            config = json.load(f)
        
        # Get server config
        if "mcpServers" in config:
            server_config = config["mcpServers"]["tenxfeedbackanalytics"]
        elif "servers" in config:
            server_config = config["servers"]["tenxfeedbackanalytics"]
        else:
            pytest.fail("MCP config must have server configuration")
        
        assert "headers" in server_config, "Server config must have 'headers' field"
        headers = server_config["headers"]
        
        assert "X-Device" in headers, "Headers must include X-Device"
        assert headers["X-Device"] in ["mac", "linux", "windows"], \
            "X-Device must be one of: mac, linux, windows"
        
        assert "X-Coding-Tool" in headers, "Headers must include X-Coding-Tool"
        assert headers["X-Coding-Tool"] in ["cursor", "vscode", "claude"], \
            "X-Coding-Tool must be one of: cursor, vscode, claude"

    def test_mcp_log_file_exists(self):
        """Verify that MCP connection log exists."""
        mcp_log_path = Path("research/mcp_log.md")
        assert mcp_log_path.exists(), \
            "research/mcp_log.md must exist (MCP connection log)"

    def test_mcp_log_contains_connection_info(self):
        """Verify that MCP log contains connection information."""
        mcp_log_path = Path("research/mcp_log.md")
        with open(mcp_log_path, "r") as f:
            log_content = f.read()
        
        # Check for key sections
        assert "tenxfeedbackanalytics" in log_content.lower() or \
               "tenx" in log_content.lower(), \
            "MCP log must mention tenxfeedbackanalytics or Tenx"
        
        assert "connection" in log_content.lower() or \
               "connected" in log_content.lower(), \
            "MCP log must document connection status"

    @pytest.mark.skip(reason="Requires active MCP server connection - manual test only")
    def test_mcp_server_is_accessible(self):
        """
        Verify that MCP server is accessible.
        
        NOTE: This test is skipped by default because it requires
        an active MCP server connection. Run manually with:
        pytest tests/test_mcp_connection.py::TestMCPConnection::test_mcp_server_is_accessible -v
        
        This test would verify that:
        1. MCP server responds to ping/health check
        2. Tools are discoverable
        3. Authentication is valid
        """
        # This would require MCP client library integration
        # For now, this is a placeholder that defines the contract
        pass

    @pytest.mark.skip(reason="Requires MCP client library - to be implemented")
    def test_mcp_tools_are_discoverable(self):
        """
        Verify that MCP tools (log_passage_time_trigger, etc.) are discoverable.
        
        NOTE: This test requires MCP client library integration.
        It defines the contract: MCP tools must be discoverable at runtime.
        """
        # Expected tools:
        # - log_passage_time_trigger
        # - log_performance_outlier_trigger
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


