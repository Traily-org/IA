---
name: adr-writer
description: Scaffolds a new numbered Architecture Decision Record in docs/adr/ using a standard Context/Decision/Status/Consequences template. Use whenever a structural technical decision is made (framework choice, library choice, service boundary, data model change).
---

# ADR writer

1. List existing files in `docs/adr/` and find the highest `NNNN-*.md`
   number (zero-padded to 4 digits). If the directory doesn't exist, create
   it and start at `0001`.
2. Create `docs/adr/000N-<kebab-case-title>.md` using this template:

   ```markdown
   # ADR 000N: <Title>

   ## Status
   Proposed | Accepted | Superseded by ADR-000X

   ## Context
   What problem or fork in the road made this decision necessary?

   ## Decision
   What was decided, in one or two sentences.

   ## Consequences
   What becomes easier or harder as a result; what was traded away.
   ```

3. Fill every section from the conversation — never leave a section as a
   placeholder. Ask the user for anything you're missing rather than guessing.
4. Tell the user the exact file path created so they can review and commit it.
