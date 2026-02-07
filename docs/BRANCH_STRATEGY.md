# Branch Strategy & Git Workflow

## Overview

This document defines the Git branching strategy and pull request workflow for Project Chimera. The strategy balances development velocity with code quality and safety.

**Reference**: `specs/_meta.md` §3 (Development Principles - Spec-Driven Development)

---

## Branch Model

We use a **GitHub Flow** variant optimized for spec-driven development:

### Main Branches

1. **`main`**: Production-ready code
   - Always deployable
   - Protected branch (requires PR approval)
   - All commits must pass CI/CD checks
   - Only merged from `develop` or hotfix branches

2. **`develop`**: Integration branch for features
   - Latest development changes
   - Protected branch (requires PR approval)
   - Merged to `main` for releases

### Supporting Branches

1. **`feature/*`**: New features or enhancements
   - Naming: `feature/skill-moltbook-trend-fetcher`, `feature/hitl-dashboard`
   - Created from: `develop`
   - Merged to: `develop`
   - Deleted after merge

2. **`fix/*`**: Bug fixes
   - Naming: `fix/rate-limiting-bug`, `fix/sanitization-edge-case`
   - Created from: `develop` (or `main` for hotfixes)
   - Merged to: `develop` (or `main` for hotfixes)
   - Deleted after merge

3. **`spec/*`**: Specification updates
   - Naming: `spec/frontend-api-contracts`, `spec/mcp-server-moltbook`
   - Created from: `develop`
   - Merged to: `develop`
   - Deleted after merge

4. **`hotfix/*`**: Critical production fixes
   - Naming: `hotfix/security-vulnerability`, `hotfix/critical-bug`
   - Created from: `main`
   - Merged to: `main` and `develop`
   - Deleted after merge

5. **`docs/*`**: Documentation updates
   - Naming: `docs/adr-0006`, `docs/api-documentation`
   - Created from: `develop`
   - Merged to: `develop`
   - Deleted after merge

---

## Branch Naming Conventions

### Format
```
{type}/{short-description}
```

### Examples
- ✅ `feature/skill-content-generator`
- ✅ `fix/redis-connection-pool`
- ✅ `spec/frontend-api-contracts`
- ✅ `hotfix/security-patch`
- ✅ `docs/branch-strategy`
- ❌ `my-feature` (missing type prefix)
- ❌ `Feature/NewSkill` (wrong case, use lowercase)
- ❌ `feature/new skill` (use hyphens, not spaces)

---

## Pull Request Workflow

### 1. Create Branch

```bash
# From develop
git checkout develop
git pull origin develop
git checkout -b feature/my-feature
```

### 2. Develop & Commit

**Commit Message Format**:
```
{type}: {short description}

{detailed explanation if needed}

Refs: specs/{spec-file}.md or #issue-number
```

**Commit Types**:
- `feat`: New feature
- `fix`: Bug fix
- `spec`: Specification update
- `docs`: Documentation
- `test`: Test additions/changes
- `refactor`: Code refactoring
- `ci`: CI/CD changes
- `chore`: Maintenance tasks

**Examples**:
```
feat: implement MoltBook trend fetcher worker

Implements the MoltBook Trend Fetcher Worker with input sanitization
and semantic filtering as specified in specs/technical.md.

Refs: specs/technical.md, specs/functional.md
```

```
fix: correct relevance score threshold validation

The threshold check was using < instead of <=, causing valid trends
to be filtered out.

Refs: specs/technical.md line 65
```

### 3. Push & Create PR

```bash
git push origin feature/my-feature
```

Create PR on GitHub with:
- **Title**: Same format as commit message
- **Description**: 
  - What changed and why
  - Reference to specs (e.g., `Refs: specs/technical.md`)
  - Testing notes
  - Screenshots (if UI changes)

### 4. PR Requirements

**Before Merge, PR Must**:
- ✅ Pass all CI/CD checks (tests, lint, security scans, spec-check)
- ✅ Have at least 1 approval from maintainer
- ✅ Be up-to-date with target branch (`develop` or `main`)
- ✅ Have no merge conflicts
- ✅ Reference relevant specs (for code changes)

**PR Labels**:
- `feature`: New feature
- `bug`: Bug fix
- `spec`: Specification update
- `docs`: Documentation
- `security`: Security-related change
- `breaking`: Breaking change
- `dependencies`: Dependency updates

### 5. Code Review Guidelines

