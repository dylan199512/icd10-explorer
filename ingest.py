from models import init_db, SessionLocal, ICD10Code
from config import ORDER_FILE, ORDER_ADDENDA_FILE
from parsers.order_parser import stream_order_file
from parsers.addenda_parser import stream_order_addenda


# ---------------------------------------------------------
# Base ORDER ingestion
# ---------------------------------------------------------

def add_code(session, rec):
    obj = ICD10Code(
        code=rec["code"],
        year=2027,
        order_number=rec.get("order_number"),
        is_billable=rec.get("is_billable"),
        short_description=rec.get("short_description"),
        long_description=rec.get("long_description"),
        source=rec.get("source", "order"),
    )
    session.add(obj)


def update_code(session, code, data):
    obj = session.query(ICD10Code).filter_by(code=code).first()
    if not obj:
        return

    if "is_billable" in data:
        obj.is_billable = data["is_billable"]
    if "short_description" in data:
        obj.short_description = data["short_description"]
    if "long_description" in data:
        obj.long_description = data["long_description"]
    if "source" in data:
        obj.source = data["source"]


def delete_code(session, code):
    obj = session.query(ICD10Code).filter_by(code=code).first()
    if obj:
        session.delete(obj)


def ingest_order_file(session):
    for rec in stream_order_file(ORDER_FILE):
        add_code(session, rec)


# ---------------------------------------------------------
# ORDER Addenda ingestion (safe for duplicates)
# ---------------------------------------------------------

def apply_addenda(session):
    for rec in stream_order_addenda(ORDER_ADDENDA_FILE):
        op = rec["op"]
        code = rec["code"]

        # Normalize update payload
        update_payload = {
            "is_billable": rec.get("is_billable"),
            "short_description": rec.get("short_description"),
            "long_description": rec.get("long_description"),
            "source": rec.get("source"),
        }

        # -------------------------
        # ADD
        # -------------------------
        if op == "add":
            existing = session.query(ICD10Code).filter_by(code=code).first()

            if existing:
                # Treat duplicate ADD as an update
                update_code(session, code, update_payload)
            else:
                add_code(session, {
                    "code": code,
                    "order_number": None,
                    "is_billable": update_payload["is_billable"],
                    "short_description": update_payload["short_description"],
                    "long_description": update_payload["long_description"],
                    "source": update_payload["source"],
                })

        # -------------------------
        # DELETE
        # -------------------------
        elif op == "delete":
            delete_code(session, code)

        # -------------------------
        # REVISE FROM / REVISE TO
        # -------------------------
        elif op in ("revise_from", "revise_to"):
            update_code(session, code, update_payload)


# ---------------------------------------------------------
# Main entry point
# ---------------------------------------------------------

def main():
    engine = init_db()
    session = SessionLocal()

    print("Ingesting base ORDER file...")
    ingest_order_file(session)

    print("Applying ORDER addenda...")
    apply_addenda(session)

    session.commit()
    print("Done.")


if __name__ == "__main__":
    main()

