import re

# -----------------------------
# Regular expressions
# -----------------------------

# Order addenda: includes billable flag (0/1) and short + long descriptions
ORDER_ADD_RE = re.compile(
    r"Add:\s+(\d)\s+([A-Z0-9]+)\s+(.*?)\s{2,}(.*)"
)
ORDER_DEL_RE = re.compile(
    r"Delete:\s+(\d)\s+([A-Z0-9]+)\s+(.*)"
)
ORDER_REV_FROM_RE = re.compile(
    r"Revise from:\s+(\d)\s+([A-Z0-9]+)\s+(.*?)\s{2,}(.*)"
)
ORDER_REV_TO_RE = re.compile(
    r"Revise to:\s+(\d)\s+([A-Z0-9]+)\s+(.*?)\s{2,}(.*)"
)

# Codes addenda: code + long description only
CODES_ADD_RE = re.compile(
    r"Add:\s+([A-Z0-9]+)\s+(.*)"
)
CODES_DEL_RE = re.compile(
    r"Delete:\s+([A-Z0-9]+)\s+(.*)"
)
CODES_REV_FROM_RE = re.compile(
    r"Revise from:\s+([A-Z0-9]+)\s+(.*)"
)
CODES_REV_TO_RE = re.compile(
    r"Revise to:\s+([A-Z0-9]+)\s+(.*)"
)


# -----------------------------
# Order Addenda Parsing
# -----------------------------

def parse_order_addenda_line(line: str):
    for kind, regex in [
        ("add", ORDER_ADD_RE),
        ("delete", ORDER_DEL_RE),
        ("revise_from", ORDER_REV_FROM_RE),
        ("revise_to", ORDER_REV_TO_RE),
    ]:
        m = regex.match(line)
        if not m:
            continue

        if kind == "add":
            flag, code, short_desc, long_desc = m.groups()
            return {
                "op": "add",
                "code": code,
                "is_billable": (flag == "1"),
                "short_description": short_desc.strip(),
                "long_description": long_desc.strip(),
                "source": "order_addenda",
            }

        if kind == "delete":
            flag, code, _ = m.groups()
            return {
                "op": "delete",
                "code": code,
            }

        if kind in ("revise_from", "revise_to"):
            flag, code, short_desc, long_desc = m.groups()
            return {
                "op": kind,
                "code": code,
                "is_billable": (flag == "1"),
                "short_description": short_desc.strip(),
                "long_description": long_desc.strip(),
                "source": "order_addenda",
            }

    return None


def stream_order_addenda(path):
    with open(path, encoding="utf8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            rec = parse_order_addenda_line(line)
            if rec:
                yield rec


# -----------------------------
# Codes Addenda Parsing
# -----------------------------

def parse_codes_addenda_line(line: str):
    for kind, regex in [
        ("add", CODES_ADD_RE),
        ("delete", CODES_DEL_RE),
        ("revise_from", CODES_REV_FROM_RE),
        ("revise_to", CODES_REV_TO_RE),
    ]:
        m = regex.match(line)
        if not m:
            continue

        if kind == "add":
            code, long_desc = m.groups()
            return {
                "op": "add",
                "code": code,
                "long_description": long_desc.strip(),
                "source": "codes_addenda",
            }

        if kind == "delete":
            code, _ = m.groups()
            return {
                "op": "delete",
                "code": code,
            }

        if kind in ("revise_from", "revise_to"):
            code, long_desc = m.groups()
            return {
                "op": kind,
                "code": code,
                "long_description": long_desc.strip(),
                "source": "codes_addenda",
            }

    return None


def stream_codes_addenda(path):
    with open(path, encoding="utf8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            rec = parse_codes_addenda_line(line)
            if rec:
                yield rec

