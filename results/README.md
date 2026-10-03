# results/: claims register, scoreboard, Results Book, verdict

Everything the report quotes comes from here. `build_results_book.py` reads the frozen study's `results.json` and the CSV tables in `../analysis/output/tables/`, registers every claim with a locator, re-verifies each one and writes the files below.

| File | Contents |
|---|---|
| `build_results_book.py` | Registers the claims (`claim(id, sentence, stated, locator, label, ...)`), verifies them, writes everything else. Run with `python3 -B results/build_results_book.py` from the project root. |
| `v3_claims.py`, `v3_section.md/.tex` | Claims and text for the V2d robustness battery (executed by the builder). |
| `claims.csv` | One row per claim: id, sentence, stated numbers, locator(s), label (CONF / POST-HOC / FWD), verified y/n, file value, note. 100 claims, all verified. |
| `scoreboard.csv`, `tables/scoreboard.tex` | Net Sharpe, IC, alpha, placebo and DSR for every strategy, by label. |
| `RESULTS_BOOK.md`, `results_book.tex`, `results_book.pdf` | The Results Book: verdict, scoreboard, every claim, figure and table list, AI-use rows, known issues. Build the PDF with `latexmk -pdf results_book.tex` (it `\input`s `../report/preamble`). |
| `VERDICT.md`, `verdict.tex` | The verdict on each strategy, what we can and cannot claim, and the figure plan. |

Locator formats: JSON `path::a.b.c`; CSV `path::col=<name>;<filter>=<value>[;...]`; markdown table `path::table=N||row=<label>||col=<name>`; hash file `path::line=N`. A claim that is counted rather than read (for example the number of calls in a log) states its rule in the `source` column and records the computed value.

Rule: a number that is not in `claims.csv` does not go in the report. If a sentence needs a new number, add a claim here first, rebuild, then quote the claim ID in the `% src:` comment.
