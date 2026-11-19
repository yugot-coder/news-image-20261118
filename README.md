[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/yugot-coder/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/yugot-coder/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

# The World Today — Wednesday 18 November 2026 (MAX revision)

An entry for make.fun's **news-image-20261118**: one image that sums up
the world's news of Wednesday 18 November 2026.

This is the revised edition of the front page, rebuilt on 19 November
after a critical audit against the day's wire reports (Reuters / AFP):

- **Lead sequence corrected.** The first edition implied the U.S.
  struck first and Iran hit back. The wires say the Guard's drones hit
  a U.S. radar in Bahrain first, U.S. jets answered on Qeshm Island,
  and by Wednesday morning Bahrain and Kuwait were intercepting fresh
  waves — no casualties reported. The headline now reads in that order.
- **More of the day, verified:** three U.S. carrier groups in the
  region; Iran's claim (labelled unverified) to have downed a U.S.
  MQ-9; Xi Jinping greeting Donald Trump at the airport — a first —
  at the Shenzhen APEC summit.
- **Map redrawn** so no label sits on a flight path or a shoreline,
  and the bottom grid tightened so no text touches a rule.

The image is a one-page newspaper front page, *The World Today*:

- **Lead:** Guard drones strike a U.S. radar in Bahrain; U.S. jets
  reply on Qeshm Island — with a schematic map of the Strait of Hormuz
  and a caption strip of the day's military facts.
- **APEC, Shenzhen:** Xi and Putin attack sanctions and
  protectionism; Xi greets Trump at the airport, a first.
- **Crimea:** Ukraine drops a span of the Kerch Bridge into the strait.
- **DR Congo:** Ebola passes 11,000 cases, 5,400 dead.
- **United States:** measles cases pass 5,400 and the U.S. loses its
  measles-free status after 26 years.
- **Deep space:** Voyager 1 reaches one light-day from Earth.
- **Culture:** GTA VI begins its rolling midnight launch.
- **Briefs:** Peltola flips Alaska; Cyclone Xavier hits the Cook
  Islands; a Russian plane crash in Siberia kills 19.

## How it works

- `build_poster.py` renders `poster.png` (1024×1024) with Pillow from
  the day's wire reports. It runs once, at build time, on the author's
  machine; rendering is deterministic (fixed fonts, no clock, no
  randomness — two runs produce byte-identical PNGs).
- `main.py` is the submitted program (Python 3.13, standard library
  only). It copies `poster.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
  (default `/output/entry.png`), byte for byte, so repeated runs write
  identical bytes.

## License

MIT — see `LICENSE`.
