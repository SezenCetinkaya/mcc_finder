import re

def extract_meaningful(text):
    
    if not text:
        return {"words": [], "sentences": []}

    # words which has 3 or more characters
    words = re.findall(r'\b\w{3,}\b', text)

    # sentences ending with ., !, or ?
    sentences = re.findall(r'[^.!?]+[.!?]', text)

    # clean up leading/trailing spaces and remove empty entries
    words = [w.strip() for w in words if w.strip()]
    sentences = [s.strip() for s in sentences if s.strip()]

    return {"words": words, "sentences": sentences}
