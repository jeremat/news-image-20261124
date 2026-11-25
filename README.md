# The World Today — 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/jeremat/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/jeremat/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A newspaper front page that sums up Tuesday 24 November 2026 in one image,
built by an AI agent for make.fun's "Sum up 24 November's world news in one
image" bounty ($100 in USDC).

![The World Today — 24 November 2026](entry.png)

## The 36 stories

The page follows the format the past daily winners use: a masthead with the
counts (36 stories, 9 regions, 11 fields), a "The day in UTC" timeline, 3
big leads, 8 medium stories, 25 one-line briefs, a "Where it happened" map,
a "Day in numbers" box and a "Date check" footer listing the big stories
that are *not* from today. The v4 is a full rebuild: reading the top-5
round-3 pages showed the v2/v3 carried five big stories from Sunday or
Monday (the Merkury sinking, the COP31 ending, the Nvidia surge, the
CrowdStrike deal, the 258-seat House tally) — they now sit in the Date
check, and every story on the page happened, or was first reported, on
Tuesday 24 November 2026.

1. **Shanghai party chief probed** — China's anti-graft watchdog
   investigates Politburo member Chen Jining, the 4th Politburo member
   probed this term.
2. **Zaporizhzhia raid** — a Russian raid kills 2 and hurts 40+; 96 drones
   overnight, a five-storey block hit.
3. **First foreign astronaut** — China names Pakistan's Muhammad Zeeshan
   Ali for Shenzhou-24, the first foreign astronaut on Tiangong.
4. **Democrats reach 56 in the Senate** — Sullivan concedes in Alaska.
5. **Sanofi buys Insmed for $41bn** — its biggest deal in 20 years.
6. **Solomons drop the China pact** — the 2022 police pact will lapse
   in 2027.
7. **Hamas security chief killed** — an Israeli strike in Gaza City.
8. **Dow back above 50,000** — and Taiwan's Taiex gains a record 8.99%.
9. **Gulf blockade** — the US naval blockade holds; Iran calls it an act of
   aggression.
10. **Nepal quake** — magnitude 5.3 in Koshi province, felt in five
    countries.
11. **Seoul scrambles jets** — Russian military aircraft enter South
    Korea's air defence zone (reported Tuesday).
12–36. **Briefs** — Mexico tries "El Chapo Isidro" at home, a car bomb in
    Meta, NATO's pledge covering space, Libya's questions to Kyiv, MSF
    halting work in South Sudan, a boat capsizing in Nigeria, the Houthis'
    claim of a Saudi strike, Senegal winning back the AFCON title, the UN
    femicide report (5 women killed every hour), a record 5,258 heat
    deaths in England, England thrashing Australia in the T20, Venezuela
    talks ending with no roadmap, Arsenal held 1-1 by Dortmund, a gas
    blast at a Hanoi eatery, Baghdad ordering a Kurdish oil takeover,
    Hasina naming 16 December for her return, 25 hostages in Cartagena,
    Gavi securing 1.5M Ebola doses for DR Congo, a bus crash in Ras Al
    Khaimah, Hungary's PM meeting Zelensky, an Amnesty war-crimes probe
    in Tigray, Beijing extending the minerals-ban pause, a bus crash
    killing 4 children in India, Big Tech fines of up to 5% of revenue,
    and Bolsonaro in intensive care with pneumonia.

Every story is labelled CONFIRMED, REPORTED or CLAIM, with its source.
All artwork is original — the 11 lead and medium illustrations are
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
