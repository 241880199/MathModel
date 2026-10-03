# Brief: a schematic for the paper's modelling workflow

You are helping a team prepare a figure for their MCM/ICM paper. Their
modelling workflow for an epidemic-control study is described below.
Draw **one schematic figure** that lets a reader follow this workflow.

The workflow:

- **Data collection** - assemble weekly case counts, mobility traces and
  vaccination coverage for the study city.
- **Preprocessing** - clean the three streams and align them onto a common
  weekly grid.
- **Calibration** - estimate the transmission parameters by fitting a
  compartmental model to the aligned data.
- **Fit check** - decide whether the fit residual is acceptable.
  - If it is **not** acceptable, revise the model structure or the priors
    and return to **Calibration** (this loop can repeat).
  - If it is acceptable, move on.
- **Scenario projections** - run the calibrated model forward under three
  alternative policies: no intervention, a vaccination campaign, and
  school closure.
- **Comparison** - compare the three projections and rank them.
- **Recommendation** - write the recommendation that goes into the paper.

Deliverables - write all of these into the output directory:

1. `figure.tex` - a **self-contained, compilable** LaTeX document whose body
   is the figure as a TikZ picture. It must compile with `pdflatex` as-is.
   A minimal working TikZ skeleton is provided at the path given to you;
   you may copy it and build the figure on top of it.
2. `figure.pdf` - the compiled figure.
3. `caption.txt` - the English caption for the figure, as plain text.

Notes:

- The figure should be a schematic a reader can follow: boxes for the steps
  and arrows for the flow between them.
- Single figure, deterministic, no network access.

Environment fact (not part of the brief): `pdflatex` is on PATH.
