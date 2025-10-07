# 🍬 Jelly Belly Data Collection and Provenance Project

## Project Overview
This project focuses on collecting, structuring, and documenting data from the [Jelly Belly Wiki API](https://jelly-belly-wiki.netlify.app/).  
The goal is to create a transparent and reproducible dataset that reflects best practices in **data provenance**, **metadata standardization**, and **API-based data management**.

The dataset includes information on:
- **Beans** — flavor names, colors, and related attributes  
- **Recipes** — instructions and combinations using specific flavors  
- **Combinations** — creative mixes that link multiple bean flavors  
- **Facts** — trivia or details about Jelly Belly beans  
- **Milestones** — historical or brand-related events  

All data are exported into structured CSV files accompanied by JSON snapshots of the exact raw API responses.

---

## Scope and Purpose
This collection serves as a demonstration of proper **data provenance practices** in small-scale web data gathering projects.  
Key objectives include:
- Ensuring the **traceability** of all data sources  
- Preserving **API response integrity** through raw JSON archiving  
- Generating **Dublin Core-compliant metadata** for each dataset  
- Establishing reproducible naming and organization conventions  

The resulting datasets may be used for:
- Data provenance research  
- Metadata schema experimentation  
- Data visualization or analytics demonstrations  

---

## Data Collection Process
Data was gathered from the following API endpoints:

| Endpoint | Output CSV | Description |
|-----------|-------------|-------------|
| `/api/beans` | `beans.csv` | Flavor information (names, colors, categories) |
| `/api/recipes` | `recipes.csv` | Recipe data including descriptions and making amounts |
| `/api/combinations` | `combinations.csv` | Multi-flavor combination data |
| `/api/facts` | `facts.csv` | Fun facts and trivia entries |
| `/api/mileStones` | `milestones.csv` | Historical milestones and company events |

Each request was made via Python using the `requests` library.  
For endpoints supporting pagination, the script retrieved all pages until completion.
