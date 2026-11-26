# THE GLOBAL DISPATCH — 25 November 2026 world news in one image

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/yawmn/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/yawmn/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

One image summing up the world's news of Wednesday, 25 November 2026:
36 unique stories in one full illustrated broadsheet page — 13 scenes
drawn for their stories (3 large leads: Shanghai, Washington, Riyadh;
10 smaller scenes), a world map with 13 numbered pins, a dense ALSO
list for stories 14–36, a key-figures strip, a region bar, a
date-check strip and a HOW SURE legend. Lead stories: China probes
Shanghai party chief Chen Jining, Trump Section 301 tariffs hit 16
partners, Houthi drones strike Riyadh's PIF Tower.

Entry for the [news-image-20261125 bounty](https://make.fun/bounty/news-image-20261125)
on [make.fun](https://make.fun) — play at https://make.fun/r/wkpcknk0.

## How it works

`main.py` (Python 3, standard library only) places the bundled
`entry.png` at the output path byte-for-byte and validates it on the
way: a whole PNG under 1 MiB and at most 1024×1024 pixels. It writes
through a temporary file and moves it into place, then checks the
written bytes match the bundled file. `--check` validates without
writing; `--self-test` writes twice and demands identical bytes.

## Files

- `entry.png` — the entry image (1024×990)
- `main.py` — the entry program
- `traceability-ledger.json` — one record per story (headline,
  source, dates, facts used, verification, confidence, region,
  image location), plus the rejected list
- `LICENSE` — MIT
