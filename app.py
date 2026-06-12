import streamlit as st
from sqlalchemy import or_
from models import SessionLocal, ICD10Code

# --- DB Session ---
session = SessionLocal()

# --- PAGE CONFIG ---
st.set_page_config(page_title="ICD‑10 Explorer", layout="wide")
st.title("ICD‑10 Code Explorer")

# --- AUTOCOMPLETE FUNCTION ---
def get_suggestions(prefix):
    if not prefix:
        return []
    results = (
        session.query(ICD10Code)
        .filter(
            ICD10Code.code.ilike(f"{prefix}%")
            | ICD10Code.short_description.ilike(f"{prefix}%")
        )
        .limit(20)
        .all()
    )
    return [f"{r.code} — {r.short_description}" for r in results]

# --- SEARCH INPUT ---
prefix = st.text_input("Search ICD‑10 codes or descriptions")
suggestions = get_suggestions(prefix)

selected = None
if suggestions:
    selected = st.selectbox("Suggestions", suggestions)

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filters")

billable_only = st.sidebar.checkbox("Billable codes only")

category = st.sidebar.text_input("Filter by category prefix (e.g., E08, S72)")

# --- QUERY BUILDING ---
query_filters = []

if prefix:
    query_filters.append(
        or_(
            ICD10Code.long_description.ilike(f"%{prefix}%"),
            ICD10Code.short_description.ilike(f"%{prefix}%"),
            ICD10Code.code.ilike(f"%{prefix}%"),
        )
    )

if billable_only:
    query_filters.append(ICD10Code.is_billable == True)

if category:
    query_filters.append(ICD10Code.code.ilike(f"{category}%"))

# --- EXECUTE QUERY ---
results = session.query(ICD10Code).filter(*query_filters).all()

# --- PAGINATION ---
PAGE_SIZE = 50
page = st.sidebar.number_input(
    "Page", min_value=1, max_value=max(1, (len(results) // PAGE_SIZE) + 1), value=1
)
start = (page - 1) * PAGE_SIZE
end = start + PAGE_SIZE
page_results = results[start:end]

st.write(f"Found {len(results)} results")

# --- RESULTS LIST ---
for r in page_results:
    if st.button(f"{r.code} — {r.short_description}", key=r.code):
        selected = f"{r.code} — {r.short_description}"

# --- DETAIL PAGE ---
if selected:
    code_value = selected.split(" — ")[0]
    code_obj = session.query(ICD10Code).filter_by(code=code_value).first()

    st.markdown("---")
    st.header("Code Details")

    st.subheader(f"{code_obj.code} — {code_obj.short_description}")
    st.write(code_obj.long_description)

    st.write(f"**Billable:** {'Yes' if code_obj.is_billable else 'No'}")
    st.write(f"**Source:** {code_obj.source}")

