#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spec Check Script for Project Chimera

Verifies that code aligns with specifications in specs/ directory.
This script enforces the Spec-Driven Development (SDD) principle.

Reference: project.md Task 3.3, specs/_meta.md
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Tuple, Dict
import json

# Fix Windows encoding issues
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Color codes for terminal output (ASCII-safe alternatives)
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

# ASCII-safe symbols
CHECK = "[OK]"
CROSS = "[X]"
WARN = "[!]"
INFO = "[*]"

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
SPECS_DIR = PROJECT_ROOT / "specs"
SKILLS_DIR = PROJECT_ROOT / "skills"
TESTS_DIR = PROJECT_ROOT / "tests"


class SpecChecker:
    """Main spec checker class"""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.checks_passed = 0
        self.checks_failed = 0
    
    def error(self, message: str):
        """Record an error"""
        self.errors.append(message)
        self.checks_failed += 1
        print(f"{RED}{CROSS} ERROR:{RESET} {message}")
    
    def warning(self, message: str):
        """Record a warning"""
        self.warnings.append(message)
        print(f"{YELLOW}{WARN} WARNING:{RESET} {message}")
    
    def success(self, message: str):
        """Record a success"""
        self.checks_passed += 1
        print(f"{GREEN}{CHECK} PASS:{RESET} {message}")
    
    def check_specs_directory_exists(self) -> bool:
        """Check that specs/ directory exists with required files"""
        print(f"\n{BLUE}{INFO} Checking specs/ directory structure...{RESET}")
        
        required_specs = [
            "_meta.md",
            "functional.md",
            "technical.md",
            "openclaw_integration.md"
        ]
        
        if not SPECS_DIR.exists():
            self.error(f"specs/ directory not found at {SPECS_DIR}")
            return False
        
        missing = []
        for spec_file in required_specs:
            spec_path = SPECS_DIR / spec_file
            if not spec_path.exists():
                missing.append(spec_file)
            else:
                self.success(f"Found {spec_file}")
        
        if missing:
            self.error(f"Missing required spec files: {', '.join(missing)}")
            return False
        
        return True
    
    def check_skills_have_spec_references(self) -> bool:
        """Check that skill interfaces reference specs"""
        print(f"\n{BLUE}{INFO} Checking skill spec references...{RESET}")
        
        if not SKILLS_DIR.exists():
            self.warning("skills/ directory not found")
            return True
        
        skill_dirs = [d for d in SKILLS_DIR.iterdir() if d.is_dir() and d.name.startswith("skill_")]
        
        if not skill_dirs:
            self.warning("No skill directories found")
            return True
        
        for skill_dir in skill_dirs:
            interface_file = skill_dir / "interface.py"
            if not interface_file.exists():
                self.warning(f"No interface.py in {skill_dir.name}")
                continue
            
            content = interface_file.read_text(encoding="utf-8")
            
            # Check for spec references
            has_spec_ref = (
                "specs/" in content or
                "specs/functional.md" in content or
                "specs/technical.md" in content or
                "specs/openclaw_integration.md" in content or
                "skills/README.md" in content
            )
            
            if has_spec_ref:
                self.success(f"{skill_dir.name} references specs")
            else:
                self.warning(f"{skill_dir.name} interface.py should reference specs/")
    
    def check_tests_reference_specs(self) -> bool:
        """Check that test files reference specs"""
        print(f"\n{BLUE}{INFO} Checking test spec references...{RESET}")
        
        if not TESTS_DIR.exists():
            self.warning("tests/ directory not found")
            return True
        
        test_files = list(TESTS_DIR.glob("test_*.py"))
        
        if not test_files:
            self.warning("No test files found")
            return True
        
        for test_file in test_files:
            content = test_file.read_text(encoding="utf-8")
            
            # Check for spec references or docstrings mentioning specs
            has_spec_ref = (
                "specs/" in content or
                "specification" in content.lower() or
                "contract" in content.lower() or
                "skills/README.md" in content
            )
            
            if has_spec_ref:
                self.success(f"{test_file.name} references specs")
            else:
                self.warning(f"{test_file.name} should reference specs/ in docstrings")
    
    def check_no_direct_api_calls(self) -> bool:
        """Check for violations of MCP-native principle (no direct API calls)"""
        print(f"\n{BLUE}{INFO} Checking MCP-native principle (no direct API calls)...{RESET}")
        
        if not SKILLS_DIR.exists():
            return True
        
        # Patterns that indicate direct API calls (should use MCP instead)
        forbidden_patterns = [
            (r"requests\.(get|post|put|delete)", "Direct HTTP requests (use MCP server)"),
            (r"httpx\.(get|post|put|delete)", "Direct HTTPX calls (use MCP server)"),
            (r"urllib\.request", "Direct urllib calls (use MCP server)"),
            (r"aiohttp\.(get|post|put|delete)", "Direct aiohttp calls (use MCP server)"),
            (r"moltbook\.api", "Direct MoltBook API (use mcp-server-moltbook)"),
            (r"coinbase\.api", "Direct Coinbase API (use mcp-server-coinbase)"),
            (r"weaviate\.Client", "Direct Weaviate client (use mcp-server-weaviate)"),
        ]
        
        skill_files = list(SKILLS_DIR.rglob("*.py"))
        violations = []
        
        for skill_file in skill_files:
            if skill_file.name == "__init__.py":
                continue
            
            content = skill_file.read_text(encoding="utf-8")
            
            for pattern, description in forbidden_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    violations.append((skill_file, description))
        
        if violations:
            for file_path, desc in violations:
                self.error(f"{file_path.relative_to(PROJECT_ROOT)}: {desc}")
            return False
        else:
            self.success("No direct API calls detected (MCP-native principle respected)")
            return True
    
    def check_security_sanitization(self) -> bool:
        """Check that security sanitization is mentioned in relevant skills"""
        print(f"\n{BLUE}{INFO} Checking security sanitization...{RESET}")
        
        # Skills that MUST have sanitization
        critical_skills = [
            "skill_moltbook_trend_fetcher",
            "skill_content_generator"
        ]
        
        found_sanitization = False
        
        for skill_name in critical_skills:
            skill_dir = SKILLS_DIR / skill_name
            if not skill_dir.exists():
                continue
            
            interface_file = skill_dir / "interface.py"
            if not interface_file.exists():
                continue
            
            content = interface_file.read_text(encoding="utf-8")
            
            # Check for sanitization mentions
            has_sanitization = (
                "sanitize" in content.lower() or
                "sanitization" in content.lower() or
                "_sanitize" in content or
                "input validation" in content.lower()
            )
            
            if has_sanitization:
                self.success(f"{skill_name} mentions sanitization")
                found_sanitization = True
            else:
                self.warning(f"{skill_name} should include input sanitization (specs/technical.md)")
        
        return found_sanitization
    
    def check_typedict_contracts(self) -> bool:
        """Check that skill interfaces use TypedDict for contracts"""
        print(f"\n{BLUE}{INFO} Checking TypedDict contracts...{RESET}")
        
        if not SKILLS_DIR.exists():
            return True
        
        skill_dirs = [d for d in SKILLS_DIR.iterdir() if d.is_dir() and d.name.startswith("skill_")]
        
        for skill_dir in skill_dirs:
            interface_file = skill_dir / "interface.py"
            if not interface_file.exists():
                continue
            
            content = interface_file.read_text(encoding="utf-8")
            
            # Check for TypedDict usage
            has_typedict = "TypedDict" in content
            
            if has_typedict:
                self.success(f"{skill_dir.name} uses TypedDict")
            else:
                self.warning(f"{skill_dir.name} should use TypedDict for contracts (specs/technical.md)")
        
        return True
    
    def check_dockerfile_exists(self) -> bool:
        """Check that Dockerfile exists"""
        print(f"\n{BLUE}{INFO} Checking Dockerfile...{RESET}")
        
        dockerfile = PROJECT_ROOT / "Dockerfile"
        if dockerfile.exists():
            self.success("Dockerfile exists")
            return True
        else:
            self.error("Dockerfile not found")
            return False
    
    def check_makefile_has_spec_check(self) -> bool:
        """Check that Makefile has spec-check target"""
        print(f"\n{BLUE}{INFO} Checking Makefile...{RESET}")
        
        makefile = PROJECT_ROOT / "Makefile"
        if not makefile.exists():
            self.error("Makefile not found")
            return False
        
        content = makefile.read_text(encoding="utf-8")
        
        if "spec-check" in content:
            self.success("Makefile has spec-check target")
            return True
        else:
            self.warning("Makefile should have spec-check target")
            return False
    
    def run_all_checks(self) -> bool:
        """Run all spec checks"""
        print(f"{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}Project Chimera - Spec Check{RESET}")
        print(f"{BLUE}{'='*60}{RESET}")
        
        checks = [
            self.check_specs_directory_exists,
            self.check_skills_have_spec_references,
            self.check_tests_reference_specs,
            self.check_no_direct_api_calls,
            self.check_security_sanitization,
            self.check_typedict_contracts,
            self.check_dockerfile_exists,
            self.check_makefile_has_spec_check,
        ]
        
        for check in checks:
            try:
                check()
            except Exception as e:
                self.error(f"Check failed with exception: {e}")
        
        # Print summary
        print(f"\n{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}Summary:{RESET}")
        print(f"  {GREEN}✅ Passed: {self.checks_passed}{RESET}")
        print(f"  {YELLOW}⚠️  Warnings: {len(self.warnings)}{RESET}")
        print(f"  {RED}❌ Errors: {len(self.errors)}{RESET}")
        print(f"{BLUE}{'='*60}{RESET}")
        
        if self.errors:
            print(f"\n{RED}Spec check FAILED with {len(self.errors)} error(s){RESET}")
            return False
        elif self.warnings:
            print(f"\n{YELLOW}Spec check PASSED with {len(self.warnings)} warning(s){RESET}")
            return True
        else:
            print(f"\n{GREEN}Spec check PASSED with no issues{RESET}")
            return True


def main():
    """Main entry point"""
    checker = SpecChecker()
    success = checker.run_all_checks()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

