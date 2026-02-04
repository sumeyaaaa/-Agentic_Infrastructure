# Agent Skills Directory

## Overview

This directory contains the **Skills** that the Chimera agents will use at runtime. A "Skill" is a specific capability package (e.g., `skill_download_youtube`, `skill_transcribe_audio`, `skill_generate_content`).

## Important Distinction

- **Skills** (this directory): Runtime capabilities for agents
- **MCP Servers** (external): Infrastructure bridges (database connectors, platform APIs)

## Structure

Each skill should have:
- `README.md`: Description, Input/Output contracts
- `interface.py` (or equivalent): Function signatures
- Implementation (to be added in later tasks)

## Planned Skills (Task 2.3)

1. `skill_trend_fetcher`: Fetch trending topics from platforms
2. `skill_content_generator`: Generate multimodal content
3. `skill_platform_publisher`: Publish to social platforms
4. `skill_analytics_collector`: Collect engagement metrics
5. `skill_wallet_manager`: Handle blockchain transactions

## Status

🚧 **Placeholder** - Skill interfaces will be defined in Task 2.3

