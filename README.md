# infra-im-harness

Verification gates for infrastructure project finance.

An AI can draft a convincing information memorandum in minutes. Convincing is not the same as checked. The skills in this repository do not write the memo for you. They attack a draft's numbers and logic until nothing is left in it that its author cannot defend.

```
draft ──▶ gates attack ──▶ author rules ──▶ fix, then run the gates again
```

## The gates

| Skill | The question it forces |
|---|---|
| [`im-skeleton`](.claude/skills/im-skeleton/SKILL.md) | Which section must pass which gate? (It builds empty slots, never filled-in numbers.) |
| [`deal-thesis-gate`](.claude/skills/deal-thesis-gate/SKILL.md) | Who pays this return, and why? Is any cost line missing, or set to zero without a reason? |
| [`assumption-trace`](.claude/skills/assumption-trace/SKILL.md) | What is the primary source and base year of every input? |
| [`stress-gate`](.claude/skills/stress-gate/SKILL.md) | Was the base case chosen because it looked good? Does debt service survive the downside? |
| [`model-audit`](.claude/skills/model-audit/SKILL.md) | Does an independent re-computation from the same assumptions give the same answer? |
| [`risk-allocation-matrix`](.claude/skills/risk-allocation-matrix/SKILL.md) | Who carries each risk, through which contract, and which risks have no owner at all? |
| [`im-parity`](.claude/skills/im-parity/SKILL.md) | Do the memo, the model and the assumption sheet still agree after the last edit? |

Every skill ends with a section on **the failures it exists to catch**. None of them are hypothetical. Each one is a mistake that was actually made while building the sample project below, and caught by the gate that now carries its name.

The skill files and the sample are written in Korean, because the market data, regulations and sources they work with are Korean.

## Sample: a 1 MW ground-mount solar plant

[`samples/solar-1mw/`](samples/solar-1mw/) is a hypothetical project built only from public data.

- [`IM.md`](samples/solar-1mw/IM.md) is the memo draft, with each section marked by the gate it has to pass.
- [`assumptions.md`](samples/solar-1mw/assumptions.md) traces every input to its primary source, and records each conflict between sources and how it was resolved.
- [`gate-log.md`](samples/solar-1mw/gate-log.md) lists what each gate caught and what changed as a result.
- [`model_check.py`](samples/solar-1mw/model_check.py) re-computes the model independently, to audit the hand-built spreadsheet.

One conclusion the gates overturned:

> The first model said the tightest debt-service year would come late, around year 15, after panel degradation had compounded. That holds for level annuity repayment. The actual bank product only allowed equal-principal repayment, and under that structure the tightest year is **year 1**, when interest is highest (minimum DSCR 1.26). Changing nothing but the repayment structure moves equity IRR between 16.1% and 18.3%, while project IRR stays at 8.6%. The plant earns the same cash either way. Only the timing of who gets paid changes.

## Usage

Open the repository in [Claude Code](https://claude.com/claude-code). The skills under `.claude/skills/` are picked up automatically.

```bash
python samples/solar-1mw/model_check.py
```

## Rules

- Hypothetical projects and public data only.
- Spreadsheet models are built by hand. Code only checks them.
- When two sources disagree and the difference can't be explained, the number is dropped rather than picked.
