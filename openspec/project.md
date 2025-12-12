# Project Context

## Purpose
WeavOps bridges GitOps with MCP-powered AI agents, automatically weaving your Git source of truth into autonomous, context-aware operations. It enables AI agents to understand and operate on infrastructure state stored in Git repositories, making GitOps workflows accessible through the Model Context Protocol (MCP).

## Tech Stack
- **Language**: Python 3.13+
- **Build System**: uv (using `uv_build` backend)
- **Package Manager**: uv
- **Type Checking**: Enabled (py.typed marker present)
- **Protocol**: MCP (Model Context Protocol) for AI agent integration

## Project Conventions

### Code Style
- Use type hints throughout all Python code
- Follow PEP 8 naming conventions
- Prefer explicit over implicit
- Keep modules focused and single-purpose

### Architecture Patterns
- MCP server pattern for AI agent integration
- GitOps as the source of truth for infrastructure state
- Stateless operations where possible

### Testing Strategy
- Unit tests for core functionality
- Integration tests for MCP protocol compliance
- Use pytest as the test framework

### Git Workflow
- Conventional commits with scope (e.g., `feat(mcp): add resource listing`)
- Main branch should always be deployable
- Feature branches for new development

## Domain Context
- **GitOps**: A paradigm where Git repositories serve as the single source of truth for declarative infrastructure and application configuration
- **MCP (Model Context Protocol)**: A protocol that enables AI agents to interact with external tools and data sources
- **AI Agents**: Autonomous systems that can understand context and execute operations
- This project connects these concepts, allowing AI agents to read, understand, and operate on GitOps-managed infrastructure

## Important Constraints
- Python 3.13+ required (no backwards compatibility with older Python versions)
- Must be compatible with MCP protocol specifications
- Should not modify Git state without explicit user approval
- Operations must be auditable and traceable

## External Dependencies
- MCP SDK/libraries for protocol implementation
- Git libraries for repository operations
- No external services required at runtime (self-contained)
