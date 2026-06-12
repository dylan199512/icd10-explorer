# Backend selection
DB_BACKEND = "sqlite"

# SQLite database URL (file in project directory)
SQLITE_URL = "sqlite:///./icd10.db"

# Placeholder Postgres URL (unused when DB_BACKEND = "sqlite")
POSTGRES_URL = "postgresql://user:password@localhost:5432/icd10"

# Paths to ICD‑10 source files (relative to project root)
ORDER_FILE = "data/icd10cm_order_2027.txt"
ORDER_ADDENDA_FILE = "data/icd10cm_order_addenda_2027.txt"

