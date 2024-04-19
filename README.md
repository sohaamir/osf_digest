# Getting a summary of OSF preprints

This directory contains code which allows one to extract and summarise OSF preprints for any given topic and date range.

Specficially, this involves:

- Extracting pre-print information from OSF (using the OSF API).
- Summarising this information (using the BART Large CNN model).
- Forecasting citations for the years 2024, 2025 and 2026 (using `prophet`).
