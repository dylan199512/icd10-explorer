# icd10-explorer
# ICD‑10 Explorer

A fast, lightweight tool for searching ICD‑10‑CM codes with clean filters, autocomplete, and structured detail pages.  
Built with Python, SQLite, SQLAlchemy, and Streamlit.

---

## Overview

ICD‑10 data is large, messy, and difficult to navigate in its raw form.  
This project provides a simple way to ingest the official ICD‑10‑CM source files, normalize them, store them in a structured database, and expose them through a clean, reactive UI.

The goal is speed, clarity, and ease of use.

---

## Features

- Autocomplete search across full ICD‑10 dataset  
- Billable‑only filter  
- Category prefix filter  
- Pagination for large result sets  
- Detail pages for each ICD‑10 code  
- Fast text queries via SQLAlchemy  
- Lightweight ingestion pipeline for raw ICD‑10 source files  

---

## Architecture

**1. Raw Data**  
Official ICD‑10‑CM order and addenda files.

**2. Parsing Layer**  
Python scripts extract codes, descriptions, and billable flags.

**3. Normalization**  
Data is cleaned and standardized into a consistent schema.

**4. Database**  
SQLite + SQLAlchemy models store structured ICD‑10 records.

**5. Query Layer**  
SQLAlchemy sessions provide fast text search and filtering.

**6. UI Layer**  
Streamlit app with autocomplete, filters, and detail views.

---

## Project Structure

```
icd10-explorer/
│
├── app.py                # Streamlit UI
├── ingest.py             # Ingestion pipeline
├── models.py             # SQLAlchemy models
├── config.py             # Config settings
│
├── data/                 # Raw ICD-10 source files (optional)
│
├── parsers/              # Parsing logic
│   ├── order_parser.py
│   └── addenda_parser.py
│
├── validate/             # Validation utilities
│
├── icd10.db              # Generated SQLite database
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Run the ingestion pipeline

```
python ingest.py
```

This generates `icd10.db`.

### 3. Launch the Streamlit app

```
streamlit run app.py
```

---

## Usage

- Type any ICD‑10 code or description into the search bar  
- Use filters to narrow results  
- Click a code to view full details  
- Explore categories by prefix  

The UI is designed to stay fast and readable even with large datasets.

---

## Why This Exists

ICD‑10 data is essential but painful to work with.  
This project makes it easier for developers, analysts, and clinicians to explore the dataset without wrestling with raw text files.

---
