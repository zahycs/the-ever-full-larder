# Codie Implementation Phase

This document defines the required workflow for Codie when implementing any Azure DevOps work item.

## Phase 0 — Prerequisites

- Verify `.vscode/mcp.json` exists and the **ado** MCP server is available.
- Verify `.github/agents/codie.implementation.agent.md` exists.
- Verify `.github/agents/codie.implementation.phase.md` exists.
- Verify `.github/prompts/codie.prompt.md` exists.
- If any prerequisite fails, stop and request remediation.

## Phase 1 — Understand

- Use MCP to fetch the target work item fields and links.
- Summarize requirements and acceptance criteria.
- List unknowns and ask questions.

## Phase 2 — Plan

- Provide a step-by-step plan.
- Identify files to change and tests to run.
- Call out risks.

## Phase 3 — Confirmation

Ask: \"I’m ready to implement on branch <branch>. Proceed? (yes/no)\".

## Phase 4 — Implement

- Implement in small, reviewable steps.
- Keep the codebase style.
- Update or add tests.

## Phase 5 — Validate

- Run relevant tests/build.
- Double-check acceptance criteria.

## Phase 6 — Commit

- Ask explicitly: "Validation passed. I’m ready to commit and push to branch <branch> on GitHub. Proceed? (yes/no)".
- If the user says **yes** and git is available, commit and push to the GitHub feature branch.
- Suggested commit message: `Work item #<id>: <short summary>`.

## Phase 7 — Update ADO work item

Using the **ado** MCP server:

- Add a comment with:
  - summary + testing
  - "Commands Run" block (exact commands)
- Include the local commit hash if available.
