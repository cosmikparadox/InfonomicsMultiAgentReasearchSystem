# Infonomics Multi-Agent Research System

A multi-agent system for PhD-level deep research in infonomics and information economics, powered by Anthropic Claude.

## Architecture

```
                    ┌─────────────────┐
                    │   Orchestrator   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
    ┌─────────▼──────┐ ┌────▼─────┐ ┌──────▼───────┐
    │  Literature     │ │ Theorist │ │ Synthesizer  │
    │  Reviewer       │ │          │ │              │
    └────────────────┘ └──────────┘ └──────────────┘
                             │
                      ┌──────▼──────┐
                      │   Critic    │◄─── Adversarial
                      │             │     Review Loop
                      └─────────────┘
```

**Pipeline:**
1. **Literature Reviewer** surveys existing research, identifies key papers, gaps, and debates
2. **Theorist** develops theoretical frameworks and formal models informed by the literature
3. **Critic** adversarially reviews all findings for logical gaps, methodological issues, and unstated assumptions
4. If the critique score is below threshold, the **Theorist** refines its analysis (up to N rounds)
5. **Synthesizer** integrates all findings into a coherent, publication-quality output

## Setup

```bash
# Clone and install
pip install -e ".[dev,research]"

# Configure
cp .env.example .env
# Edit .env with your Anthropic API key
```

## Usage

```bash
# Run a research query
research "How should organizations value their data assets using infonomics frameworks?"

# With additional context
research "What is the economic impact of data marketplaces?" "Focus on healthcare data"
```

## Project Structure

```
src/
├── core/
│   ├── types.py          # Pydantic models: Finding, Citation, CritiquePoint, etc.
│   └── agent.py          # BaseAgent class with Claude API integration
├── agents/
│   ├── orchestrator.py   # Pipeline coordinator with critique loop
│   ├── literature_reviewer.py
│   ├── theorist.py
│   ├── critic.py
│   └── synthesizer.py
├── config/
│   └── settings.py       # Pydantic settings from .env
├── tools/                # Extensible tools for agents (web search, data analysis, etc.)
└── cli.py                # CLI entry point
```

## Extending

- **Add new agent types**: Subclass `BaseAgent`, implement `system_prompt()` and `parse_response()`
- **Add tools for agents**: Place in `src/tools/` (e.g., web search, database queries, API calls)
- **Customize the pipeline**: Modify `Orchestrator.run()` to add/reorder phases
- **Swap models**: Configure per-agent models in `.env` for cost/quality tradeoffs

## Design Principles

- **No framework bloat**: Direct Anthropic SDK usage for full control and transparency
- **Structured I/O**: Pydantic models for every agent interaction, enabling validation and serialization
- **Adversarial rigor**: The Critic agent ensures findings meet PhD-level standards before synthesis
- **Audit trail**: Every agent call is logged and saved, supporting reproducibility
- **Extensible**: Clean base classes make it easy to add domain-specific agents
