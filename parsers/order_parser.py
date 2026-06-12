def parse_order_line(line):
    return {
        "order_number": int(line[0:5]),
        "code": line[6:13].strip(),
        "is_billable": (line[14:15] == "1"),
        "short_description": line[16:76].strip(),
        "long_description": line[77:].strip(),
        "source": "order",
    }

def stream_order_file(path):
    with open(path, encoding="utf8") as f:
        for line in f:
            if line.strip():
                yield parse_order_line(line)
