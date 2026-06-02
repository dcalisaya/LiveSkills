# Skill Template

Use this template to create a new skill. Copy the entire `_template/` directory and rename it.

## Quick Start

```bash
# Create a new skill
cp -r _template/ my-new-agent/

# Edit the SKILL.md
# 1. Update the YAML frontmatter (name, description, version)
# 2. Fill in the Agent Thinking Process
# 3. Define task types and their references
# 4. Set quality standards
# 5. Define structured output format

# Create reference files
# 1. One .md file per major topic
# 2. Include code templates, patterns, and checklists
# 3. Keep each reference self-contained and loadable independently
```

## Conventions

- Skill directory name: `kebab-case-agent/` (e.g., `data-analysis-agent/`)
- Main file: `SKILL.md` (always this exact name)
- References: `references/*.md` (one per topic)
- YAML frontmatter required: `name`, `description`, `version`, `maintainer`
- After creating the skill, add it to `MANIFEST.json` in the root directory
