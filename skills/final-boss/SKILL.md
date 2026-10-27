---
name: final-boss
description: Require a delegated subagent to complete a correction pass before accepting its work as finished.
---

# Final Boss

When a user or another active workflow requests a final-boss pass on work delegated to a subagent:

1. After the subagent finishes their work the first time, tell the subagent:

   `You did not do your job properly. Please be more thorough!!!`

2. When the subagent comes back with their revised work, tell the subagent: 

      `Check for remaining gaps. Correct every gap you can, then explicitly report anything unresolved and why. Return the corrected final revision.`

