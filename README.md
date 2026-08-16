# signal-engine

<div align="center">

**Open-source reference implementation of the GitHub commit-velocity acceleration signal.**

*The computation is open. The live data feed is not.*

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![DOI](https://img.shields.io/badge/SSRN-6606558-8a2be2)](https://ssrn.com/abstract=6606558)
[![DOI](https://img.shields.io/badge/Zenodo-10.5281%2Fzenodo.19650920-168363)](https://doi.org/10.5281/zenodo.19650920)
[![License: CC BY 4.0](https://img.shields.io/badge/Dataset-CC%20BY%204.0-lightgrey)](https://creativecommons.org/licenses/by/4.0/)

</div>

---

## What this is

`signal-engine` is the open-source **computation layer** of [GitDealFlow](https://gitdealflow.com), a deal-flow signal product that reads public GitHub engineering activity and surfaces the startups accelerating **21–47 days before they announce a fundraise**.

Given a GitHub organization, it computes three leading indicators and combines them into a single ranked score:

| # | Signal | Window | What it measures |
|---|--------|--------|------------------|
| 1 | **Commit velocity** | 14 days | Total commits to the org's most active public repo, and the *change* vs. the prior 14 days |
| 2 | **Contributor growth** | 30 days | Unique contributor count and its growth rate — a proxy for team expansion |
| 3 | **New repo creation** | 30 days | Burst of new public repos — infrastructure buildout, new product lines |

Plus the composite predictor that produced the headline finding in the SSRN panel:

> **"14-day commit-velocity acceleration × low top-contributor concentration (Gini < 0.30)"**
> → orgs meeting both conditions were **3.4× more likely** to announce a Series A within 60 days.

The methodology is fully documented and peer-reviewable:

- **Paper:** [*A Longitudinal Panel of GitHub Engineering Velocity for Venture-Backed Startups*](https://ssrn.com/abstract=6606558) — SSRN abstract `6606558`, DOI `10.2139/ssrn.6606558`
- **Dataset:** DOI `10.5281/zenodo.19650920`, CC BY 4.0
- **Author:** The Data Nerd — [ORCID `0009-0002-2222-4112`](https://orcid.org/0009-0002-2222-4112), [Wikidata Q139376302](https://www.wikidata.org/wiki/Q139376302)
- **Live walkthrough:** [commit-velocity methodology](https://signals.gitdealflow.com/methodology)

---

## Why open-source the code?

Three reasons, in order of honesty:

1. **Reproducibility is the moat.** A signal you can't audit is a signal you shouldn't bet on. The SSRN panel (`n=219` confirmed rounds) is only persuasive if anyone can re-derive the numbers. This repo is that guarantee.

2. **The edge was never the arithmetic.** The math here is ~200 lines of Python. The hard, expensive part — and the actual product — is the *pipeline*: tracking 350+ orgs, 15 sectors, weekly, with historical baselines, sector rankings, and a Sunday digest. Open-sourcing the formula doesn't give away the factory; it proves the factory makes what the label says.

3. **The category wins when the method is public.** "Code-Side Sourcing" only becomes a real sourcing channel if the methodology is transparent enough to be discussed, cited, and reproduced. This repo is the category's open handshake.

**In short:** open-source the computation, gate the live data feed. You can run this on your own watchlist with your own compute for free, forever. When you'd rather not maintain the pipeline, the continuously-refreshed feed is at [the live deal-flow signal](https://gitdealflow.com).

---

## Installation

Requires **Python 3.10+** and a free GitHub API token (read-only is enough).

```bash
git clone https://github.com/kindrat86/gitdealflow-signal-engine.git
cd gitdealflow-signal-engine

python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

`requirements.txt` is a single dependency:

```text
requests>=2.31.0
```

Set your token:

```bash
export GITHUB_TOKEN=ghp_xxxxxxxx          # macOS / Linux
# or: set GITHUB_TOKEN=ghp_xxxxxxxx       # Windows (cmd)
```

> Fine-grained PATs work too — grant **read-only** access to public repositories.

---

## Quick start

```python
from signal_engine_core import GitHubClient, SignalEngine

engine = SignalEngine(GitHubClient())   # reads GITHUB_TOKEN from env

report = engine.analyze_org("vercel")
print(report.to_dict())
```

Or from the command line:

```bash
python signal_engine_core.py vercel
python signal_engine_core.py vercel anthropics supabase  # watchlist mode
```

Real output from a live run (August 13, 2026 — numbers shift weekly):

```
=== vercel ===
  Most active repo:        next.js
  Commit velocity (14d):   225 commits
  Velocity change:         -22.7%
  Contributors (30d):      36
  Contributor growth:      +100.0%
  New repos (30d):         2
  Gini (diversity):        0.967
  Composite score:         48.0/100
  Signal type:             Engineering Hiring Burst
  Estimated stage:         series-a-b
  Series-A composite hit:  False
```

> **Note on first runs:** GitHub computes `/stats/*` endpoints lazily — the first
> query against a repo returns `202 Accepted` while GitHub crunches the data, and
> the client waits and retries automatically. A cold 3-org watchlist can take a
> few minutes; subsequent runs are fast because GitHub caches the stats.
>
> Also note: a mature public company like Vercel scores mid-range by design —
> the composite rewards *acceleration from a baseline*, not absolute size. The
> interesting names are small orgs whose velocity just inflected.

---

## API reference

### `GitHubClient`

| Method | Description |
|--------|-------------|
| `GitHubClient(token=None, base_url=..., timeout=20.0)` | Authenticated, rate-limit-aware client. Reads `GITHUB_TOKEN` if `token` omitted. |
| `.get(path, params=None)` | Single GET with retry + backoff, respects `X-RateLimit-*` headers, returns `None` on 404. |
| `.get_all_pages(path, params=None)` | Follows `Link` pagination, returns a flattened list. |

### `SignalEngine`

| Method | Returns | Description |
|--------|---------|-------------|
| `analyze_org(org)` | `SignalReport` | Full pipeline for one org: picks most-active repo, computes all three signals + composite, classifies signal type, estimates stage. |
| `analyze_watchlist(orgs)` | `List[SignalReport]` | Runs the pipeline across many orgs, sorted by composite score (descending). |
| `commit_velocity(activity, window_days=14)` | `(current, prior, change)` | 14-day rolling commit count vs. prior 14-day window. |
| `contributor_growth(totals, window_days=30)` | `(now, prior, growth)` | Unique-contributor count and growth rate. |
| `new_repo_count(repos, window_days=30)` | `int` | Public repos created in the last 30 days. |
| `composite_score(vc, cg, nr, gini)` | `float` | Weighted 0–100 score (see weights below). |
| `classify_signal(vc, cg, nr)` | `str` | One of the four published signal types. |
| `estimate_stage(contributor_count)` | `str` | `pre-seed` / `seed` / `series-a-b` / `growth`. |

**Composite weights** (defaults, overridable in `signal-engine-core.py`):

| Component | Weight |
|-----------|--------|
| Commit velocity change | 0.40 |
| Contributor growth | 0.30 |
| New repo creation | 0.20 |
| Contributor diversity (1 − Gini) | 0.10 |

---

## The three signals, in code

### 1. Commit velocity (14-day window)

```python
activity = engine.get_commit_activity("vercel", "next.js")
current, prior, change = engine.commit_velocity(activity, window_days=14)
# current = commits in the last 14 days
# prior   = commits in the preceding 14 days
# change  = fractional change, e.g. 1.524 == +152.4%
```

GitHub's `stats/commit_activity` endpoint returns up to **52 weekly buckets**; two consecutive weeks are summed to produce each 14-day figure. This is the "shipping at an unusually high rate" signal.

### 2. Contributor growth (30-day window)

```python
totals = engine.get_contributor_counts("vercel", "next.js")
now, prior, growth = engine.contributor_growth(totals, window_days=30)
# now    = unique contributors active in the last 30 days
# growth = fractional change, e.g. 0.68 == +68%
```

A rising contributor count is the "team is scaling" signal — historically a leading indicator of funding or product-market fit.

### 3. New repo creation (30-day window)

```python
repos = engine.list_org_repos("vercel")
new_repos = engine.new_repo_count(repos, window_days=30)
# new_repos = public repos created in the last 30 days
```

A burst of new repos (≥ 3 in 30 days) signals infrastructure buildout, SDK releases, or framework migration.

---

## Signal classification

Each org is bucketed into one of four signal types based on the **dominant** driver:

| Signal type | Trigger |
|-------------|---------|
| **Engineering Hiring Burst** | Contributor growth ≥ +50% |
| **Infrastructure Buildout** | ≥ 3 new repos in 30 days |
| **Deploy Frequency Spike** | Commit velocity change ≥ +150% |
| **Framework Migration** | General acceleration that doesn't fit the above |

Stage is estimated from contributor count: **pre-seed** (1–7), **seed** (8–19), **series-a-b** (20–49), **growth** (50+). This is a rough proxy — not all contributors are employees, and not all employees push to public repos.

---

## Running your own watchlist

```python
from signal_engine_core import GitHubClient, SignalEngine

engine = SignalEngine(GitHubClient())

watchlist = [
    "vercel", "anthropics", "supabase", "modal-labs", "replicate",
    "langchain-ai", "dust-tt", "mistralai", "huggingface", "charmbracelet",
]

for r in engine.analyze_watchlist(watchlist):
    print(f"{r.org:20s} {r.composite_score:5.1f}/100  {r.signal_type}")
```

Sort by `composite_score`, then look at **`meets_series_a_composite`** — that flag encodes the velocity-acceleration × diversity condition from the 3.4× finding.

> **Rate limits:** unauthenticated requests to the GitHub API allow ~60 requests/hour; an authenticated token raises that to **5,000/hour**. A 10-org watchlist makes roughly 30–50 API calls, comfortably inside either quota.

---

## How this maps to the paid Dashboard

| This repo (open) | GitDealFlow Dashboard (paid) |
|------------------|------------------------------|
| You supply the org names | 350+ tracked orgs across 15 sectors |
| You run it on your compute | Continuously refreshed, weekly (Monday) |
| Raw numbers + composite score | Sector rankings, historical baselines, quarters |
| You interpret the output | Plain-English notes: *why* each org is moving |
| You backtest yourself | 219 documented fundraises, validated against the SSRN panel |
| No alerting | Sunday digest: 5 named startups, every week |

The formula is the same. The product is the pipeline, the coverage, and the ongoing backtest — plus the time you'd otherwise spend babysitting rate limits and stale baselines.

---

## License

The **code** in this repository is [MIT](./LICENSE).

The **dataset and methodology** are published separately under **CC BY 4.0** ([Zenodo: 10.5281/zenodo.19650920](https://doi.org/10.5281/zenodo.19650920)). You may use both freely with attribution.

---

## Citation

If you use this code or the underlying methodology in your own research or writing:

```bibtex
@misc{thedatanerd2026longitudinal,
  author       = {The Data Nerd},
  title        = {A Longitudinal Panel of GitHub Engineering Velocity for
                  Venture-Backed Startups: Dataset and Early Observations},
  year         = {2026},
  doi          = {10.2139/ssrn.6606558},
  publisher    = {SSRN},
  note         = {Preprint, SSRN abstract 6606558},
  orcid        = {0009-0002-2222-4112},
  url          = {https://ssrn.com/abstract=6606558}
}
```

---

## Contributing

Pull requests are welcome — especially fixes to the computation, additional signal types, or better tests.

1. Fork the repo and create a branch: `git checkout -b fix/your-change`
2. Make your change and add a test where relevant.
3. Keep the math honest: this repo is a reproducibility guarantee, so any change to the scoring logic should be justified against the SSRN panel.
4. Open a PR with a clear description.

Questions, ideas, or a backtest result that surprised you? Open an [issue](https://github.com/kindrat86/gitdealflow-signal-engine/issues) or drop a note via [GitDealFlow](https://gitdealflow.com).

---

<div align="center">

**Want the live data feed without building it yourself?**

<br>

[**→ GitDealFlow**](https://gitdealflow.com)

Free Sunday digest · €49/mo Dashboard · €197/mo Insider Circle

*Track 350+ orgs across 15 sectors. Get the five names worth a meeting, every week.*

</div>
