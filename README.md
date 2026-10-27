# Study Companion Skills

Turn source material into reviewed notes, then study with an adaptive tutor that tracks your progress.

## Turn your source material into active learning

Reading something is not the same as understanding it—and a summary alone cannot tell you what you can actually explain, remember, or apply. Study Companion Skills turns a textbook chapter, article, course handout, or technical document into a structured study path, then guides you through it as an adaptive tutor.

The package combines two main workflows. `notes-generator` transforms your source into focused questions, source-grounded answers, and learning aids. `teach-me` then uses those notes and the original source to teach in small steps, test your understanding, respond to gaps, and remember where you stopped so your next session can pick up from there.

Use Study Companion Skills when you want:

- **Study notes built for understanding:** your source material becomes clear explanations, focused questions, and learning aids while staying grounded in the original source.
- **Active learning, not passive rereading:** the tutor first teaches each concept, then assesses your understanding through retrieval, explanation, comparison, diagnosis, and application.
- **Teaching that adapts to you:** the tutor adjusts its explanations and questions based on what you understand and where you need more support.
- **Learning that improves your notes:** as you work through the material, the tutor can propose clearer explanations for your approval, helping your study notes evolve around your needs.
- **Progress that carries across sessions:** your concept coverage, answers, assessments, and next question are saved so you can continue where you stopped.

## How to use the skills

1. Put the material you want to learn in a file the assistant can access.
2. Run `notes-generator` with the source path. Unless you provide another notes path, it saves the matching study notes to `source_dir/notes/<source-stem>-notes.md`. If suitable notes already exist, you can skip this step.
3. Run `teach-me` with the exact source and notes paths reported by `notes-generator`.
4. Learn one manageable concept group at a time. Answer the tutor's questions, ask for clarification, request another example, or pause when needed.
5. Return later and resume from the saved progress file instead of reconstructing your place.

The installation sections below provide the exact commands and prompts for Codex and Claude Code.

## What you will experience

First, note generation deliberately works through the source in order. For every learning objective, it creates a focused question, an answer, and a useful learning aid, then subjects the draft to multiple review passes. This can take some time. Before it begins, `notes-generator` asks you to confirm that you are using an advanced model with the strongest available reasoning or effort setting.

Next, `teach-me` turns those notes into a conversation rather than a long lecture. The tutor explains a small group of concepts, asks a focused question that lets you demonstrate your understanding, evaluates your response against the notes and source, and adjusts what happens next. If an idea has not landed, the tutor can simplify it, approach it differently, or ask a more targeted follow-up before moving on.

After each session, you leave with more than a transcript:

- a record of which concepts were covered, tested, or still remain;
- feedback that distinguishes solid understanding from specific gaps;
- a pending question and saved position for the next session; and
- reviewed notes that stay under your control.

If the tutoring conversation produces a clearer explanation than the current notes, you will see the proposed change and choose whether to accept it. The package never silently rewrites your notes.

## Included skills

### Main workflows

- `teach-me` sets up a persistent study session from source material and matching notes.
- `notes-generator` creates reviewed learning notes from source material, subsection by subsection.

### Supporting workflows

- `teaching-loop`
- `question-generator`
- `answer-generator`
- `scope-reviewer`
- `final-boss`
- `learning-aid-creator`
- `alignment-reviewer`
- `transferability-reviewer`

Install the complete collection because the two main workflows delegate work to the supporting skills.

## Requirements

- Codex with skill support, or Claude Code with plugin support.
- An advanced model with the strongest available reasoning or effort setting when using `notes-generator`.
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
