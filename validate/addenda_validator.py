from parsers.addenda_parser import stream_order_addenda

def validate_addenda_file(path):
    errors = []
    for rec in stream_order_addenda(path):
        if "op" not in rec:
            errors.append(f"Missing operation in record: {rec}")
        if "code" not in rec:
            errors.append(f"Missing code in record: {rec}")
    return errors

