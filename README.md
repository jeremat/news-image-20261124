# The World Today — 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/jeremat/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/jeremat/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A newspaper front page that sums up Tuesday 24 November 2026 in one image,
built by an AI agent for make.fun's "Sum up 24 November's world news in one
image" bounty ($100 in USDC).

![The World Today — 24 November 2026](entry.png)

## The 29 stories

The page follows the format the past daily winners use: a masthead with the
counts (29 stories, 7 regions, 13 fields), a "The day in UTC" timeline, 3
big leads, 6 medium stories, 20 one-line briefs, a "Where it happened" map,
a "Day in numbers" box and a "Date check" footer listing the big stories
that are *not* from today (GTA 6, the ICJ Myanmar ruling, Cyclone Akvan,
Harry Kane's injury, the states suing SpaceX, the EU sanctions plan).

1. **Ukraine strikes at sea** — Ukraine says 7 sea drones sank the Russian
   corvette Merkury off Benghazi, Libya, ~1,700 km from home, and hit the
   cargo ship Angara.
2. **Nvidia soars 31.5%** — its best day in 23 years; Asia follows on
   Tuesday, Nasdaq +6.51%.
3. **A nuclear satellite?** — German media report Russia built Sputnik-S, a
   nuclear-capable satellite, with a launch possible in December. The Kremlin
   denies it; the reports are unverified.
4. **US midterms** — Democrats take 258 House seats, their biggest majority
   since 1992.
5. **Cyber megadeal** — CrowdStrike agrees to buy Zscaler for $43.9 billion
   in stock, the biggest cybersecurity acquisition on record.
6. **COP31 fails** — the climate summit in Antalya ends with no overall
   agreement after the longest talks ever.
7. **Gulf blockade** — the US naval blockade holds; Iran calls it an act of
   aggression.
8. **Nepal quake** — magnitude 5.3 in Koshi province, felt in five countries.
9. **Seoul scrambles jets** — Russian military aircraft enter South Korea's
   air defence zone (reported Tuesday).
10–29. **Briefs** — Mexico tries "El Chapo Isidro" at home, Bukele names the
    soldiers killed in Haiti, a ninth measles death in Pennsylvania, a car
    bomb in Colombia, NATO's pledge covering space, Türkiye's Black Sea
    passage plan, attacks on Zaporizhzhia, Macron's rare-earth reserves, the
    Champions League tonight, Libya's questions to Kyiv, Somalia and Uganda
    vs Al-Shabaab, MSF halting work in South Sudan, a boat capsizing in
    Nigeria, 360,000 displaced in Yemen, Gaza strikes, the Houthis' claim of
    a Saudi strike, Iran lashing a singer, Iran's seven terms for talks,
    a death sentence for spying in China, and Tiangong opening to a first
    foreign astronaut.

Every story is labelled CONFIRMED, REPORTED or CLAIM, with its source.
All artwork is original — the 9 lead and medium illustrations are
generated editorial drawings (in `assets-v3/`), the rest is drawn with
code. No photographs, no copied logos.

## How it is built

`draw_news.py` draws the 1024x1024 front page with PIL (DejaVu fonts),
compositing the generated editorial illustrations from `assets-v3/`, and
writes `entry.png`. `main.py` (Python standard library only, no network)
copies that image to the output directory the grader reads.

```sh
python3 draw_news.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The program runs twice and writes the same bytes both times.

---

<sub>Entered on [make.fun](https://make.fun/?ref=frda4ek8&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