**Reviewers Should Check**:
- ✅ Code aligns with specifications (`specs/` directory)
- ✅ Follows MCP-native principle (no direct API calls)
- ✅ Security best practices (input sanitization, no hardcoded secrets)
- ✅ Test coverage (new code has tests)
- ✅ Documentation updated (if needed)

**Review Comments**:
- Be constructive and specific
- Reference specs when requesting changes
- Approve if code meets standards, even if minor improvements possible

### 6. Merge Strategy

- **Merge Method**: Squash and merge (preferred) or merge commit
- **Delete Branch**: Yes (after merge)
- **Require Linear History**: Optional (squash merge ensures this)

---

## Release Workflow

### Creating a Release

1. **Prepare Release Branch** (if needed):
   ```bash
   git checkout develop
   git checkout -b release/v1.0.0
   ```

2. **Update Version**:
   - Update `pyproject.toml` version
   - Update `CHANGELOG.md` (if exists)

3. **Merge to Main**:
   ```bash
   git checkout main
   git merge develop  # or release branch
   git tag v1.0.0
   git push origin main --tags
   ```

4. **Create GitHub Release**:
   - Tag: `v1.0.0`
   - Title: `Release v1.0.0`
   - Description: Changelog entries

---

## Hotfix Workflow

For critical production issues:

1. **Create Hotfix Branch**:
   ```bash
   git checkout main
   git checkout -b hotfix/critical-bug
   ```

2. **Fix & Test**:
   - Make minimal changes to fix issue
   - Add tests if possible
   - Commit with `fix:` prefix

3. **Merge to Main**:
   ```bash
   git checkout main
   git merge hotfix/critical-bug
   git tag v1.0.1
   git push origin main --tags
   ```

4. **Merge to Develop**:
   ```bash
   git checkout develop
   git merge main
   git push origin develop
   ```

---

## Branch Protection Rules

### `main` Branch
- ✅ Require pull request reviews (1 approval minimum)
- ✅ Require status checks to pass (all CI jobs)
- ✅ Require branches to be up to date
- ✅ Require linear history (optional)
- ✅ Restrict pushes (no direct pushes, PRs only)

### `develop` Branch
- ✅ Require pull request reviews (1 approval minimum)
- ✅ Require status checks to pass (tests, lint, spec-check)
- ✅ Require branches to be up to date
- ✅ Restrict pushes (no direct pushes, PRs only)

---

## Spec-Driven Development Workflow

### For Code Changes

1. **Update Specs First** (if needed):
   ```bash
   git checkout -b spec/update-api-contract
   # Edit specs/technical.md
   git commit -m "spec: update API contract for trend fetcher"
   # Create PR, get approval, merge to develop
   ```

2. **Implement Code**:
   ```bash
   git checkout develop
   git checkout -b feature/implement-trend-fetcher
   # Write failing tests (TDD)
   # Implement code
   git commit -m "feat: implement trend fetcher worker

   Implements MoltBook Trend Fetcher Worker as specified in
   specs/technical.md and specs/functional.md.

   Refs: specs/technical.md, specs/functional.md"
   # Create PR, reference specs, get approval, merge
   ```

### For Spec-Only Changes

- Use `spec/*` branch
- PR must be approved by architecture lead
- No code changes required (specs are source of truth)

---

## Best Practices

1. **Keep Branches Small**: One feature/fix per branch
2. **Commit Often**: Small, logical commits
3. **Write Clear Messages**: Reference specs, explain why
4. **Update Specs First**: If behavior changes, update specs before code
5. **Test Before PR**: Run tests locally before pushing
6. **Rebase, Don't Merge**: Keep history clean (optional, depends on team preference)

---

## Troubleshooting

### Merge Conflicts

```bash
# Update your branch
git checkout feature/my-feature
git fetch origin
git rebase origin/develop  # or merge origin/develop

# Resolve conflicts, then
git add .
git rebase --continue  # or git commit (if merge)
git push origin feature/my-feature --force-with-lease
```

### Accidentally Committed to Wrong Branch

```bash
# Create new branch from current state
git checkout -b feature/correct-branch

# Reset original branch
git checkout develop
git reset --hard origin/develop
```

---

## References

- `specs/_meta.md` §3 (Development Principles)
- `.coderabbit.yaml` (AI code review rules)
- `.github/workflows/main.yml` (CI/CD pipeline)

---

**Last Updated**: 2026-02-07  
**Maintainer**: Project Chimera Team

