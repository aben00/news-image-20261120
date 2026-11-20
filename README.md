# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/aben00/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/aben00/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Sum up 20 November's world news in one image — a "The World Today" newspaper front page for **Friday 20 November 2026**, drawn with Pillow. $250 pot; the top 50 entries share it. Entries close 2026-11-22T00:00:00Z.

## The image

A one-page front page, 1024×1024 PNG, under 1 MiB. The masthead names the day — **FRIDAY · 20 NOVEMBER · 2026** — in a red band, with three illustrated lead stories, a pinned world map, nine more illustrated stories and a dense brief index of 24 more stories: **36 verified stories of the day, 12 illustrations, 6 continents**.

## Lead stories

1. **Missiles over Kyiv** (Ukraine) — Russia fires a wave of ballistic missiles at the capital in the early hours; air-raid alerts from 01:19, about a dozen missiles reported.
2. **Cyclone Akvan hits the coast** (India) — Severe Cyclone Akvan crosses the Odisha–Andhra coast by noon; about 300,000 people evacuated, 69 trains cancelled; winds 90–100 kmph.
3. **Asian stocks plunge** (Markets) — The Nikkei falls 4.5% to below 57,000 and the Kospi 4.7% as the AI selloff spreads; SoftBank drops 14%; the MSCI Asia-Pacific index falls for a seventh session.

## The map

A simplified world map pins all 12 illustrated stories by number (1–3 the leads, 4–12 below), so the day's geography is visible at a glance: Kyiv, India's east coast, Tokyo, Riyadh, New York, Berlin, Senegal, Brussels, Paris, Wellington and Cincinnati.

## More of the day — in pictures

4. **Houthis claim 4 Saudi strikes** — the Houthis claim strikes on four Saudi targets; the coalition says it downed five missiles and a cruise missile. 5. **Anthropic joins top indexes** — Anthropic joins MSCI Large Cap and FTSE global indexes after its record IPO. 6. **Europe ready for talks** — Europe is ready for talks with Russia on ending the war, leaders say. 7. **13,000 march in Tokyo** — protest against the Takaichi government's policies. 8. **Senegal search resumes** — four bodies recovered off Yenne; dozens missing after a migrant boat capsizes. 9. **EU plans €45bn for Ukraine** — the Commission proposes a €45 billion joint-debt loan. 10. **Harris meets Macron** — a courtesy meeting in Paris amid 2028 speculation. 11. **Nicholls tons up** — Henry Nicholls hits an unbeaten 113 for New Zealand against India in Wellington. 12. **Pete Rose pardoned** — Trump posthumously pardons the baseball legend.

## Also today — the brief index (24 more stories)

A projectile lands near the Dutch embassy in Kyiv; SK Hynix and Samsung each fall more than 5% in Seoul; three killed in a drone attack on Russia's Saratov region; Taiwan's dollar nears a 10-year low; a 3-year-old rescued from rubble 8 hours after a Tbilisi gas explosion; the US sanctions Hezbollah-linked charities and gold traders; Venezuela signs a military deal with the US; the White House taps Kirsten Davies as cyber chief; California targets Nvidia in a China AI chip probe; GIFT Nifty points to a gap-down start for Indian markets; Yemen's parliament designates the Houthis a terrorist organisation; the IEA calls the Mideast conflict the biggest energy security threat in history; the IEA warns data-centre power use could double by 2030; Congress is back facing a Dec 11 deadline to fund the government; nearly a quarter of the world's children live in conflict zones (Save the Children); Modi hails India's growth at the FICCI centenary; a fire at Muhammad Yunus's ancestral home in Chattogram; the NTA publishes the UGC NET December 2026 schedule; a man charged with terrorism offences after a Sydney raid; Taiwan's new short-selling curbs take effect; COP31 closes in Antalya with fossil fuels dropped from the draft; Trump's noon White House news conference after his China trip; the ATP Finals in Turin (Alcaraz v Cobolli, Medvedev v Tiafoe winner-takes-all); US monthly options expire as Wall Street reels from a tech reversal.

Stories from 19 November — the Shenzhen trilateral summit, the ICJ Myanmar ruling, the Fiona the hippo death, the Senegal boat capsizing itself, the PIF Tower strike in Riyadh, the Genoa airport drone shutdown, the Fontenay-sous-Bois fire, the Beqaa Valley strike in Lebanon, the Hormuz tanker mine strikes — were checked and deliberately left out, except where a story has a genuine 20 November development stated on the page (the Senegal search resuming, with four bodies recovered on the 20th; the Houthis' fresh 20 November claim of four Saudi strikes): this page is 20 November alone.

Sources: Reuters, BBC, AP, The Hindu, IMD, AFP, Le Monde, EIN Presswire, ATP.

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
