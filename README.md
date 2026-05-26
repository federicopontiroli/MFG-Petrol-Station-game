# The petrol station game: the regional average price

This repository contains the data pipeline, numerical simulations and calibration for a multi-population **Mean Field Game (MFG)** model applied to the fuel prices. The theoretical framework and its applications have been discussed in a joint work with **Fabio Bagagiolo** and **Ivan Romanò**.

The project models the strategic pricing behavior of individual petrol stations as rational agents interacting within a competitive environment, using real-world data from the Autonomous Province of Trento.

## Repository Contents

* **Data Extraction & Cleaning:** A complete pipeline to extract and clean daily gasoline prices in Italy filtered by fuel type, service mode (e.g., self-service), and province. It includes modules for individual volatility estimation ($\sigma_i$) and $k$-means clustering.
* **Dynamics Simulations:** Functions to simulate price trajectories under both homogeneous agent assumptions and multi-population ($K$-clusters) dynamics. Real historical data is utilized to initialize the game and calibrate model parameters.

---

## Data Structures & Formats

* `df_clean`: A pivot-table dataframe containing daily retail prices for the first quarter of 2023 for each individual petrol station in the Province of Trento (specifically for *Gasoline* and *Self-service* options). Rows represent dates and columns represent station IDs.
* `df_stat`: A summary statistics dataframe that collects the quarterly average price and standard deviation (idiosyncratic volatility) for each station.
* `Other / Samples`: Includes sample snapshots of the raw `anagrafica` (station registry) and `prezzo` (daily price logs) dataframes for a single day to illustrate the pipeline's inputs.

---

## Data Source
The complete raw datasets are publicly provided by the Italian Ministry of Enterprises and Made in Italy (MIMIT) and can be accessed at:
 [MIMIT Open Data Portal](https://www.mimit.gov.it/it/open-data/elenco-dataset)

 ## References

If you are interested in the mathematical foundations of Mean Field Games and the core framework that inspired this application, please refer to:

* O. Guéant, J.M. Lasry, P.L. Lions. **Mean field games and applications.** In: *Paris-Princeton Lectures on Mathematical Finance 2010*. Lecture Notes in Mathematics, vol 2003, pages 205–266, Springer, Berlin, Heidelberg, 2011.
* Bagagiolo, Fabio; Pontiroli, Federico; Romanò, Ivan; **The petrol station game: the regional average price. A mean field analysis**,  arXiv e-prints, 05/2026, arXiv:2605.24241, Optimization and Control, https://ui.adsabs.harvard.edu/abs/2026arXiv260524241B
