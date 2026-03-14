# Infonomics Multi-Agent Research System

A PhD-level deep research system for infonomics and information economics, powered entirely by Claude Code. **No external API calls, no extra costs** — Claude Code itself acts as the multi-agent system.

## How It Works

Claude Code adopts specialist roles sequentially to conduct rigorous research:

```
                    ┌─────────────────┐
                    │   Claude Code   │
                    │  (Orchestrator) │
                    └────────┬────────┘
                             │ adopts each role in sequence
              ┌──────────────┼──────────────┐
              │              │              │
    ┌─────────▼──────┐ ┌────▼─────┐ ┌──────▼───────┐
    │  Literature     │ │ Theorist │ │ Synthesizer  │
    │  Reviewer       │ │          │ │              │
    └────────────────┘ └──────────┘ └──────────────┘
                             │
                      ┌──────▼──────┐
                      │   Critic    │◄─── Adversarial
                      │ (Devil's    │     Review Loop
                      │  Advocate)  │
                      └─────────────┘
```

**Pipeline:**
1. **Literature Reviewer** — surveys existing research, identifies key papers, gaps, debates
2. **Theorist** — develops theoretical frameworks and models informed by the literature
3. **Critic** — adversarially reviews findings for logical gaps, methodological issues, assumptions
4. If critique score < 0.7 → **Theorist** refines (max 2 rounds)
5. **Synthesizer** — integrates into publication-quality output

## Usage

Just talk to Claude Code:

```
"Research the economic implications of data non-rivalry for marketplace design"
"What does the literature say about Shapley value approaches to data valuation?"
"Develop a theoretical framework for information asymmetry in AI training data markets"
```

Claude Code will work through the full pipeline and save structured outputs.

## Project Structure

```
CLAUDE.md                    # Operating manual — how Claude Code runs the system
src/
├── models.py                # Pydantic models for findings, citations, critiques
├── session.py               # Save/load research sessions as JSON
├── viewer.py                # CLI viewer for past sessions
├── templates/               # Role prompt templates (reference)
│   ├── literature_reviewer.md
│   ├── theorist.md
│   ├── critic.md
│   └── synthesizer.md
data/
├── outputs/                 # Research session outputs (JSON)
├── knowledge_base/          # Accumulated cross-session knowledge
```

## Key Design Decisions

- **No external API calls** — Claude Code is the LLM, zero extra cost
- **Structured persistence** — all research outputs saved as typed JSON via Pydantic
- **Adversarial rigor** — Critic role ensures PhD-level standards before synthesis
- **Audit trail** — every role's output is saved for reproducibility
- **Cross-session memory** — knowledge base accumulates across research sessions
