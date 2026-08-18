# Contributing

Thank you for considering a contribution to `signal-engine`.

This repository is a **reproducibility guarantee**: the computation behind the
published SSRN methodology (abstract 6606558) is open so that anyone can audit,
re-derive, and extend it. That purpose shapes every contribution.

## Ground rules

1. **Keep the math honest.** Any change to the scoring logic must be justified
   against the published panel (n=219 confirmed rounds, SSRN 6606558). If your
   change alters the composite weights, the signal windows, or the Gini
   handling, explain in the PR description how it affects the published
   findings.
2. **Prefer additive changes.** New signal types and new utilities are welcome.
   Changes that silently alter the output of the three published signals need
   a stronger justification than changes that add functionality.
3. **Tests are mandatory.** Pure computation functions must ship with unit
   tests. The test suite runs without network access and without a token:
   `pytest -q`.
4. **No claim inflation.** The repo tracks 350+ orgs / 15 sectors in the live
   product. Do not introduce larger coverage numbers anywhere in the code,
   README, or documentation.

## Getting started

```bash
git clone https://github.com/kindrat86/gitdealflow-signal-engine.git
cd gitdealflow-signal-engine
python -m venv .venv && source .venv/bin/activate
pip install -e .
pytest -q
```

## Submitting a change

1. Fork the repo and create a branch: `git checkout -b fix/your-change`.
2. Make your change and add a test where relevant.
3. Run the full test suite: `pytest -q`.
4. Keep the math honest (see ground rules).
5. Open a PR with a clear description of the change and its justification.

## Reporting issues

Open an [issue](https://github.com/kindrat86/gitdealflow-signal-engine/issues)
with:

- What you expected to happen.
- What actually happened (include the org name and, if possible, the raw API
  response that misled you).
- The version of the package and Python you are using.

## Support expectations

This project is maintained by the GitDealFlow team. Issues and PRs are
reviewed, but response times are not guaranteed. The live data feed
(GitDealFlow dashboard) is a separate, paid product; this repository covers
only the open computation layer.
