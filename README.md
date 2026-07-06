# NTE Fons Projection

A tiny, self-contained web calculator that projects how many **Fons** you'll have at
the end of the next patch in **Neverness to Everness (NTE)**.

**▶ Live: <https://alwinvollmer.github.io/nte-fons-calculator/>** — runs entirely in your
browser. No install, no server, no dependencies. (Or just open `nte-fons.html` locally.)

## Features

- Counts every recurring reset (daily / weekly / biweekly / monthly / per-patch)
  that fires between *now* and the end of the next patch.
- **Timezone-correct** — all resets are anchored to a fixed **03:00 UTC** instant
  (05:00 CEST in summer, 04:00 CET in winter) and shown in your local time automatically.
- **Patch day auto-derived** from a patch anchor (patches recur every 6 weeks, always on a Wednesday).
- **Settings modal** — edit every payout and every cycle anchor; saved in your browser via `localStorage`.
- **Draggable end-date slider** — trim the projection window day-by-day and watch the totals update live.
- Optional **Monthly Pass** / **Battle Pass** toggles.

## Calibrating payouts

The Fons values (City Stamina, Mammon boss, Pink Paws Heist, …) are **estimates you
tune to your own account** — edit them in the **Settings** modal (⚙). Cycle **anchors**
set the phase of each reset (any real past reset instant works) and roll forward
automatically. Everything you change is saved in your browser.

> The calculator assumes every Fons source is **already collected up to now** — it only
> counts resets that fire from now until the end of the window.

## Notes

- Payout numbers ship with sensible defaults but are game-version dependent — verify against your game.
- Not affiliated with or endorsed by the developers of Neverness to Everness.

## Optional desktop launcher (Linux)

```ini
[Desktop Entry]
Type=Application
Name=NTE Fons Projection
Exec=xdg-open https://alwinvollmer.github.io/nte-fons-calculator/
Icon=accessories-calculator
Terminal=false
Categories=Utility;Calculator;
```

## License

MIT — see [LICENSE](LICENSE).
