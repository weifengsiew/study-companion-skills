# Study Companion Skills

**Stop just reading. Start understanding.**

Turn textbooks, articles, course materials, and technical documents into reviewed study notes—then learn with an adaptive AI tutor that teaches, tests your understanding, and remembers your progress.

## From passive reading to active learning

Reading something isn't the same as understanding it. And a summary alone can't tell you what you can actually explain, remember, or apply.

**Study Companion Skills combines two skills to bridge that gap:**

- **`notes-generator` — Turn your sources into study-ready notes.** Creates focused questions, source-grounded answers, and useful learning aids for every learning objective, with multiple review passes to improve quality.
- **`teach-me` — Learn with an adaptive tutor.** Teaches concepts in manageable steps, tests your understanding, identifies knowledge gaps, and adjusts its explanations and questions based on your responses.

**What makes it different?**

- **Active learning, not passive rereading.** Test your ability to recall, explain, compare, diagnose, and apply what you've learned.
- **Teaching that adapts to you.** Get simpler explanations, alternative approaches, and targeted follow-up questions when you're struggling.
- **Notes that evolve with your understanding.** Your tutor can propose clearer explanations for your approval, without silently rewriting your notes.
- **Progress that carries across sessions.** Your concept coverage, assessments, and next question are saved so you can pick up exactly where you left off.

**The goal isn't just better notes. It's knowing what you truly understand—and what you still need to learn.**

## Install with one prompt

Ready to turn your next reading into an interactive learning experience?

**Choose your AI coding assistant, copy the prompt, and let it handle the installation.**

### Claude Code

Paste this into Claude Code:

```text
Install Study Companion Skills from the GitHub repository weifengsiew/study-companion-skills as a user plugin, so it is available in all my projects. Add its marketplace if needed, then confirm that the plugin is enabled.
```

### Codex

Paste this into Codex:

```text
Install all skills from https://github.com/weifengsiew/study-companion-skills into my personal Codex skills directory. If a skill with the same name is already installed, leave it untouched and tell me. Codex should detect the new skills automatically; if it does not, tell me to restart Codex.
```

### Start learning

Once installed, turn your source material into an interactive learning experience:

1. **Choose your material.** Put the textbook chapter, article, course handout, or document you want to study in a file your assistant can access.
2. **Generate your study notes.** Run `notes-generator` with the source file path. By default, it saves the reviewed notes to `source_dir/notes/<source-stem>-notes.md`. If suitable notes already exist, you can skip this step.
3. **Start your tutoring session.** Run `teach-me` with the exact source and notes paths reported by `notes-generator` (or the paths to your existing notes).
4. **Learn at your own pace.** Work through one manageable concept group at a time. Answer questions, ask for clarification, request examples, or pause whenever you need.
5. **Pick up where you left off.** Return later and resume from your saved progress file without starting over.

**Note:** `notes-generator` performs multiple review passes, so note generation can take some time.

**Install Study Companion Skills and turn your next reading session into real learning.**

## Included skills

### Main workflows

- `teach-me` sets up a persistent study session from source material and matching notes.
- `quiz-me` sets up a persistent question-first assessment session and explains identified gaps.
- `notes-generator` creates reviewed learning notes from source material, subsection by subsection.

### Supporting workflows

- `teach-loop`
- `quiz-loop`
- `study-session-manager`
- `learning-preference-manager`
- `question-generator`
- `answer-generator`
- `scope-reviewer`
- `learning-aid-creator`
- `alignment-reviewer`
- `transferability-reviewer`

Install the complete collection because the main workflows delegate work to the supporting skills.

## Requirements

- Codex with skill support, or Claude Code with plugin support.
- Source material supplied by the learner. The `teach-me` workflow will not generate notes without it.

## Install in Codex

In Codex, ask:

```text
Install all skills from https://github.com/weifengsiew/study-companion-skills into my personal Codex skills directory (~/.agents/skills). If a skill with the same name is already installed, leave it untouched and tell me. Codex should detect the new skills automatically; if it does not, tell me to restart Codex.
```

Or install them manually in a terminal by cloning the repository and copying its skills:

```bash
git clone https://github.com/weifengsiew/study-companion-skills.git
mkdir -p ~/.agents/skills
for skill in study-companion-skills/skills/*; do
  destination="$HOME/.agents/skills/$(basename "$skill")"
  if [ -e "$destination" ]; then
    printf 'Skipped existing skill: %s\n' "$(basename "$skill")"
  else
    cp -R "$skill" "$destination"
  fi
done
```

Codex detects skill changes automatically. If the new skills do not appear, restart Codex.

### Update in Codex

From the directory containing your clone, pull the latest changes and copy them into your Codex skills directory. This replaces files for skills from this collection:

```bash
git -C study-companion-skills pull
for skill in study-companion-skills/skills/*; do
  destination="$HOME/.agents/skills/$(basename "$skill")"
  mkdir -p "$destination"
  cp -R "$skill/." "$destination/"
done
```

### Use in Codex

Generate notes:

```text
Use $notes-generator to turn <source-path> into learning notes.
```

Start a study session:

```text
Use $teach-me with source <source-path> and notes <notes-path>.
```

## Install in Claude Code

In Claude Code, ask:

```text
Install Study Companion Skills from the GitHub repository weifengsiew/study-companion-skills as a user plugin, so it is available in all my projects. Add its marketplace if needed, then confirm that the plugin is enabled.
```

Or install it from your terminal:

```bash
claude plugin marketplace add weifengsiew/study-companion-skills
claude plugin install study-companion-skills@study-companion-skills --scope user
```

### Load for one session

To try the plugin for one session without installing it:

```bash
git clone https://github.com/weifengsiew/study-companion-skills.git
claude --plugin-dir ./study-companion-skills
```

If Claude Code is already open, run `/reload-plugins` to load the plugin. Otherwise, it loads the next time you start Claude Code.

### Use in Claude Code

Skills installed through the plugin are namespaced with `study-companion-skills`:

```text
/study-companion-skills:notes-generator Turn <source-path> into learning notes.
```

```text
/study-companion-skills:teach-me Use source <source-path> and notes <notes-path>.
```

Claude can also select a skill automatically when the request matches its description.

### Update in Claude Code

Third-party marketplaces have automatic updates turned off by default. To update the plugin from your terminal, run:

```bash
claude plugin update study-companion-skills@study-companion-skills
```

## Repository structure

```text
study-companion-skills/
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
├── plugin.json
└── skills/
    ├── teach-me/
    ├── notes-generator/
    └── supporting skills...
```

Each skill contains a required `SKILL.md` and optional Codex UI metadata in `agents/openai.yaml`. The root `plugin.json` is the portable package manifest; `.claude-plugin/plugin.json` is the Claude Code compatibility manifest.

## Development

Validate a skill with the validator bundled with Codex's `skill-creator`:

```bash
python /path/to/skill-creator/scripts/quick_validate.py skills/teach-me
```

Validate the Claude Code plugin and marketplace when Claude Code is installed:

```bash
claude plugin validate .
```

Test direct, indirect, incomplete, negative, and edge-case prompts before publishing changes.

## License

Licensed under the [MIT License](LICENSE). Copyright © 2026 Siew Wei Feng.
