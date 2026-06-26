# AI System Design Handbook

A Staff-level, production-focused reference for AI System Design — LLM architecture, RAG, agents, AI infrastructure, LLMOps, security, and 20 full system-design case studies (ChatGPT, Claude, Perplexity, Cursor, Glean, and more). Published as a GitHub Pages site with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

**Live site:** https://gyanendrachaubey.github.io/AI-System-Design-Notes/

This is not a machine learning theory resource — no linear regression, no CNN derivations. It's about how production AI systems are actually architected, scaled, evaluated, secured, and paid for, at the depth expected in a Staff Engineer design review or an AI System Design interview.

## Status

Under active construction. Every topic in the full curriculum already has a page (nothing 404s), but content is at one of two depths — see [BACKLOG.md](BACKLOG.md) for the exact, current list:

- **✅ Flagship** — full depth: all required sections, 5 Mermaid diagrams, concrete numbers, answered interview questions.
- **📋 Stub** — a real synopsis and outline, expanded in a future pass.

## Local development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve       # http://127.0.0.1:8000
```

`mkdocs build --strict` is the CI-equivalent check — it fails on broken nav references or malformed Markdown/Mermaid.

## Adding or expanding a chapter

- New chapters: copy `templates/chapter-template.md`. New case studies: copy `templates/case-study-template.md`. Both encode the required section list and the 5 mandatory Mermaid diagrams.
- Stub pages (and the per-section `index.md` landing pages) are generated from a single manifest in `scripts/new_stub.py`. To change a stub's synopsis/outline or mark a page flagship-complete, edit the `SECTIONS` list there and re-run `python3 scripts/new_stub.py` — it also regenerates `BACKLOG.md` from the same source of truth.

## Deployment

Pushing to `main` triggers `.github/workflows/deploy.yml`, which builds the site and publishes it to the `gh-pages` branch via `mkdocs gh-deploy`. GitHub Pages must be configured (once) to serve from that branch.