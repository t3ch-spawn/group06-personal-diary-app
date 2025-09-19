import re

def search_by_keyword(text, keyword):
    """
    Search for a keyword in the given text using regex (case-insensitive).
    Returns a list of matches.
    """
    pattern = re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
    matches = pattern.findall(text)
    return matches

# Example usage
text = "The quick brown fox jumps over the lazy dog."
keyword = "fox"
matches = search_by_keyword(text, keyword)

if matches:
    print(f"Found '{keyword}' in the text.")
else:
    print(f"'{keyword}' not found in the text.")