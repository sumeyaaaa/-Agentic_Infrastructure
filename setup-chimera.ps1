# Project Chimera - Environment Setup Automation
# Task 1.3: The "Golden" Environment Setup
# Date: $(Get-Date -Format "yyyy-MM-dd")
# Author: FDE Trainee

# ============================================
# CONFIGURATION SECTION - EDIT THESE VALUES
# ============================================

$Config = @{
    # Repository Information
    RepositoryUrl = "https://github.com/sumeyaaaa/-Agentic_Infrastructure.git"
    RepositoryName = "-Agentic_Infrastructure"
    ProjectRoot = "https://github.com/sumeyaaaa/-Agentic_Infrastructure"  
    
    # MCP Server Configuration
    MCPSenseServer = "localhost:8080"  # Tenx MCP Sense server
    MCPApiKey = $env:MCP_API_KEY  # Load from environment variable
    
    # Python Environment
    PythonVersion = "3.11"
    UVVersion = "latest"
    
    # Project Structure
    Directories = @(
        "research",
        "specs", 
        "skills",
        "tests",
        "src",
        "src/agents",
        "src/mcp_servers",
        "src/utils",
        ".cursor",
        ".github/workflows",
        "docs",
        "config",
        "logs"
    )
    
    # Required Files
    Files = @(
        "research/architecture_strategy.md",
        "research/tooling_strategy.md",
        "specs/_meta.md",
        "specs/functional.md", 
        "specs/technical.md",
        "specs/openclaw_integration.md",
        "skills/README.md",
        "tests/test_trend_fetcher.py",
        "tests/test_skills_interface.py",
        ".cursor/rules",
        "CLAUDE.md",
        ".env.example",
        "pyproject.toml",
        "Dockerfile",
        "Makefile",
        ".gitignore",
        "README.md",
        ".github/workflows/main.yml"
    )
}

# ============================================
# FUNCTION DEFINITIONS
# ============================================

function Write-Step {
    param([string]$Message)
    Write-Host "`n" + ("=" * 80) -ForegroundColor Cyan
    Write-Host "STEP: $Message" -ForegroundColor Yellow
    Write-Host ("=" * 80) -ForegroundColor Cyan
}

function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

