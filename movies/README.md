# Film Watch Guide

`Film_Watch_Guide.xlsx` is an ordered map of cinema: 10 categories → 68 subcategories → 330 niches,
2,593 unique films and 4,219 watch-path entries (films sit in many buckets). The groupings rest on
film-studies texts, critics' polls, and label/curator catalogs. Letterboxd is used only to mark what you've seen.

- `catalog/`: the curated niches (one file per top-level category). Each line is `Title | Year | Director`;
  a `*` prefix means Start Here, no prefix means Core, `+` means Deep Cut. Line order is viewing order.
- `build_watch_guide.py`: builds the workbook.

Rebuild with a fresh Letterboxd export:

    python movies/build_watch_guide.py path/to/letterboxd-export.zip movies/Film_Watch_Guide.xlsx

Or skip rebuilding: paste a newer `watched.csv` into the workbook's **Letterboxd Watched** sheet
(columns A–D) and every Seen mark updates.
