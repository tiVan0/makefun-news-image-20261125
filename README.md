# THE WORLD TODAY — 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/tiVan0/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/tiVan0/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One image that sums up the world's news of **Wednesday 25 November 2026**:
55 stories across 10 regions and 21 fields, drawn by hand in code — no
photographs.

## What is in the picture

- **3 big features** — the day's consensus trio: the U.S. proposes tariffs
  on 14 economies (China 20%), the KOSPI crashes 6.2% as AI doubts sink
  Asian chip stocks, and Shenzhou-24 docks at Tiangong with the first
  foreigner aboard (Pakistan's Muhammad Zeeshan Ali).
- **12 medium stories** — Ofgem's +26% UK energy price cap, the
  Solomon Islands–Australia security pact, Dhaka's Tk17,000 garment wage,
  the Cartagena hostage rescue, Ukrainian drone strikes on two Russian
  refineries, the Bogor mine flood, the Giza tanker fire, the Farmgate
  court ruling, the coalition strike on Hodeidah, the Gaza toll of 74,746,
  the Zaporizhzhia nuclear plant losing external power, and U.S. GDP 4.3%
  with core PCE 3.3%.
- **40 ALSO rows** (#16–55), a numbered-pin world map, a UTC timeline,
  region and field bars that both sum to 55, a DATE CHECK box listing the
  stories that are *not* 25 November's (Riyadh missile, Dell, Sanofi,
  Miley Cyrus, the Hamas chief killing, the Zaporizhzhia strike, UNRWA 397
  — all 24 November or older), and a NOT YET box for what had not happened.

Attribution tags on every story: **C = CONFIRMED** (official source),
**R = REPORTED**, **CL = CLAIM** (unverified). Sources: Reuters, AP,
Xinhua/CMSA, Ofgem, USTR, BEA, UN/OCHA, court and wire reports — all
figures as reported on 25 November 2026.

## Files

- `entry.png` — the image (1024×1024, 187,657 bytes).
- `main.py` — the entrypoint: standard library only, copies `entry.png`
  to `$MAKEFUN_OUTPUT_DIR/entry.png`. Deterministic (byte-identical on
  repeated runs).
- `render.py` — the build-time script that draws `entry.png` with PIL.
  It is a build tool, not part of the entrypoint; the image it produces
  is what ships.
- `research/verification-notes.md` — the verification log: primary sources
  for every key fact, the Bivia fact-check results, and the date-discipline
  correction (three stories the gap analysis carried from v1 turned out to
  be 24 November events and were moved to DATE CHECK).

## License

MIT — see `LICENSE`.