function Initialize-ProjectStructure {
    Write-Step "Creating Project Structure"
    
    # Create directories
    foreach ($dir in $Config.Directories) {
        $fullPath = Join-Path $Config.ProjectRoot $dir
        if (-not (Test-Path $fullPath)) {
            New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
            Write-Host "  Created: $dir" -ForegroundColor Green
        } else {
            Write-Host "  Exists: $dir" -ForegroundColor Gray
        }
    }
    
    # Create placeholder files
    foreach ($file in $Config.Files) {
        $fullPath = Join-Path $Config.ProjectRoot $file
        $dir = Split-Path $fullPath -Parent
        
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
        }
        
        if (-not (Test-Path $fullPath)) {
            switch ($file) {
                "research/architecture_strategy.md" {
                    @"
# Project Chimera: Domain Architecture Strategy

## 1. Executive Summary
$(Get-Date -Format "2026-02-04") - Architecture strategy based on Task 1.1 research.

## 2. Agent Pattern: Hierarchical Swarm (Planner-Worker-Judge)
**Decision**: Implement FastRender-inspired hierarchical swarm...

## 3. Human-in-the-Loop Framework
**Integration Point**: Judge agent decision layer...

## 4. Database Strategy: Polyglot Persistence
**Structured Data**: PostgreSQL for metadata...
**Unstructured Data**: MongoDB for logs/metrics...
**Vector Data**: Weaviate for agent memory...
**Media Files**: S3/GCS for video assets...

## 5. MCP Integration Layer
Core to all external interactions...
"@ | Out-File $fullPath -Encoding UTF8
                }
                
                ".cursor/rules" {
                    @"
# Project Chimera - Cursor Rules
# Generated: $(Get-Date -Format "2026-02-04")

## Project Context
This is Project Chimera, an autonomous influencer system implementing:
- Hierarchical Swarm architecture (Planner-Worker-Judge)
- MCP for all external integrations
- Agentic Commerce via Coinbase AgentKit
- Multi-tenant SaaS/PaaS platform

## Prime Directive
NEVER generate code without checking specs/ first.
ALWAYS refer to the architecture_strategy.md for system design.
VERIFY all external API calls go through MCP servers.

## Development Rules
1. Specification-First: Always check specs/ directory before implementation
2. Traceability: Add MCP telemetry comments to all agent interactions
3. Security: Never hardcode credentials; use environment variables
4. Testing: Write tests for all new skills and MCP servers
5. Documentation: Update relevant specs when changing architecture

## Agent Behavior Guidelines
- Planner agents decompose goals into DAGs
- Worker agents are stateless and specialized
- Judge agents validate all outputs with confidence scoring
- All financial actions require CFO Judge approval

## File Structure Conventions
- specs/: Human-readable specifications
- skills/: Reusable agent capability packages  
- src/mcp_servers/: External integration servers
- src/agents/: Core agent implementations
- tests/: Test-driven development fixtures
"@ | Out-File $fullPath -Encoding UTF8
                }
                
                "pyproject.toml" {
                    @"
[project]
name = "project-chimera"
version = "0.1.0"
description = "Autonomous Influencer Agent Platform"
authors = [{name = "FDE Trainee"}]
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "mcp>=1.0.0",
    "coinbase-agentkit>=0.5.0",
    "weaviate-client>=4.0.0",
    "langchain>=0.1.0",
    "pydantic>=2.0.0",
    "redis>=5.0.0",
    "psycopg2-binary>=2.9.0",
    "pymongo>=4.0.0",
    "fastapi>=0.100.0",
    "uvicorn>=0.20.0",
    "httpx>=0.25.0",
    "tenacity>=8.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
version = "1.0.0"

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true

[tool.black]
line-length = 88
target-version = ['py311']
"@ | Out-File $fullPath -Encoding UTF8
                }
                
                "Dockerfile" {
                    @"
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast Python package management
RUN pip install uv

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies using uv
RUN uv pip install -e . --system

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 agent && chown -R agent:agent /app
USER agent

# Health check for MCP server
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8080/health')"

# Default command
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
"@ | Out-File $fullPath -Encoding UTF8
                }
                
                ".github/workflows/main.yml" {
                    @"
name: Chimera CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11"]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install uv
      run: pip install uv
    
    - name: Install dependencies
      run: uv pip install -e .[dev]
    
    - name: Lint with Black
      run: black --check src tests
    
    - name: Type check with mypy
      run: mypy src
    
    - name: Run tests
      run: pytest tests/ -v
    
    - name: Run spec compliance check
      run: python scripts/spec_check.py

  docker:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to DockerHub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: yourdockerhub/project-chimera:latest
"@ | Out-File $fullPath -Encoding UTF8
                }
                
                default {
                    "# Placeholder for $file`n# Created: $(Get-Date)" | Out-File $fullPath -Encoding UTF8
                }
            }
            Write-Host "  Created: $file" -ForegroundColor Green
        }
    }
}

function Initialize-GitRepository {
    Write-Step "Initializing Git Repository"
    
    Set-Location $Config.ProjectRoot
    
    if (Test-Path ".git") {
        Write-Host "  Git repository already exists" -ForegroundColor Yellow
        git status
    } else {
        Write-Host "  Initializing new Git repository..." -ForegroundColor Green
        git init
        git add .
        git commit -m "feat: Initial project structure for Project Chimera
        
        - Created architecture strategy document
        - Set up MCP-integrated project structure
        - Added core configuration files
        - Implemented CI/CD pipeline foundation
        
        Task: 1.3 Environment Setup
        Date: $(Get-Date -Format "yyyy-MM-dd")"
        
        if ($Config.RepositoryUrl -ne "https://github.com/yourusername/project-chimera.git") {
            git remote add origin $Config.RepositoryUrl
            Write-Host "  Remote origin set to: $($Config.RepositoryUrl)" -ForegroundColor Green
        }
    }
}

