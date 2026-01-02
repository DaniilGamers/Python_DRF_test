BAD_WORDS = ["дурак", "блядь", "срака"]


def check_bad_words(text):
    text_lower = text.lower()
    for word in BAD_WORDS:
        if word in text_lower:
            return True
    return False
