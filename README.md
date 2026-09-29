# Pump × PMS — Normal table

A curated subset of [PMS Database Normal Records](https://pmsdifficulty.xxxxxxxx.jp/PMSdifficulty.html) for songs featured in Pump It Up.

**[Open the table](https://sehun-joo.github.io/pump-pms-normal/)** — use this URL for player imports.

The source snapshot is dated **2026-09-28**. The fork includes the normal table's levels **1–45 and 45+**. Insane-table levels and unassessed `?` rows are excluded. Levels describe PMS difficulty, not Pump difficulty.

## Supplemental easier charts

Updated **2026-09-29** with mopemope (もぺもぺ) Normal **Lv22 / 250 notes** and Hyper **Lv40 / 634 notes**. These are 9-button PMS charts. They are listed in the upstream [excluded records](https://pmsdifficulty.xxxxxxxx.jp/excluded_PMSdifficulty.html) under the BGA gore category; their source comments preserve rating corrections of 20→22 and 39→40. These are documented ratings, not estimates from note density.

`supplemental-charts.json` retains both original records, source URL and the explicit numeric level used for import. The build does not automatically import other excluded records. Existing five-button charts remain included.

## Use

Open the GitHub Pages URL to browse and search. Add the same public page URL to a compatible BMS/PMS player's difficulty-table settings. The page exposes `bmstable` metadata pointing to `header.json`, which points to `data.json`. Hashes, original titles, author credits and links are preserved from the source. Supplemental rows annotate the original comments and use their documented numeric ratings. Original grade courses are omitted because they contain charts outside this subset.

This repository contains table metadata, not music or chart files. Follow the original song/package and chart links to obtain those separately. External downloads have not been tested.

You can also open `dist/index.html` locally; search works without a server. Automatic player import requires publicly accessible hosting. GitHub Pages is configured through `.github/workflows/pages.yml`.

## Curate or update

`catalog.json` lists the selected songs, aliases, artist checks and selection evidence. User-supplied additions are labeled as such; additional discoveries have source links. Matching uses normalized exact titles or known aliases and requires an artist match. It does not use arbitrary title substrings. No-normal-chart entries remain visible in the coverage list but are not inserted into playable data.

Run with Python 3 (no extra packages):

```sh
python build.py
# Explicitly refresh the normal-table snapshot:
python build.py --refresh --base-url https://YOUR-USER.github.io/pump-pms-normal
```

The GitHub Actions workflow rebuilds from the committed snapshot on each push; it does not silently fetch newer upstream rows. To refresh the snapshot, run the second command and commit the changed source and generated files. Update the snapshot date in `build.py` and `page.html` when refreshing.

## Scope and title handling

- Includes historical releases and spin-offs (RISE, Infinity, mobile), not just the current arcade release.
- Pump edits/remasters are matched at the song level, not asserted to be audio-identical to the BMS version.
- `Bamboo` matches `竹`; `Kokugen Kairou Labyrinth` matches `刻限回廊ラビリンス`; `F(R)IEND` matches `F℟IEND`; `L (PIU Edit)` matches Ice's `L`.
- `Destr0yer` by Sakuzyo is distinct from `Destroyer` by Tlahuizcalpantecuhtli. Only Sakuzyo's song is selected.
- The 5-button NightTheater and Rush-Hour entries are retained and clearly labeled.
- A missing match means absent from the checked normal snapshot and curated supplements, not absent from Pump or unavailable in all PMS sources.
- This is a curated starting set, not a claim to be the complete licensing catalog.

## Attribution

Chart metadata and rankings: [PMS Database](https://pmsdifficulty.xxxxxxxx.jp/PMSdifficulty.html), [upstream data](https://pmsdatabase.github.io/pmsdatabase/pmsdatabase_score.json). All original author and download credits are retained. The source snapshot is included for reproducibility. No upstream ownership is claimed. Independent fan-made fork; not affiliated with Andamiro or the original table's maintainers.
