# Brief R1 - district vulnerability composition

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
structure.

Deliverables - write all of these into the output directory:

1. `make_figure.m` - a MATLAB script that regenerates the figure from the numbers
   above, deterministically, with no network access and no manual steps, and that
   can be run headlessly.
2. the exported figure, twice: as `figure.png` and as `figure.pdf`.
3. `caption.txt` - the figure caption, in English, as plain text.
