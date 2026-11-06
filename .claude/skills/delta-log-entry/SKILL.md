---
name: delta-log-entry
description: Appends a correctly formatted row to DELTA_LOG.md recording a prescribed action, the friction actually observed, and the corrective action taken. Use whenever a documented setup, build, or install step didn't go exactly as written.
---

# Delta Log entry

When the user reports friction (a command failed, an env var was missing,
a step needed a manual fix), do the following:

1. If `DELTA_LOG.md` doesn't exist at the repo root, create it with this header:

   | Prescribed Action | Executed Reality (Observed Friction) | Corrective Action & Impacted Source Doc |
   |---|---|---|

2. Append one new row, in the same three columns, using what the user
   described. Keep language factual and specific (name the exact command,
   error, file, and commit if known) — never write vague entries like
   "had an issue."
3. If the corrective action changed a real file (README.md, .env.example,
   a script), make sure that column names the file and, if available,
   the commit hash.
4. Show the user the new row before/after so they can confirm it's accurate.
