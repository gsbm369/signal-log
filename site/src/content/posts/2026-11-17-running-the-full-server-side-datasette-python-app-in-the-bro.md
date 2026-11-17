---
title: "Running the full server-side Datasette Python app in the browser with service workers and Pyodide"
description: "Datasette Lite is my port of the Datasette Python application to run directly in the browser using WebAssembly and Pyodide . I've released a complete rewrite of Datasette Lite using service workers, and it's now almost i"
pubDate: 2026-11-17T16:48:33+00:00
addedAt: 2026-11-17T21:48:37.767209+00:00
source: "Simon Willison"
category: ai
sourceUrl: "https://simonwillison.net/2026/Nov/17/datasette-lite/"
tags: ["python", "sqlite", "webassembly"]
heat: 89
score: 1.45837
readMinutes: 1
image: "https://static.simonwillison.net/static/cors-allow/2026/datasette-maplibre.webp"
imageAlt: "Screenshot of a web map interface. Toolbar: &quot;View&quot; set to &quot;Clusters&quot;, &quot;Colour by&quot; set to &quot;continent&quot;, plus &quot;Filter to this area&quot; and &quot;Download GeoJSON&quot; buttons. A world map shows countries outlined and shaded by continent, with coloured dots and numbered cluster circles. A popup for a point in South America reads: capital Caracas, country Venezuela, continent South America, capital_population 2985000, latitude 10.502944, longitude -66.918983. Legend: Africa (52), Asia (45), Europe (39), North America (16), South America (13), Oceania (6). Text: &quot;All 171 rows are on the map&quot;. Below, a table with columns country, continent, capital_population, latitude, longitude, boundary. First row: Afghanistan, Asia, 3277000, 34.518636, 69.181314, with a small map in the boundary column showing Afghanistan outlined and shaded in blue."
hnPoints: 2
hnComments: 0
buzz: 18
---

Datasette Lite is my port of the Datasette Python application to run directly in the browser using WebAssembly and Pyodide . I've released a complete rewrite of Datasette Lite using service workers, and it's now almost indistinguishable from the real server-side application. You can now do all of the following, using a carefully crafted URL to lite.datasette.io : Load client-side Datasette to browse any SQLite database, JSON file, CSV file or SQL script Select a released version of Datasette to load from PyPI Load a specific commit, tag, or branch name from the Datasette GitHub repository Pick from over 100 versions of SQLite to use with Datasette Install additional Datasette plugins from PyPI or URLs to wheel files, including JavaScript visualization tools The ability to load specific Datasette references, plugins, and SQLite versions makes this a fantastic tool for linking to demos of

*Reproduced from the Simon Willison feed. No model was used to write this entry — follow the link for the full article.*
