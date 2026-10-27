# Learning Skills

A cross-compatible collection of Codex and Claude Code skills for generating source-grounded learning notes and running persistent, interactive study sessions.

## Turn your source material into active learning

Reading something is not the same as understanding it—and a summary alone cannot tell you what you can actually explain, remember, or apply. Learning Skills turns a textbook chapter, article, course handout, or technical document into a structured study path, then guides you through it as an adaptive tutor.

The package combines two main workflows. `notes-generator` transforms your source into focused questions, source-grounded answers, and learning aids. `teach-me` then uses those notes and the original source to teach in small steps, test your understanding, respond to gaps, and remember where you stopped so your next session can pick up from there.

Use Learning Skills when you want:

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

Clone the repository and copy each skill into your personal Codex skills directory:

```bash
git clone https://gitlab.aisingapore.net/siew_weifeng/learning-skills.git
mkdir -p ~/.codex/skills
for skill in learning-skills/skills/*; do
  destination="$HOME/.codex/skills/$(basename "$skill")"
  if [ -e "$destination" ]; then
    printf 'Skipped existing skill: %s\n' "$destination"
  else
    cp -R "$skill" "$destination"
  fi
done
```

The script does not overwrite existing skills. Start a new Codex session after installation so all ten skills are discovered.

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

Claude Code can load the repository as one plugin. Clone it, then choose either a temporary or persistent installation.

### Load for one session

```bash
git clone https://gitlab.aisingapore.net/siew_weifeng/learning-skills.git
claude --plugin-dir ./learning-skills
```

### Load in every session

```bash
mkdir -p ~/.claude/skills
git clone https://gitlab.aisingapore.net/siew_weifeng/learning-skills.git ~/.claude/skills/learning-skills
```

Start a new Claude Code session after cloning. If a session is already open, run `/reload-plugins`.

### Use in Claude Code

Skills installed through the plugin are namespaced with `learning-skills`:

```text
/learning-skills:notes-generator Turn <source-path> into learning notes.
```

```text
/learning-skills:teach-me Use source <source-path> and notes <notes-path>.
```

Claude can also select a skill automatically when the request matches its description.

## Repository structure

```text
learning-skills/
├── .claude-plugin/
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

Validate the complete Claude Code plugin when Claude Code is installed:

```bash
claude plugin validate . --strict
```

Test direct, indirect, incomplete, negative, and edge-case prompts before publishing changes.

## License

Licensed under the [MIT License](LICENSE). Copyright © 2026 Siew Wei Feng.
