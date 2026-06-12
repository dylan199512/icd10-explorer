from config import ORDER_FILE, ORDER_ADDENDA_FILE
from validate.order_validator import validate_order_file
from validate.addenda_validator import validate_addenda_file

def main():
    print("Validating ICD-10 Order File...")
    order_errors = validate_order_file(ORDER_FILE)
    if order_errors:
        print("Order file errors:")
        for e in order_errors:
            print(" -", e)
    else:
        print("Order file OK.")

    print("\nValidating ICD-10 Addenda File...")
    addenda_errors = validate_addenda_file(ORDER_ADDENDA_FILE)
    if addenda_errors:
        print("Addenda file errors:")
        for e in addenda_errors:
            print(" -", e)
    else:
        print("Addenda file OK.")

if __name__ == "__main__":
    main()

