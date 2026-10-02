# Brief R3 - district vulnerability composition, paper-ready

A regional risk assessment divides a study area into six districts (A-F). For each
district, the share of its land area falling into each of three vulnerability tiers
(low, medium, high) has been measured. Within every district the three shares sum to
1.00.

| District | low  | medium | high |
|----------|------|--------|------|
| A        | 0.42 | 0.35   | 0.23 |
| B        | 0.31 | 0.44   | 0.25 |
| C        | 0.55 | 0.30   | 0.15 |
| D        | 0.28 | 0.47   | 0.25 |
| E        | 0.37 | 0.38   | 0.25 |
| F        | 0.50 | 0.33   | 0.17 |

Question to answer with the figure: describe the vulnerability composition of each
district, and support a judgement about which two districts have the most similar
structure. I need one figure (with its caption) that I can paste straight into the
body text of my paper.

Deliverables - write all of these into the output directory:

1. `table.tex` - the LaTeX source for **one table** that answers the question above, as a
   self-contained snippet the author can paste into a paper (do **not** include a preamble;
   assume `booktabs` and `siunitx` are available). Deterministic, no network, no manual steps.
2. `caption.txt` - the table caption, in English, as plain text.
