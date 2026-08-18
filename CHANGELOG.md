# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-08-18

### Added

- Initial public release of the open-source signal computation layer.
- `GitHubClient`: authenticated, rate-limit-aware GitHub API client with retry/backoff, pagination, and lazy `/stats/*` endpoint handling.
- `SignalEngine`: full pipeline computing three leading indicators from public GitHub data:
  - Commit velocity (14-day window, change vs. prior window)
  - Contributor growth (30-day window)
  - New repo creation (30-day window)
- Composite 0-100 score (velocity change 0.40, contributor growth 0.30, new repos 0.20, diversity 0.10).
- Signal classification into four published types (Engineering Hiring Burst, Infrastructure Buildout, Deploy Frequency Spike, Framework Migration).
- Stage estimation (pre-seed / seed / series-a-b / growth).
- `meets_series_a_composite` flag encoding the velocity x diversity condition from the SSRN panel.
- Unit tests (no network or token required) for the pure computation functions.
- CLI: `python signal_engine_core.py <org> [org2 ...]`.
- RePEc archive templates (ReDIF) for the SSRN paper.
