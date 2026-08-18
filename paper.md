---
title: 'signal-engine: an open-source reference implementation of GitHub engineering-velocity signals for startup deal-flow research'
tags:
  - Python
  - venture capital
  - alternative data
  - GitHub API
  - startup signals
  - deal-flow
authors:
  - name: Maryan Kindrat
    orcid: 0009-0002-2222-4112
    corresponding: true
    affiliation: 1
affiliations:
 - name: Independent Researcher
   index: 1
date: 18 August 2026
bibliography: paper.bib
---

# Summary

`signal-engine` is a small, dependency-light Python package that turns public GitHub activity into quantitative acceleration signals for startup organizations. Given a GitHub organization name, it computes three leading indicators: commit velocity over a rolling 14-day window, contributor growth over a 30-day window, and new public repository creation over a 30-day window. It then combines these into a single composite score on a 0-100 scale, classifies the dominant acceleration pattern into one of four human-readable types, and estimates the organization's financing stage.

The package is the open-source computation layer behind GitDealFlow, a deal-flow product that tracks engineering activity across 350+ startup organizations in 15 sectors. The computation is deliberately published in full: the methodology is documented in a preprint (SSRN 6606558) and the underlying panel dataset is released under CC BY 4.0 (Zenodo, DOI 10.5281/zenodo.19650920). The project's design principle is that a signal nobody can audit is a signal nobody should bet on.

# Statement of need

Early-stage investors face an extreme information asymmetry: the startups that are about to raise are usually the ones whose internal momentum is least visible externally. Most deal-flow tools rely on funding announcements, founder networks, or self-reported metrics, all of which lag or can be gamed. Public engineering activity on GitHub is observable before most fundraise announcements, updates at high frequency, and is comparatively hard to fabricate at scale.

Existing software in this space falls into two camps. Commercial platforms (PitchBook, CB Insights, Dealroom) provide proprietary signals behind closed scoring methodologies, which makes them unsuitable for reproducible research. Academic tools for analyzing GitHub data focus on project-level health or developer productivity, not on organization-level acceleration as a leading indicator of financing events.

`signal-engine` fills the gap between these two: an open, auditable, deterministic implementation of organization-level engineering acceleration signals, designed to be run by a single researcher on a laptop with a free GitHub API token. Its target users are academic researchers studying alternative data in venture finance, quantitative scouts at early-stage funds, and founders who want the same view of their own organization.

# State of the field

The closest general-purpose tools are GitHub API client libraries such as PyGithub, which provide access to raw endpoints but no derived signals. Packages that compute acceleration-style metrics are usually tied to a specific study and are not maintained as reusable software. To our knowledge, no open-source package computes this specific combination of rolling commit velocity, contributor growth, and repository creation with a documented link to a published panel.

A deliberate design choice was to build rather than contribute: the signal definitions, window lengths, and composite weights are specific to the published methodology (SSRN 6606558), and general-purpose clients are not opinionated enough to encode them. The package is small by design (roughly 1,300 lines), with a single runtime dependency (`requests`), so that a reviewer can read the entire computation in one sitting. The live product and the open computation layer share the same formulas; the product adds the pipeline, coverage, and data feed.

# Software design

The package is organized as two classes plus pure functions.

`GitHubClient` wraps the GitHub REST API v3 with rate-limit awareness (respects `X-RateLimit` headers and waits when the limit is near), retry with backoff, pagination through the `Link` header, and handling of the lazily computed `/stats/*` endpoints that return `202 Accepted` on first request. This matters in practice: GitHub computes commit statistics on demand, and a naive client either fails or blocks without explanation.

`SignalEngine` implements the pipeline. For a given organization it selects the most active public repository, then computes three signals. Commit velocity uses the `stats/commit_activity` endpoint (52 weekly buckets); two consecutive weeks are summed to produce 14-day figures, and the fractional change against the prior 14-day window is the acceleration measure. Contributor growth uses the contributors endpoint with a 30-day window. New repository creation counts public repos created in the last 30 days.

The composite score is a weighted sum: velocity change 0.40, contributor growth 0.30, new repo creation 0.20, and contributor diversity (1 minus the Gini coefficient) 0.10. The Gini coefficient is computed on the top contributor counts and captures whether work is concentrated in one or two people. The design encodes a specific published finding: organizations with 14-day velocity acceleration and low contributor concentration (Gini below 0.30) were 3.4x more likely to announce a Series A within 60 days in a panel of 219 confirmed rounds.

Design trade-offs worth noting. First, the package prefers a small number of carefully chosen endpoints over exhaustive crawling, trading coverage for determinism and rate-limit safety. Second, edge cases are handled explicitly and documented: a zero-value prior window returns a bounded +100% change instead of infinity, and an organization with no activity receives the maximum Gini penalty so that dead repositories never earn the diversity bonus. Third, pure computation functions are separated from network I/O so the test suite runs offline with no token, and so reviewers can verify the math independently of the API.

# Research impact statement

The software is the reference implementation of the methodology described in a preprint (SSRN 6606558). The companion dataset is published under CC BY 4.0 with a Zenodo DOI (10.5281/zenodo.19650920) and is mirrored on Kaggle and Data.world. The panel comprises 219 confirmed fundraise observations across venture-backed startups, spanning five quarters, and the preprint reports descriptive statistics on rolling 14-day commit velocity (median 71, mean 173, 90th percentile 392) and quarter-over-quarter velocity change (range -94% to +1,647%).

The software is also in continuous production use as the computation layer of GitDealFlow, which tracks 350+ startup organizations across 15 sectors with weekly baselines and a Sunday digest. This gives the project an unusual property for a research artifact: the published code is the same code that runs in production, so any discrepancy between the published computation and the live product would be immediately visible to users.

# AI usage disclosure

Generative AI tools (large language models) were used in the development of this software and in the drafting of this paper. Specifically: AI assistance was used for code scaffolding, unit test drafting, documentation, and copy-editing of the paper text. The human author made all core design decisions (signal definitions, window lengths, composite weights, edge-case semantics), reviewed and edited every AI-assisted output, and validated the computation logic against the published panel results. All claims in this paper were verified by the author against the repository code, the preprint, and the live API before submission.

# Acknowledgements

No external funding was received. The author thanks the maintainers of the GitHub REST API and the open-source community whose public engineering activity makes this line of research possible.

# References
