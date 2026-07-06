# NTE Fons Projection

A tiny **offline** calculator that projects how many **Fons** you'll have at the end
of the next patch in **Neverness to Everness (NTE)**.

Two front-ends, one shared model:

- **`nte-fons.html`** — standalone, offline, theme-aware GUI. Just open it in a browser.
- **`calc_fons.py`** — command-line version (Python 3, standard library only).

## Features

- Counts every recurring reset (daily / weekly / biweekly / monthly / per-patch)
  that fires between *now* and the end of the next patch.
- **DST-aware resets** — 05:00 local in summer time, 04:00 in winter
  (a fixed 03:00 UTC instant), picked automatically per date.
- **Patch day auto-derived** from a patch anchor (patches recur every 6 weeks, always on a Wednesday).
- **Settings modal** (GUI) — edit every payout and every cycle anchor; saved in your
  browser via `localStorage`.
- **Draggable end-date slider** (GUI) — trim the projection window day-by-day and watch
  the totals update live.
- Optional **Monthly Pass** / **Battle Pass** toggles.

## Usage

### GUI
Open `nte-fons.html` in any browser. No server, no build step, no dependencies.

### CLI
```sh
python3 calc_fons.py --fons 122000 --patch-start 2026-07-08
```
Options: `--now <ISO>`, `--patch-weeks <N>`, `--monthly-pass`, `--battle-pass`.

## Calibrating payouts

The Fons values (City Stamina, Mammon boss, Pink Paws Heist, …) are **estimates you
tune to your own account** — edit them in the GUI **Settings** modal, or in the
`CONFIG` block at the top of `calc_fons.py`. Cycle **anchors** set the phase of each
reset (any real past reset instant works) and roll forward automatically.

## Notes

- The summer/winter reset-hour switch assumes a Central-European timezone.
  Adjust `resetHourFor` (both files) if your server resets on a different rule.
- Payout numbers ship with sensible defaults but are game-version dependent — verify against your game.
- Not affiliated with or endorsed by the developers of Neverness to Everness.

## Optional desktop launcher (Linux)

```ini
[Desktop Entry]
Type=Application
Name=NTE Fons Projection
Exec=xdg-open /full/path/to/nte-fons.html
Icon=accessories-calculator
Terminal=false
Categories=Utility;Calculator;
```

## License

MIT — see [LICENSE](LICENSE).
