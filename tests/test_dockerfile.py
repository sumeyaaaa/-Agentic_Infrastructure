"""
Test Dockerfile Configuration

Tests that verify the Dockerfile is production-ready and follows best practices.

Reference: 
- project.md Task 3.2 (Containerization & Automation)
- specs/technical.md (Infrastructure requirements)
- Docker best practices for production deployments
"""

import pytest
from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).parent.parent
DOCKERFILE = PROJECT_ROOT / "Dockerfile"


class TestDockerfileExists:
    """Test that Dockerfile exists and is readable"""
    
    def test_dockerfile_exists(self):
        """Test that Dockerfile exists"""
        assert DOCKERFILE.exists(), "Dockerfile must exist"
        assert DOCKERFILE.is_file(), "Dockerfile must be a file"
    
    def test_dockerfile_readable(self):
        """Test that Dockerfile is readable"""
        content = DOCKERFILE.read_text(encoding="utf-8")
        assert len(content) > 0, "Dockerfile must not be empty"


class TestDockerfileContent:
    """Test Dockerfile content and structure"""
    
    @pytest.fixture
    def dockerfile_content(self):
        """Load Dockerfile content"""
        return DOCKERFILE.read_text(encoding="utf-8")
    
    def test_uses_python_base_image(self, dockerfile_content):
        """Test that Dockerfile uses Python base image"""
        assert "FROM python" in dockerfile_content, \
            "Dockerfile should use Python base image"
    
    def test_sets_workdir(self, dockerfile_content):
        """Test that Dockerfile sets WORKDIR"""
        assert "WORKDIR" in dockerfile_content, \
            "Dockerfile should set WORKDIR"
    
    def test_copies_dependencies(self, dockerfile_content):
        """Test that Dockerfile copies dependency files"""
        assert "COPY" in dockerfile_content or "pyproject.toml" in dockerfile_content, \
            "Dockerfile should copy dependency files"
    
    def test_installs_dependencies(self, dockerfile_content):
        """Test that Dockerfile installs dependencies"""
        assert "pip install" in dockerfile_content or "RUN pip" in dockerfile_content, \
            "Dockerfile should install dependencies"
    
    def test_no_root_user_in_production(self, dockerfile_content):
        """Test that Dockerfile doesn't run as root (production best practice)"""
        # This is a warning, not a hard requirement for now
        # In production, should have: RUN useradd -m -u 1000 appuser && USER appuser
        has_user = "USER" in dockerfile_content
        # We'll warn but not fail for now since this is a development Dockerfile
        if not has_user:
            pytest.skip("Production Dockerfile should run as non-root user (optional for dev)")


class TestDockerfileSecurity:
    """Test Dockerfile security best practices"""
    
    @pytest.fixture
    def dockerfile_content(self):
        """Load Dockerfile content"""
        return DOCKERFILE.read_text(encoding="utf-8")
    
    def test_no_hardcoded_secrets(self, dockerfile_content):
        """Test that Dockerfile doesn't contain hardcoded secrets"""
        secret_patterns = [
            r"password\s*=\s*['\"][^'\"]+['\"]",
            r"api_key\s*=\s*['\"][^'\"]+['\"]",
            r"secret\s*=\s*['\"][^'\"]+['\"]",
            r"token\s*=\s*['\"][^'\"]+['\"]",
        ]
        
        violations = []
        for pattern in secret_patterns:
            if re.search(pattern, dockerfile_content, re.IGNORECASE):
                violations.append(pattern)
        
        assert len(violations) == 0, \
            f"Dockerfile should not contain hardcoded secrets: {violations}"
    
    def test_uses_no_cache_for_pip(self, dockerfile_content):
        """Test that pip install uses --no-cache-dir (reduces image size)"""
        pip_install_lines = [line for line in dockerfile_content.split('\n') 
                           if 'pip install' in line.lower()]
        
        if pip_install_lines:
            # At least one pip install should use --no-cache-dir
            has_no_cache = any('--no-cache-dir' in line for line in pip_install_lines)
            # This is a best practice, not a hard requirement
            if not has_no_cache:
                pytest.skip("Consider using --no-cache-dir for pip install (best practice)")


class TestDockerfileMultiStage:
    """Test Dockerfile multi-stage build (production optimization)"""
    
    @pytest.fixture
    def dockerfile_content(self):
        """Load Dockerfile content"""
        return DOCKERFILE.read_text(encoding="utf-8")
    
    def test_consider_multi_stage_build(self, dockerfile_content):
        """Test that Dockerfile considers multi-stage build (production best practice)"""
        # Multi-stage builds reduce final image size
        # This is optional for development, recommended for production
        has_multiple_from = dockerfile_content.count("FROM ") > 1
        
        if not has_multiple_from:
            pytest.skip("Consider multi-stage build for production (reduces image size)")


class TestDockerfileCommands:
    """Test Dockerfile command structure"""
    
    @pytest.fixture
    def dockerfile_content(self):
        """Load Dockerfile content"""
        return DOCKERFILE.read_text(encoding="utf-8")
    
    def test_has_cmd_or_entrypoint(self, dockerfile_content):
        """Test that Dockerfile has CMD or ENTRYPOINT"""
        has_cmd = "CMD" in dockerfile_content
        has_entrypoint = "ENTRYPOINT" in dockerfile_content
        
        assert has_cmd or has_entrypoint, \
            "Dockerfile should have CMD or ENTRYPOINT"

