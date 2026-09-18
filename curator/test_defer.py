#!/usr/bin/env python3
"""A subscriber-only item is deferred, then published once the paywall lifts.

LWN marks subscriber-only articles [$]. They were in the noise list, which cost
40% of the best Linux source on the site permanently. Verified against LWN's own
archive rather than taken on faith — same content type, different ages:

    Weekly Edition Sept 10   1.8 days old   HTTP 403  Subscription required
    Weekly Edition Sept  3   8.8 days old   HTTP 200  free
    Aug 27 / 20 / 13 / 6, Jul 30 / 23       HTTP 200  free

The deferred store is the half that makes this work at all: a [$] item leaves
LWN's 15-item feed long before it becomes free, so waiting for it to come round
again would wait for ever.

Needs network for the ripening test; skips that half without one.
"""
from __future__ import annotations

import json
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import curate  # noqa: E402
import ranker  # noqa: E402

FAILURES: list[str] = []


def check(name, got, want):
    if got == want:
        print(f"  PASS  {name}")
    else:
        FAILURES.append(name)
        print(f"  FAIL  {name}\n          got : {got}\n          want: {want}")


# A LWN Weekly Edition old enough to be free, and one fresh enough not to be —
# DISCOVERED at run time, not hardcoded.
#
# These were constants: the Sept 3 edition as "free" and the Sept 10 edition as
# "paywalled". The second was true for exactly one week. On 2026-09-18 the
# Sept 10 edition had ripened, the test asserted it was still paywalled, and it
# failed on a perfectly healthy system — a constant in an assertion is a
# measurement of the day it was written. The relationship that stays true is
# "the NEWEST edition is paywalled, one three editions back is free", so that is
# what the fixture is built from.
def _editions() -> list[str]:
    import re, urllib.request
    try:
        req = urllib.request.Request("https://lwn.net/Archives/",
                                     headers={"User-Agent": "signal.log-curator/2.0"})
        body = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
    except Exception:
        return []
    ids = []
    for aid in re.findall(r'href="/Articles/(\d+)/"[^>]*>\s*[^<]*Weekly Edition', body):
        if aid not in ids:
            ids.append(aid)
    return [f"https://lwn.net/Articles/{a}/" for a in sorted(ids, key=int, reverse=True)]


def _paywalled_now() -> str:
    """A [$] item from LWN's LIVE feed, under five days old.

    Not the newest archive edition: the /Archives/ index lags publication —
    measured on 2026-09-18 it had not yet listed the Sept 17 edition, so its
    "newest" was the Sept 10 one, already free. The RSS feed is current by
    construction, and [$] there means subscriber-only right now.
    """
    import time, urllib.request
    from datetime import datetime, timezone
    import feedparser
    try:
        raw = urllib.request.urlopen(urllib.request.Request(
            "https://lwn.net/headlines/newrss",
            headers={"User-Agent": "signal.log-curator/2.0"}), timeout=20).read()
    except Exception:
        return ""
    now = datetime.now(timezone.utc)
    for e in feedparser.parse(raw).entries:
        st = e.get("published_parsed") or e.get("updated_parsed")
        if not st or not e.get("title", "").startswith("[$]"):
            continue
        age_d = (now - datetime.fromtimestamp(time.mktime(st), timezone.utc)).days
        if age_d < 5:
            return e.get("link", "")
    return ""


_ED = _editions()
PAYWALL_URL = _paywalled_now()
FREE_URL = _ED[3] if len(_ED) >= 4 else ""


def main() -> int:
    print("\n-- classification --")
    check("[$] is deferred, not noise",
          (ranker.is_deferred("[$] x"), ranker.is_noise("[$] x")), (True, False))

    print("\n-- the store holds an unripe item --")
    with tempfile.TemporaryDirectory() as td:
        curate.STATE_DIR = Path(td)
        curate.DEFERRED_FILE = Path(td) / "deferred.json"
        now = datetime.now(timezone.utc)
        store = {
            "fresh": {"key": "fresh", "url": PAYWALL_URL, "title": "fresh one",
                      "source": "LWN.net", "category": "devops_linux",
                      "first_seen": (now - timedelta(days=1)).isoformat(),
                      "status": "deferred"},
        }
        ready = curate.ripen_deferred(dict(store), now)
        check("an item younger than the re-check window is not even probed",
              (len(ready), curate.METRICS.get("deferred_probed")), (0, 0))

    print("\n-- ripening, against LWN itself --")
    if not (FREE_URL and PAYWALL_URL):
        print("  SKIP — could not read LWN's archive to pick fixtures")
        print()
        return 0 if not FAILURES else 1
    print(f"  fixtures: paywalled={PAYWALL_URL}  free={FREE_URL}")
    free = curate._is_free(FREE_URL)
    pay = curate._is_free(PAYWALL_URL)
    if free is None or pay is None:
        print("  SKIP — no network, or LWN did not answer")
        print()
        return 0 if not FAILURES else 1
    check("an aged LWN edition reads as free", free, True)
    check("a fresh LWN edition reads as paywalled", pay, False)

    with tempfile.TemporaryDirectory() as td:
        curate.STATE_DIR = Path(td)
        curate.DEFERRED_FILE = Path(td) / "deferred.json"
        now = datetime.now(timezone.utc)
        old = (now - timedelta(days=10)).isoformat()
        store = {
            "ripe":  {"key": "ripe", "url": FREE_URL, "title": "ripe one",
                      "source": "LWN.net", "category": "devops_linux",
                      "first_seen": old, "status": "deferred"},
            "unripe": {"key": "unripe", "url": PAYWALL_URL, "title": "unripe one",
                       "source": "LWN.net", "category": "devops_linux",
                       "first_seen": old, "status": "deferred"},
            "stale": {"key": "stale", "url": FREE_URL, "title": "abandoned",
                      "source": "LWN.net", "category": "devops_linux",
                      "first_seen": (now - timedelta(days=99)).isoformat(),
                      "status": "deferred"},
        }
        ready = curate.ripen_deferred(store, now)
        titles = sorted(r["title"] for r in ready)
        check("the freed item is promoted", titles, ["ripe one"])
        check("the still-paywalled item stays deferred",
              store.get("unripe", {}).get("status"), "still_paywalled")
        check("the promoted item leaves the store", "ripe" in store, False)
        check("an item past the give-up window is abandoned, not probed for ever",
              store.get("stale", {}).get("status"), "gave_up")

    print()
    if FAILURES:
        print(f"FAILED: {FAILURES}")
        return 1
    print("All defer tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
