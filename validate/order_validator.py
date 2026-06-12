from parsers.order_parser import stream_order_file

def validate_order_file(path):
    errors = []
    for rec in stream_order_file(path):
        code = rec.get("code")
        if not code:
            errors.append(f"Missing code in record: {rec}")
    return errors

