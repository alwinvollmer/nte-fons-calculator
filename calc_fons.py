#!/usr/bin/env python3
"""Neverness to Everness — Fons projection to end of next patch.

Counts every recurring reset that fires in the window (now, end-of-next-patch],
assuming the player already collected everything claimable up to `now`.
window = now -> (patch_start + PATCH_WEEKS weeks).
"""
import argparse
import math
from datetime import datetime, timedelta, timezone

# ---------------------------------------------------------------------------
# CONFIG  — edit here when the game changes.
# Every reset is a FIXED 03:00 UTC instant (= 05:00 CEST summer / 04:00 CET winter).
# Working in UTC means no DST bookkeeping; display is converted to local time.
# ---------------------------------------------------------------------------
UTC = timezone.utc
RESET_HOUR_UTC = 3                    # all resets fire at 03:00 UTC

PATCH_WEEKS   = 6                     # 1 patch = 6 weeks

CAFE_PER_HOUR = 2400                  # Cafe by Origen, continuous, NO cap (edit to your rate)
DAILY_MISSIONS = 20_000               # per daily reset (estimate, adjust if wrong)

WEEKLY = {"City Stamina": 700_000, "Mammon boss": 75_000,
          "Mysterious Cargo Delivery": 24_000}   # every Monday
PINK_PAWS   = 1_000_000               # biweekly
BEYOND_RAILS = 200_000                # biweekly
MONTHLY = {"Otherworld Salvage": 180_000, "Lost Exchange": 200_000}  # 1st of month
MONTHLY_PASS = 30_000                 # per daily reset, when --monthly-pass
BATTLE_PASS  = 700_000                # per patch, when --battle-pass

WEEK  = timedelta(days=7)
FORT  = timedelta(days=14)


def reset_instant(y, m, d):
    """The reset instant on a given date: 03:00 UTC (tz-aware)."""
    return datetime(y, m, d, RESET_HOUR_UTC, tzinfo=UTC)


# Reset-cycle anchors (any real reset instant; script rolls them forward).
WEEKLY_ANCHOR = reset_instant(2026, 7, 6)    # a Monday
PINK_ANCHOR   = reset_instant(2026, 7, 6)    # next Pink Paws = upcoming Monday
RAILS_ANCHOR  = reset_instant(2026, 7, 18)   # from in-game "12d 21h 34m" (seen 2026-07-05)
# ---------------------------------------------------------------------------


def count_periodic(now, end, anchor, period):
    """# of events (anchor + k*period) with now < event <= end."""
    k = math.floor((now - anchor) / period) + 1     # first event strictly after now
    first = anchor + k * period
    if first > end:
        return 0
    return int((end - first) // period) + 1


def count_monthly(now, end, day=1):
    """# of `day`-of-month at the reset instant with now < event <= end."""
    n, y, m = 0, now.year, now.month
    while True:
        dt = reset_instant(y, m, day)
        if dt > end:
            break
        if dt > now:
            n += 1
        m += 1
        if m > 12:
            m, y = 1, y + 1
    return n


def main():
    ap = argparse.ArgumentParser(description="NTE Fons projection to end of next patch")
    ap.add_argument("--fons", type=int, required=True, help="current Fons balance")
    ap.add_argument("--patch-start", required=True,
                    help="start date of the NEXT patch, YYYY-MM-DD (patch day)")
    ap.add_argument("--now", default=None, help="override current time, ISO (default: system now)")
    ap.add_argument("--patch-weeks", type=int, default=PATCH_WEEKS)
    ap.add_argument("--monthly-pass", action="store_true", help="add Monthly Pass (+30k/day)")
    ap.add_argument("--battle-pass", action="store_true", help="add Battle Pass (700k/patch)")
    args = ap.parse_args()

    if args.now:
        now = datetime.fromisoformat(args.now)
        if now.tzinfo is None:            # treat a naive --now as UTC
            now = now.replace(tzinfo=UTC)
    else:
        now = datetime.now(UTC).replace(microsecond=0)
    ps = datetime.fromisoformat(args.patch_start)
    patch_start = reset_instant(ps.year, ps.month, ps.day)
    end = patch_start + timedelta(weeks=args.patch_weeks)   # fixed UTC instant, no DST fixup needed

    rows = []  # (name, count, unit, subtotal)

    # weekly (Mondays)
    wk = count_periodic(now, end, WEEKLY_ANCHOR, WEEK)
    for name, pay in WEEKLY.items():
        rows.append((name, wk, pay, wk * pay))

    # biweekly
    pp = count_periodic(now, end, PINK_ANCHOR, FORT)
    rows.append(("Pink Paws Heist", pp, PINK_PAWS, pp * PINK_PAWS))
    br = count_periodic(now, end, RAILS_ANCHOR, FORT)
    rows.append(("Beyond the Rails", br, BEYOND_RAILS, br * BEYOND_RAILS))

    # monthly
    mo = count_monthly(now, end)
    for name, pay in MONTHLY.items():
        rows.append((name, mo, pay, mo * pay))

    # daily missions (05:00 daily reset)
    dm = count_periodic(now, end, WEEKLY_ANCHOR, timedelta(days=1))
    rows.append(("Daily Missions", dm, DAILY_MISSIONS, dm * DAILY_MISSIONS))

    if args.monthly_pass:
        rows.append(("Monthly Pass", dm, MONTHLY_PASS, dm * MONTHLY_PASS))
    if args.battle_pass:
        # current patch's pass assumed already claimed -> count only patches ending after patch_start
        bp = count_periodic(patch_start, end, patch_start, timedelta(weeks=args.patch_weeks))
        rows.append(("Battle Pass", bp, BATTLE_PASS, bp * BATTLE_PASS))

    # cafe — continuous accrual, no cap
    hours = max(0.0, (end - now).total_seconds() / 3600)
    cafe = int(round(CAFE_PER_HOUR * hours))
    rows.append(("Cafe by Origen", round(hours, 1), CAFE_PER_HOUR, cafe))

    earned = sum(r[3] for r in rows)
    total = args.fons + earned
    span_days = (end - now).total_seconds() / 86400

    lt = lambda d: d.astimezone()   # UTC instant -> local wall clock for display
    print(f"NTE Fons projection")
    print(f"  now            : {lt(now):%Y-%m-%d %H:%M %Z}")
    print(f"  next patch day : {lt(patch_start):%Y-%m-%d %H:%M %Z}")
    print(f"  end of patch   : {lt(end):%Y-%m-%d %H:%M %Z}  (+{args.patch_weeks} wk)")
    print(f"  window         : {span_days:.1f} days")
    print()
    print(f"  {'source':<26}{'cycles':>8}{'per':>12}{'fons':>16}")
    print("  " + "-" * 62)
    for name, cnt, pay, sub in rows:
        cyc = f"{cnt}" if not isinstance(cnt, float) else f"{cnt:g}h"
        print(f"  {name:<26}{cyc:>8}{pay:>12,}{sub:>16,}")
    print("  " + "-" * 62)
    print(f"  {'earned this window':<26}{'':>8}{'':>12}{earned:>16,}")
    print(f"  {'current balance':<26}{'':>8}{'':>12}{args.fons:>16,}")
    print(f"  {'TOTAL at patch end':<26}{'':>8}{'':>12}{total:>16,}")


if __name__ == "__main__":
    main()
