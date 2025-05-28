from langdetect import detect

def is_arabic(text: str) -> bool:
    try:
        return detect(text) == "ar"
    except:
        return False
