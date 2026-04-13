import re

# Paths
BOOK_HTML_PATH = "/home/ubuntu/econ-growth/book.html"
REBUILD_SCRIPT_PATH = "/home/ubuntu/econ-growth/scripts_rebuild_booking_calendar.py"
FINALIZE_SCRIPT_PATH = "/home/ubuntu/econ-growth/scripts_finalize_booking_fix.py"

# 1. Get the backend URL
with open(FINALIZE_SCRIPT_PATH, "r") as f:
    finalize_content = f.read()
match = re.search(r'BACKEND_URL = "(.*?)"', finalize_content)
if not match:
    raise SystemExit("Could not find BACKEND_URL in scripts_finalize_booking_fix.py")
backend_url = match.group(1)

# 2. Get the replacement script content from scripts_rebuild_booking_calendar.py
with open(REBUILD_SCRIPT_PATH, "r") as f:
    rebuild_content = f.read()

replacement_start_marker = "replacement = '''"
replacement_end_marker = "'''"

start_index_rebuild = rebuild_content.find(replacement_start_marker)
if start_index_rebuild == -1:
    raise SystemExit("Could not find replacement start marker in scripts_rebuild_booking_calendar.py")

start_index_rebuild += len(replacement_start_marker)

end_index_rebuild = rebuild_content.find(replacement_end_marker, start_index_rebuild)
if end_index_rebuild == -1:
    raise SystemExit("Could not find replacement end marker in scripts_rebuild_booking_calendar.py")

replacement_script_content = rebuild_content[start_index_rebuild:end_index_rebuild]

# 3. Replace the placeholder with the actual URL in the replacement script content
fixed_script_content = replacement_script_content.replace("BOOKING_API_URL_PLACEHOLDER", backend_url)

# 4. Read the book.html content
with open(BOOK_HTML_PATH, "r") as f:
    book_content = f.read()

# 5. Define the anchors for the existing script block in book.html
# The script block starts with <script> and ends with </script> before the Google API scripts.
start_anchor_book = "<script>\nconst BOOKING_API_URL ="
end_anchor_book_tag = "</script>"

start_index_book = book_content.find(start_anchor_book)

if start_index_book != -1:
    # Find the first closing </script> tag after the start of the booking script
    script_block_end_tag_index = book_content.find(end_anchor_book_tag, start_index_book)

    if script_block_end_tag_index != -1:
        # Construct the final replacement, including the script tags
        final_replacement_block = f"<script>\n{fixed_script_content}\n</script>"

        # Replace the old script block with the new one
        new_book_content = book_content[:start_index_book] + final_replacement_block + book_content[script_block_end_tag_index + len(end_anchor_book_tag):]

        # 6. Write the updated content back to book.html
        with open(BOOK_HTML_PATH, "w") as f:
            f.write(new_book_content)
        print("Successfully fixed the booking script in book.html")
    else:
        print("Could not find the closing </script> tag for the booking script block after the start anchor.")
else:
    print("Could not find the start anchor for the booking script in book.html.")
