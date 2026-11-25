# CGHS + CS(MA) Rules 1944 — Interactive Study Guide

Open `index.html` in any browser (single offline file, no dependencies).

## Rebuild

```bash
python3 -I build/build.py <source.html> index.html
python3 -I build/verify_coverage.py <source.html> index.html COVERAGE_REPORT.md
```

Needs `beautifulsoup4` and `lxml`. `build/visuals.py` holds the hand-authored SVG flowcharts and
comparison tables (all facts taken from the source guide); `build/assets/` holds the CSS and JS.

`verify_coverage.py` checks that every text block, OM number, date, rupee amount, rule reference
and GD item in the source appears in the Overview / CGHS / CS(MA) views of the output.
