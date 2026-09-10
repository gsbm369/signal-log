#!/usr/bin/env python3
"""Negative tests for the image extractor's only network sink.

This project's rule: a control is not in force until you have watched it refuse
something. Every case below is one this code ACCEPTED before `_safe_target`
existed — measured, not imagined:

    file:///tmp/x.html            -> read and parsed, og:image returned
    http://192.168.100.25:8080/   -> reachable from the builder, HTTP 200

Run:  python3 curator/test_images.py
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import images  # noqa: E402


def _tmp_html() -> str:
    fh = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False)
    fh.write('<meta property="og:image" content="https://evil.test/leak.png">')
    fh.close()
    return fh.name


REFUSED_SCHEMES = [
    "ftp://ftp.example.com/x.html",
    "gopher://example.com/",
    "data:text/html,<meta property='og:image' content='https://e/x.png'>",
    "jar:https://example.com/a.jar!/b.html",
]

REFUSED_HOSTS = [
    "http://127.0.0.1:8080/",
    "http://192.168.100.25:8080/",                 # measured reachable pre-fix
    "http://10.0.0.5/",
    "http://172.16.4.1/",
    "http://169.254.169.254/latest/meta-data/",    # cloud metadata service
    "http://[::1]/",
    "http://[fd00::1]/",
    "http://0.0.0.0/",
    "http://localhost:8080/",                      # by name, not by literal
]

MALFORMED = ["", "http://", "not-a-url", "https://", "://"]

# Hostile input must come back as a tuple, never as an exception. A missing
# picture is a designed outcome; a raised exception would fail the cycle.
NEVER_RAISES = REFUSED_SCHEMES + REFUSED_HOSTS + MALFORMED + [
    "file:///etc/passwd",
    "https://no-such-host.invalid/",
]


def main() -> int:
    failures: list[str] = []

    def check(label: str, ok: bool) -> None:
        print(f"  {'ok  ' if ok else 'FAIL'}  {label}")
        if not ok:
            failures.append(label)

    print("scheme refusal")
    path = _tmp_html()
    try:
        check(f"file://{path}", images._safe_target(f"file://{path}") is False)
        check(f"_from_og(file://…) -> (None, None)",
              images._from_og(f"file://{path}") == (None, None))
    finally:
        Path(path).unlink(missing_ok=True)
    for url in REFUSED_SCHEMES:
        check(url, images._safe_target(url) is False)

    print("private, loopback, link-local and reserved addresses")
    for url in REFUSED_HOSTS:
        check(url, images._safe_target(url) is False)

    print("malformed input")
    for url in MALFORMED:
        check(repr(url), images._safe_target(url) is False)

    print("a public host still passes — the guard must not break the feature")
    check("https://techcrunch.com/some/article/",
          images._safe_target("https://techcrunch.com/some/article/") is True)

    print("nothing here may raise")
    for url in NEVER_RAISES:
        try:
            check(f"_from_og({url[:38]!r})", images._from_og(url) == (None, None))
        except Exception as exc:                       # noqa: BLE001
            check(f"_from_og({url[:38]!r}) raised {type(exc).__name__}", False)

    class Junk:
        links = "not-a-list"

    try:
        check("extract(junk entry, file:///etc/passwd)",
              images.extract(Junk(), "file:///etc/passwd") == (None, None))
    except Exception as exc:                           # noqa: BLE001
        check(f"extract raised {type(exc).__name__}", False)

    print()
    if failures:
        print(f"FAILED ({len(failures)}): " + "; ".join(failures))
        return 1
    print("All image-guard refusals verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
