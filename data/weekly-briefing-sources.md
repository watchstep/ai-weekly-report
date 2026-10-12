# Weekly AI Briefing Source Guide

Updated: 2026-10-12 (Asia/Seoul)
Companion feed list: [data/ai-feeds.opml](./ai-feeds.opml)

## Purpose

Provide a stable source policy for a Korean-language weekly ChatGPT briefing about significant AI releases, AI developer tooling, papers, safety/alignment research and AI industry developments. This file is a *source guide*, not a guarantee that ChatGPT will fetch every RSS item.

The existing OPML remains the collection registry for the Python RSS pipeline. All 37 existing feed URLs are retained. A non-RSS Threads account is listed for manual/web-search monitoring without being passed to feedparser.

## Priority order

### P1. Official announcements and release notes (verify at original source)

- [OpenAI News](https://openai.com/news) — models, APIs, product announcements
- [Anthropic News](https://www.anthropic.com/news) and [Engineering](https://www.anthropic.com/engineering) — Claude models, agents, evaluations and tools
- [Google DeepMind Blog](https://deepmind.google/discover/blog/) and [Google AI Blog](https://blog.google/technology/ai/) — Gemini models and research
- [Meta AI Blog](https://ai.meta.com/blog/) — open models and research
- [Hugging Face Blog](https://huggingface.co/blog) — models, datasets, evaluation and tooling
- [Microsoft Research](https://www.microsoft.com/en-us/research/) — model research and agent systems
- [NVIDIA Blog](https://blogs.nvidia.com/) — AI infrastructure, inference and tooling
- [LangChain Blog](https://blog.langchain.dev/) — agent and developer framework releases
- [AWS News Blog](https://aws.amazon.com/blogs/aws/) — developer infrastructure and cloud AI

When there is a conflict between an original announcement and coverage in another publication, use the original.

### P2. Research and papers (verify papers, release dates and claims)

- [arXiv cs.AI](https://arxiv.org/list/cs.AI/recent)
- [Berkeley BAIR](https://bair.berkeley.edu/blog/)
- [Stanford AI](https://ai.stanford.edu/blog/)
- [MIT AI News](https://news.mit.edu/topic/artificial-intelligence2)
- [ML@CMU](https://blog.ml.cmu.edu/)
- [Ai2](https://allenai.org/blog)
- [Microsoft Research](https://www.microsoft.com/en-us/research/)

For important work in LLM alignment/safety, evaluations and agent reliability, review the primary paper or project repository. Note that a new arXiv preprint is not automatically peer reviewed.

### P3. Specialist news and synthesis (use for discovery, then verify)

- [The Decoder](https://the-decoder.com/)
- [VentureBeat AI](https://venturebeat.com/category/ai/)
- [IEEE Spectrum](https://spectrum.ieee.org/artificial-intelligence)
- [InfoQ AI/ML/Data Engineering](https://www.infoq.com/ai-ml-data-eng/)
- [Last Week in AI](https://lastweekin.ai/)
- [Latent Space](https://www.latent.space/)
- [SemiAnalysis](https://www.semianalysis.com/)

### P4. Community and Korean perspectives (discovery only unless first-hand)

- [GeekNews](https://news.hada.io/)
- [AI Matters](https://aimatters.co.kr/)
- [PyTorch KR](https://discuss.pytorch.kr/)
- [r/MachineLearning](https://www.reddit.com/r/MachineLearning/)
- [r/artificial](https://www.reddit.com/r/artificial/)
- [r/deeplearning](https://www.reddit.com/r/deeplearning/)

Other feeds in the OPML may supplement coverage. A source not appearing in this shortlist is not deleted or banned.

## Social account watchlist (not a verified RSS source)

- [Threads @choi.openai](https://www.threads.com/@choi.openai) — independent AI news/updates discovery source. **Do not treat this account as an official OpenAI account.**
  - Search or inspect public posts that fall within the briefing period if accessible.
  - Verify each material claim using the corresponding vendor announcement, research paper, official documentation, or reliable reporting.
  - Cite the original claim source in the main briefing; add the relevant Threads post link when accessible.
  - Threads does not provide a verified first-party profile RSS endpoint for this source. A third-party RSSHub route such as `/threads/choi.openai` is only a candidate and has **not been verified to work**. Do not insert a fabricated or untested RSS URL into the collection pipeline.
  - If posts cannot be accessed, state that coverage was unavailable; never claim comprehensive monitoring.

## Weekly ChatGPT briefing specification

- Schedule: Monday, 10:00 Asia/Seoul.
- Coverage period: previous Monday 00:00 through Sunday 23:59 Asia/Seoul.
- Selection: 10–15 significant *distinct* items, not a mandatory number per category.
- Focus in order: **new frontier/open models and APIs**, **coding agents and AI developer tools**, **LLM/agent evaluations, alignment and safety research**, **important product releases**, then **policy, investment and infrastructure with meaningful technical impact**.
- For every item provide: title, announcement/event date, factual 2–3 sentence summary, why it matters for an AI developer, and working primary-source URL.
- Exclude rumors, duplicate coverage, recycled old stories, unsupported benchmarks and promotional-only posts.
- Distinguish **publication date** from **event/announcement date**. Never imply a paper is peer reviewed solely because it is on arXiv.
- If official pages are inaccessible or details cannot be confirmed, disclose the limitation and omit or explicitly mark the uncertain claim.
- Include a concise leading section: **Top 3 this week**, followed by **Models**, **Agents/Tools**, **Research/Safety**, **Industry**. Report fewer items when the week is quiet.
- Reading the GitHub repository or the OPML in a scheduled ChatGPT run is best-effort. To avoid relying on repository access at runtime, include this file's most important domains and the Threads handle explicitly in the recurring task instruction.

## Source maintenance

The GitHub Python pipeline uses `feedparser` and recognizes only OPML `outline` entries with `xmlUrl`. A manually monitored website must **not** be assigned `xmlUrl` until the endpoint is confirmed as a working RSS/Atom feed.
