Title: Know Thyself. Automatically Check Spelling and Grammar on Git Commits
Date: 2025-05-17 16:30:00 MST
Category: Development
Tags: go, git
Slug: pre-commit-hooks-spell-grammar
Authors: Marc Leonard
Summary: Use pre-commit hooks to automatically check spelling and grammar in your code.

I work very hard to write clean concise comments. I will toil over them, read, re-read, and re-read again. Even still - I am terrible at catching my own spelling and grammar mistakes. 
I've recently gotten sick of other people spending time in code review fixing my mistakes. I know that I can do better, and I want to be better. So like any good developer - lets automate it!

This is my setup using `pre-commit`, `aspell`, and `languagetool` to automatically check spelling and grammar **only in the changed lines** of `*.go` and `*.md` files when committing code.

---

## 🛠 Tools Used

- [`pre-commit`](https://pre-commit.com): Git hook manager
- [`aspell`](http://aspell.net/): Spell checker
- [`languagetool`](https://languagetool.org/): Grammar checker (CLI required)

These tools integrate cleanly into your local development workflow without linting untouched lines or scanning the entire codebase.

---

## 📁 Project Structure

Below is a simplified version of my repository layout:

```
your-repo/
├── .git/
├── .pre-commit-config.yaml  
├── hooks/           
│   ├── smart_spellcheck.sh
│   └── smart_grammar_check.sh
├── main.go
└── README.md
```

---

## ⚙️ .pre-commit-config.yaml

```yaml
repos:
  - repo: local
    hooks:
      - id: smart-spellcheck
        name: Smart Spell Check (diff-only)
        entry: .hooks/smart_spellcheck.sh
        language: system
        pass_filenames: false

      - id: smart-grammar-check
        name: Smart Grammar Check (diff-only)
        entry: .hooks/smart_grammar_check.sh
        language: system
        pass_filenames: false
```

---

## ✏️ `hooks/smart_spellcheck.sh`

```bash
#!/bin/bash

# Get changed lines from staged files
FILES=$(git diff --cached --name-only --diff-filter=ACMR | grep -E '\.(go|md)$')

HAS_ERRORS=0

for FILE in $FILES; do
  if [ -f "$FILE" ]; then
    # Extract added or changed lines (without + at beginning)
    git diff --cached -U0 "$FILE" | \
      grep '^+[^+]' | \
      sed 's/^+//' > /tmp/spell_lines.txt

    if [ -s /tmp/spell_lines.txt ]; then
      echo "🔍 Checking spelling in changed lines of $FILE..."

      # Run aspell and collect misspelled words
      MISSPELLED=$(cat /tmp/spell_lines.txt | aspell list | sort | uniq)

      if [[ -n "$MISSPELLED" ]]; then
        echo "❌ Misspelled words in $FILE:"
        echo "$MISSPELLED"
        HAS_ERRORS=1
      fi
    fi
  fi
done

exit $HAS_ERRORS
```

---

## 📝 `hooks/smart_grammar_check.sh`

```bash
#!/bin/bash

if ! command -v languagetool >/dev/null 2>&1; then
  echo "⚠️  LanguageTool CLI not found. Skipping grammar check."
  exit 0
fi

FILES=$(git diff --cached --name-only --diff-filter=ACMR | grep -E '\.(go|md)$')

HAS_ERRORS=0

for FILE in $FILES; do
  if [ -f "$FILE" ]; then
    git diff --cached -U0 "$FILE" | \
     grep '^+[^+]' | \
     sed 's/^+//' > /tmp/grammar_lines.txt

    if [ -s /tmp/grammar_lines.txt ]; then
      echo "📝 Checking grammar in changed lines of $FILE..."
      languagetool --language en-US /tmp/grammar_lines.txt || HAS_ERRORS=1
    fi
  fi
done

exit $HAS_ERRORS
```

---

## ✅ Usage

To set it up:

1. Install `pre-commit`:
   ```bash
   pip install pre-commit
   ```

2. Install the hooks:
   ```bash
   pre-commit install
   ```

3. Manually test:
   ```bash
   pre-commit run --all-files
   ```

---

## ✨ Result

Now when I try to commit changes, these hooks run automatically and alert me if I’ve introduced spelling or grammar mistakes — without touching the rest of the file.

It’s a simple setup, but it’s already helping keep my commits a little more polished. Hope it helps you too!
