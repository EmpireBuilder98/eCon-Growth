import os

BACKEND_URL = "https://script.google.com/macros/s/AKfycby5pWyF_TawUei8-xqOJ4xG4S9sM0kX9n4Kbi2Sge6wF2GvS8oBHGnOtW3_J7eqa1AV/exec"

def patch_book_html():
    path = "book.html"
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        return

    with open(path, "r") as f:
        content = f.read()

    # Update the BOOKING_API_URL in the script
    placeholder = "const BOOKING_API_URL = 'BOOKING_API_URL_PLACEHOLDER';"
    if placeholder in content:
        content = content.replace(placeholder, f"const BOOKING_API_URL = '{BACKEND_URL}';")
        print(f"Updated BOOKING_API_URL in {path}")
    else:
        # Try a more flexible regex if exact match fails
        import re
        new_content = re.sub(r"const BOOKING_API_URL = '.*?';", f"const BOOKING_API_URL = '{BACKEND_URL}';", content)
        if new_content != content:
            content = new_content
            print(f"Updated BOOKING_API_URL via regex in {path}")
        else:
            print(f"Warning: Could not find BOOKING_API_URL placeholder in {path}")

    with open(path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    patch_book_html()
