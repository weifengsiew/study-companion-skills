# Study Companion Skills

**Stop just reading. Start understanding.**

Turn textbooks, articles, course materials, and technical documents into reviewed study notes—then learn with an adaptive AI tutor that teaches, tests your understanding, and remembers your progress.

## From passive reading to active learning

Reading something isn't the same as understanding it. And a summary alone can't tell you what you can actually explain, remember, or apply.

**Study Companion Skills combines three main workflows to bridge that gap:**

- **`notes-generator` — Turn your sources into study-ready notes.** Creates reviewed, source-grounded notes with a big-picture orientation, practical takeaway, focused questions, explanatory answers, and useful learning aids.
- **`teach-me` — Learn with an adaptive tutor.** Teaches concepts in manageable steps, tests your understanding, identifies knowledge gaps, and adjusts its explanations and questions based on your responses.
- **`quiz-me` — Test what you understand.** Runs a question-first assessment, identifies knowledge gaps, and explains only what needs improvement.

**What makes it different?**

- **Active learning, not passive rereading.** Test your ability to recall, explain, compare, diagnose, and apply what you've learned.
- **Teaching that adapts to you.** Get simpler explanations, alternative approaches, and targeted follow-up questions when you're struggling.
- **Notes that evolve with your understanding.** During `teach-me`, after every three mastered concept groups, your tutor compares confirmed explanations with your notes and proposes worthwhile improvements for your approval.
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
Install Study Companion Skills as a plugin from the GitHub repository weifengsiew/study-companion-skills. Add its marketplace if needed, install and enable the plugin, then tell me to start a new chat.
```

### Start learning

Once installed, turn your source material into an interactive learning experience:

1. **Choose your material.** Put the textbook chapter, article, course handout, or document you want to study in a file your assistant can access.
2. **Generate your study notes.** Run `notes-generator` with the source file path. By default, it saves the reviewed notes to `source_dir/notes/<source-stem>-notes.md`. If suitable notes already exist, you can skip this step.
3. **Choose how to learn.** Run `teach-me` for guided instruction or `quiz-me` for question-first assessment, using the exact source and notes paths reported by `notes-generator` (or the paths to your existing notes). At the start of each session, choose conceptual understanding, technical fluency, or a balanced mix, then choose multiple choice, short answer, or a mix.
4. **Learn at your own pace.** Work through one manageable concept group at a time. Answer questions, ask for clarification, request examples, test yourself, or pause whenever you need.
5. **Pick up where you left off.** Return later and resume from the saved teaching or quiz progress file without starting over.

**Note:** `notes-generator` performs multiple review passes, so note generation can take some time.

**Install Study Companion Skills and turn your next reading session into real learning.**

## Included skills

### Public workflows

- `teach-me` sets up a persistent study session from source material and matching notes.
- `quiz-me` sets up a persistent question-first assessment session and explains identified gaps.
- `notes-generator` creates reviewed learning notes from source material, subsection by subsection.

### Internal workflows

- `teach-loop`
- `quiz-loop`
- `study-session-manager`
- `learning-preference-manager`
- `question-generator`
- `answer-generator`
- `scope-reviewer`
- `learning-aid-creator`
- `big-picture-generator`
- `practical-takeaway-generator`
- `notes-formatter`
- `duplication-reviewer`
- `alignment-reviewer`
- `transferability-reviewer`

The plugin installs every workflow together. On OpenAI surfaces, only the three public workflows are selected automatically. In Claude Code, narrow internal descriptions guide ordinary requests through the public workflows while preserving delegated and explicit use.

## Requirements

- Codex or Claude Code with plugin support.
- Source material supplied by the learner. The `teach-me` and `quiz-me` workflows will not generate notes without it.

## Install in Codex

Add this repository as a plugin marketplace from your terminal:

```bash
codex plugin marketplace add weifengsiew/study-companion-skills
```

Start Codex and open the plugin browser:

```bash
codex
```

Then run `/plugins`, find **Study Companion Skills**, and select **Install plugin**. Start a new chat before using it for the first time.

### Update in Codex

Refresh the marketplace from your terminal:

```bash
codex plugin marketplace upgrade study-companion-skills
```

Open `/plugins` in Codex to confirm the installed version, then start a new chat.

### Use in Codex

Generate notes:

```text
Use $notes-generator to turn <source-path> into learning notes.
```

Start a guided study session:

```text
Use $teach-me with source <source-path> and notes <notes-path>.
```

Start a question-first quiz session:

```text
Use $quiz-me with source <source-path> and notes <notes-path>.
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

```text
/study-companion-skills:quiz-me Use source <source-path> and notes <notes-path>.
```

Use `teach-me`, `quiz-me`, or `notes-generator` as the normal entry points. Internal workflows remain available for delegation and explicit advanced use; their descriptions identify them as internal to discourage accidental routing.

### Update in Claude Code

Third-party marketplaces have automatic updates turned off by default. To update the plugin from your terminal, run:

```bash
claude plugin update study-companion-skills@study-companion-skills
```

## Repository structure

```text
study-companion-skills/
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
├── plugin.json
└── skills/
    ├── teach-me/
    ├── quiz-me/
    ├── notes-generator/
    └── supporting skills...
```

Each skill contains a required `SKILL.md` and optional UI metadata in `agents/openai.yaml`. On OpenAI surfaces, internal workflows set `allow_implicit_invocation: false`; Claude Code uses their narrowly scoped descriptions for routing. The root `plugin.json` is the portable package manifest; `.claude-plugin/plugin.json` is the Claude Code compatibility manifest.

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