function Test-MCPConnection {
    Write-Step "Testing MCP Server Connection"
    
    $mcpTestScript = @"
import asyncio
import httpx
import os
from datetime import datetime

async def test_mcp_connection():
    """Test connection to Tenx MCP Sense server"""
    server_url = "$($Config.MCPSenseServer)"
    api_key = os.getenv("MCP_API_KEY", "$($Config.MCPApiKey)")
    
    print(f"Testing MCP connection to: {server_url}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    headers = {"X-API-Key": api_key} if api_key else {}
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test health endpoint
            health_response = await client.get(f"http://{server_url}/health", headers=headers)
            print(f"Health check: {health_response.status_code}")
            
            # Test MCP endpoints
            endpoints = ["/tools", "/resources", "/prompts"]
            for endpoint in endpoints:
                try:
                    response = await client.get(f"http://{server_url}{endpoint}", headers=headers)
                    print(f"{endpoint}: {response.status_code}")
                except Exception as e:
                    print(f"{endpoint}: ERROR - {str(e)}")
            
            return True
            
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_mcp_connection())
    exit(0 if success else 1)
"@
    
    $testFile = Join-Path $Config.ProjectRoot "test_mcp_connection.py"
    $mcpTestScript | Out-File $testFile -Encoding UTF8
    
    Write-Host "  Running MCP connection test..." -ForegroundColor Cyan
    python $testFile
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n  ✅ MCP connection successful!" -ForegroundColor Green
        Write-Host "  Connection details logged to: logs/mcp_connection.log" -ForegroundColor Gray
        
        # Log connection details
        $logEntry = @"
MCP Connection Test - $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
============================================================
Server: $($Config.MCPSenseServer)
Project: $($Config.RepositoryName)
Test Result: SUCCESS
Commit Hash: $(git rev-parse HEAD 2>$null || "N/A")
Python: $(python --version 2>&1)

Next Steps:
1. Verify MCP Sense telemetry is active
2. Commit this connection test
3. Proceed to Task 2.1: Master Specification
"@
        
        $logEntry | Out-File (Join-Path $Config.ProjectRoot "logs/mcp_connection.log") -Encoding UTF8 -Append
    } else {
        Write-Host "`n  ❌ MCP connection failed!" -ForegroundColor Red
        Write-Host "  Please check:" -ForegroundColor Yellow
        Write-Host "  1. Is Tenx MCP Sense server running?" -ForegroundColor Yellow
        Write-Host "  2. Is the server URL correct?" -ForegroundColor Yellow
        Write-Host "  3. Do you need to set MCP_API_KEY environment variable?" -ForegroundColor Yellow
    }
    
    Remove-Item $testFile -Force
}

function Setup-PythonEnvironment {
    Write-Step "Setting up Python Environment"
    
    Set-Location $Config.ProjectRoot
    
    # Check if uv is installed
    if (-not (Test-Command "uv")) {
        Write-Host "  Installing uv..." -ForegroundColor Cyan
        pip install uv
    }
    
    # Create virtual environment
    Write-Host "  Creating Python virtual environment..." -ForegroundColor Cyan
    uv venv
    
    # Activate and install dependencies
    Write-Host "  Installing dependencies..." -ForegroundColor Cyan
    
    $activateScript = if ($IsWindows) { ".venv\Scripts\activate.ps1" } else { ".venv/bin/activate" }
    
    if (Test-Path $activateScript) {
        & $activateScript
        uv pip install -e .
        Write-Host "  Dependencies installed successfully!" -ForegroundColor Green
    } else {
        Write-Host "  Virtual environment not found. Installing globally..." -ForegroundColor Yellow
        uv pip install -e . --system
    }
    
    # Verify installation
    Write-Host "`n  Verifying critical packages..." -ForegroundColor Cyan
    $packages = @("mcp", "pydantic", "httpx")
    foreach ($pkg in $packages) {
        try {
            python -c "import $pkg; print(f'  ✓ {($pkg+':').PadRight(15)} {getattr($pkg, '__version__', 'OK')}')"
        } catch {
            Write-Host "  ✗ $($pkg): NOT INSTALLED" -ForegroundColor Red
        }
    }
}

function Generate-Readme {
    Write-Step "Generating Project README"
    
    $readmeContent = @"
# Project Chimera: Autonomous Influencer Network

## Project Status
**Environment**: ✅ Setup Complete  
**MCP Connection**: ✅ $(if (Test-MCPConnectionInternal) { "Active" } else { "Pending" })  
**Repository**: Initialized  
**Last Setup**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## Architecture Overview
Project Chimera implements a hierarchical swarm of autonomous AI influencers with:
- **Planner-Worker-Judge** agent pattern
- **MCP** for all external integrations  
- **Agentic Commerce** via Coinbase AgentKit
- **Polyglot persistence** (PostgreSQL, Weaviate, S3, Redis)

## Quick Start

### Prerequisites
- Python 3.11+
- Docker (optional)
- Tenx MCP Sense Server

### Installation
```bash
# Clone repository
git clone $($Config.RepositoryUrl)

# Run setup script
.\setup-chimera.ps1

# Or manually:
uv pip install -e .