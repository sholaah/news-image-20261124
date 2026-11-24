# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/sholaah/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/sholaah/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A program that renders Tuesday 24 November 2026's world news as one Economist-style cover image: a cream page, a red "THE WORLD TODAY" masthead, the date as a huge title, and a drawn night scene over the Strait of Hormuz for the lead story — the UN counting 25 seafarers killed near the Strait as Iran vows "all means" against a US naval blockade. Below it: a UTC timeline strip, a schematic drawn world map marking nine flashpoints, and 42 short dated story items in three columns grouped by region (Middle East, Europe & Ukraine, Asia-Pacific, Americas & Markets, Climate & World, Sport & Science), closed by a "date check" verification footer naming the sources and verification time. The image is pre-rendered with Pillow by build_image.py and copied to the output directory by main.py, so the entrypoint is deterministic and needs no network.

## Run it

```sh
python3 build_image.py && MAKEFUN_OUTPUT_DIR=./output python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=s0dzaxys&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
