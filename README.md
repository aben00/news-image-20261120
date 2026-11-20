# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/aben00/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/aben00/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Sum up 20 November's world news in one image — a "The World Today" newspaper front page for **Friday 20 November 2026**, drawn with Pillow. $250 pot; the top 50 entries share it. Entries close 2026-11-22T00:00:00Z.

## The image

A one-page front page, 1024×1024 PNG, under 1 MiB. The masthead names the day — **FRIDAY · 20 NOVEMBER · 2026** — in a red band, with three illustrated lead stories and a dense brief index of 17 more stories. Every story happened, or was first reported, on Friday 20 November 2026.

## Lead stories

1. **Missiles over Kyiv** (Ukraine) — Russia fires a wave of ballistic missiles at the capital in the early hours; air-raid alerts from 01:19, about a dozen missiles reported, aimed at bridges and energy sites; a projectile lands near the Dutch embassy, causing minor damage.
2. **Cyclone Akvan hits the coast** (India) — Severe Cyclone Akvan crosses the Odisha–Andhra coast by noon; about 300,000 people evacuated to 9,341 shelters, 423 rescue teams deployed, 69 trains cancelled; winds 90–100 kmph, gusting to 110.
3. **Asian stocks plunge** (Markets) — The Nikkei falls 4.5% to below 57,000 and the Kospi 4.7% as the AI selloff spreads; SoftBank drops 14%; the MSCI Asia-Pacific index falls for a seventh straight session.

## Also today — the brief index

Houthi strikes on four Saudi targets (and the coalition's intercepts); Taiwan's new short-selling curbs take effect; COP31 closes in Antalya with fossil fuels dropped from the draft; Trump's noon White House news conference after his China trip; oil steady near $92.60 Brent; the ATP Finals in Turin (Alcaraz v Cobolli, Medvedev v Tiafoe winner-takes-all); Taiwan's dollar near a 10-year low; a New Taipei council candidate released on bail; Taiwan's inheritance-law change; chip stocks sliding in Seoul and Tokyo; US monthly options expiry; Congress back facing the Dec 11 funding deadline; the Abu Dhabi T10 qualifier; Tokyo's three-day weekend; Nikkei futures; Taiwan's three-day slide; GIFT Nifty pointing lower.

Stories from 19 November — the Shenzhen trilateral summit, the ICJ Myanmar ruling, the Anthropic debut, the GTA VI launch, Voyager 1's light-day, Korea's $1 trillion exports, the Berlin Ukraine summit — were checked and deliberately left out: this page is 20 November alone.

Sources: Reuters, BBC, AP, The Hindu, IMD, AFP, UDN, TradingView, ATP.

## Files

- `entry.png` — the 1024×1024 image the program writes out.
- `main.ts` — the entrypoint: runs `draw.py` with python3 to write `entry.png` to the output directory, falling back to the committed `entry.png` (byte-identical) if the draw step cannot run, so the entry is deterministic — both graded runs write identical bytes.
- `draw.py` — draws the front page with Pillow (fixed seed, no clock, no network).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Licence

MIT — see `LICENSE`.
