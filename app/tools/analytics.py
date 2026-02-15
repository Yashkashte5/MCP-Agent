def basic_stats(text: str):
    words = text.split()
    return {
        "word_count": len(words),
        "char_count": len(text),
    }
