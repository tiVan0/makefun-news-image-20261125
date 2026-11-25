# makefun-news-image-20261125

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/tiVan0/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/tiVan0/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

One image that sums up the world's news of **Wednesday 25 November 2026** —
a picture-led magazine / world atlas. The masthead names the day in full;
the atlas below it pins the 13 places that made the news; the lead story is
the Houthi missile strike on the PIF Tower in Riyadh; 12 illustrated stories
and 15 one-line items complete the day across 8 regions.

## What's in the picture

- **30 stories** — 1 lead + 2 secondary + 12 illustrated cards + 15 one-liners
- **15 illustrations**, each drawn in code with PIL (no photographs)
- **13 labelled pins** on the world map: New York, Washington, Warsaw, Kyiv,
  Gaza, Riyadh, Hormuz, Taiz, Seoul, Tokyo, Shanghai, Cikande, Sydney
- **BY THE NUMBERS** — every figure labelled: Dow 50,018.70 (first close
  above 50,000), KOSPI −5.3%, Dell revenue $54.94bn (+103%), 490,000+ Russian
  war deaths (leaked records), Gaza toll 74,746, 26 dead in Cikande
- **DATE CHECK** — three lines explaining the date: what counts as 25 November,
  why Tuesday-night US/Europe news is Wednesday's news in Asia, and which
  reported developments are *not* 25 November events (Riyadh strike 24 Nov,
  Miley Cyrus wedding 21 Nov, Microsoft outage 12–13 Nov)
- **Sources** (footer): Reuters, AP, UEFA.com, UN OCHA / UNRWA, BBC,
  Al Jazeera, Xinhua, company filings

## Run it

```sh
python3 render.py          # redraw entry.png from scratch (needs Pillow)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` is standard library only: it copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (mode 0644). It runs twice and writes
identical bytes both times.

## Files

- `entry.png` — the entry, 1024×1024 RGB, under 1 MiB
- `render.py` — the program that draws the image from the story list
- `main.py` — the entrypoint the grader runs
- `LICENSE` — MIT

## License

MIT — see `LICENSE`.
