# Brief R2 - drivers of historical disaster counts

A regional risk assessment divides a study area into six districts (A-F). Five
attributes have been measured for each district.

| District | Population density (people/km2) | Mean slope (degrees) | Vegetation cover (fraction of area) | Historical disaster count | Infrastructure index (0-100) |
|----------|--------------------------------|----------------------|-------------------------------------|---------------------------|------------------------------|
| A        | 820                            | 3.2                  | 0.61                                | 12                        | 74                           |
| B        | 640                            | 11.5                 | 0.58                                | 31                        | 72                           |
| C        | 610                            | 2.4                  | 0.72                                | 8                         | 81                           |
| D        | 1210                           | 14.8                 | 0.41                                | 38                        | 55                           |
| E        | 990                            | 7.1                  | 0.49                                | 16                        | 66                           |
| F        | 1750                           | 5.0                  | 0.55                                | 24                        | 70                           |

Question to answer with the figure: identify which factor is most strongly correlated
with the historical disaster count, and describe the similarity between districts.

Deliverables - write all of these into the output directory:

1. `make_figure.py` - a Python script that regenerates the figure from the numbers
   above, deterministically, with no network access and no manual steps.
2. the exported figure itself, as `figure.pdf` or `figure.png`.
3. `caption.txt` - the figure caption, in English, as plain text.
