"""
Test Spec Alignment

Tests that verify code aligns with specifications.
This ensures the Spec-Driven Development (SDD) principle is maintained.

Reference: specs/_meta.md, project.md Task 3.3
"""

import pytest
from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).parent.parent
SPECS_DIR = PROJECT_ROOT / "specs"
SKILLS_DIR = PROJECT_ROOT / "skills"
TESTS_DIR = PROJECT_ROOT / "tests"


class TestSpecsDirectory:
    """Test that specs/ directory has required files"""
    
    def test_specs_directory_exists(self):
        """Test that specs/ directory exists"""
        assert SPECS_DIR.exists(), "specs/ directory must exist"
        assert SPECS_DIR.is_dir(), "specs/ must be a directory"
    
    def test_required_spec_files_exist(self):
        """Test that all required spec files exist"""
        required_files = [
            "_meta.md",
            "functional.md",
            "technical.md",
            "openclaw_integration.md"
        ]
        
        for spec_file in required_files:
            spec_path = SPECS_DIR / spec_file
            assert spec_path.exists(), f"Required spec file missing: {spec_file}"
            assert spec_path.is_file(), f"{spec_file} must be a file"
    
    def test_meta_spec_has_vision(self):
        """Test that _meta.md contains project vision"""
        meta_spec = SPECS_DIR / "_meta.md"
        content = meta_spec.read_text(encoding="utf-8")
        
        assert "Project Vision" in content or "vision" in content.lower(), \
            "_meta.md must contain project vision"
    
    def test_meta_spec_has_constraints(self):
        """Test that _meta.md contains architectural constraints"""
        meta_spec = SPECS_DIR / "_meta.md"
        content = meta_spec.read_text(encoding="utf-8")
        
        assert "Constraint" in content or "constraint" in content.lower(), \
            "_meta.md must contain architectural constraints"


class TestSkillsSpecAlignment:
    """Test that skills align with specifications"""
    
    def test_skills_directory_exists(self):
        """Test that skills/ directory exists"""
        assert SKILLS_DIR.exists(), "skills/ directory must exist"
    
    def test_skill_interfaces_exist(self):
        """Test that skill interfaces exist"""
        if not SKILLS_DIR.exists():
            pytest.skip("skills/ directory not found")
        
        skill_dirs = [d for d in SKILLS_DIR.iterdir() 
                     if d.is_dir() and d.name.startswith("skill_")]
        
        assert len(skill_dirs) > 0, "At least one skill directory must exist"
        
        for skill_dir in skill_dirs:
            interface_file = skill_dir / "interface.py"
            assert interface_file.exists(), \
                f"{skill_dir.name} must have interface.py"
    
    def test_skill_interfaces_reference_specs(self):
        """Test that skill interfaces reference specs"""
        if not SKILLS_DIR.exists():
            pytest.skip("skills/ directory not found")
        
        skill_dirs = [d for d in SKILLS_DIR.iterdir() 
                     if d.is_dir() and d.name.startswith("skill_")]
        
        for skill_dir in skill_dirs:
            interface_file = skill_dir / "interface.py"
            if not interface_file.exists():
                continue
            
            content = interface_file.read_text(encoding="utf-8")
            
            # Check for spec references
            has_spec_ref = (
                "specs/" in content or
                "specification" in content.lower() or
                "skills/README.md" in content
            )
            
            assert has_spec_ref, \
                f"{skill_dir.name}/interface.py should reference specs/"
    
    def test_skill_interfaces_use_typedict(self):
        """Test that skill interfaces use TypedDict"""
        if not SKILLS_DIR.exists():
            pytest.skip("skills/ directory not found")
        
        skill_dirs = [d for d in SKILLS_DIR.iterdir() 
                     if d.is_dir() and d.name.startswith("skill_")]
        
        for skill_dir in skill_dirs:
            interface_file = skill_dir / "interface.py"
            if not interface_file.exists():
                continue
            
            content = interface_file.read_text(encoding="utf-8")
            
            assert "TypedDict" in content, \
                f"{skill_dir.name}/interface.py should use TypedDict for contracts"


class TestMCPNativePrinciple:
    """Test that code follows MCP-native principle (no direct API calls)"""
    
    def test_no_direct_http_requests_in_skills(self):
        """Test that skills don't use direct HTTP requests"""
        if not SKILLS_DIR.exists():
            pytest.skip("skills/ directory not found")
        
        forbidden_patterns = [
            r"requests\.(get|post|put|delete)",
            r"httpx\.(get|post|put|delete)",
            r"urllib\.request",
            r"aiohttp\.(get|post|put|delete)",
        ]
        
        skill_files = list(SKILLS_DIR.rglob("*.py"))
        violations = []
        
        for skill_file in skill_files:
            if skill_file.name == "__init__.py":
                continue
            
            content = skill_file.read_text(encoding="utf-8")
            
            for pattern in forbidden_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    violations.append((skill_file, pattern))
        
        assert len(violations) == 0, \
            f"Found direct HTTP calls (violates MCP-native principle): {violations}"


class TestSecuritySanitization:
    """Test that security sanitization is present"""
    
    def test_moltbook_skill_mentions_sanitization(self):
        """Test that MoltBook skill mentions sanitization"""
        if not SKILLS_DIR.exists():
            pytest.skip("skills/ directory not found")
        
        skill_dir = SKILLS_DIR / "skill_moltbook_trend_fetcher"
        if not skill_dir.exists():
            pytest.skip("skill_moltbook_trend_fetcher not found")
        
        interface_file = skill_dir / "interface.py"
        if not interface_file.exists():
            pytest.skip("interface.py not found")
        
        content = interface_file.read_text(encoding="utf-8")
        
        has_sanitization = (
            "sanitize" in content.lower() or
            "sanitization" in content.lower() or
            "_sanitize" in content
        )
        
        assert has_sanitization, \
            "skill_moltbook_trend_fetcher should mention input sanitization"


class TestDockerfile:
    """Test Dockerfile configuration"""
    
    def test_dockerfile_exists(self):
        """Test that Dockerfile exists"""
        dockerfile = PROJECT_ROOT / "Dockerfile"
        assert dockerfile.exists(), "Dockerfile must exist"
    
    def test_dockerfile_uses_python(self):
        """Test that Dockerfile uses Python base image"""
        dockerfile = PROJECT_ROOT / "Dockerfile"
        content = dockerfile.read_text(encoding="utf-8")
        
        assert "FROM python" in content or "FROM python:" in content, \
            "Dockerfile should use Python base image"


class TestMakefile:
    """Test Makefile configuration"""
    
    def test_makefile_exists(self):
        """Test that Makefile exists"""
        makefile = PROJECT_ROOT / "Makefile"
        assert makefile.exists(), "Makefile must exist"
    
    def test_makefile_has_spec_check(self):
        """Test that Makefile has spec-check target"""
        makefile = PROJECT_ROOT / "Makefile"
        content = makefile.read_text(encoding="utf-8")
        
        assert "spec-check" in content, \
            "Makefile should have spec-check target"
    
    def test_makefile_has_test_target(self):
        """Test that Makefile has test target"""
        makefile = PROJECT_ROOT / "Makefile"
        content = makefile.read_text(encoding="utf-8")
        
        assert "test:" in content, \
            "Makefile should have test target"

