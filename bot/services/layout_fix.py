import re

# EN (QWERTY) -> RU (ЙЦУКЕН)
_EN_TO_RU = str.maketrans(
    "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
    "QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?~",
    "йцукенгшщзхъфывапролджэячсмитьбю.ё"
    "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё"
)

def en_to_ru_layout(text: str) -> str:
    """Convert text typed in English layout into Russian layout."""
    return text.translate(_EN_TO_RU)

def looks_like_wrong_layout(text: str) -> bool:
    """
    Heuristic: detect Russian text typed in English layout.
    - If text already has Cyrillic, do nothing.
    - If too short, ignore.
    - If contains only Latin letters + common punctuation/spaces, consider it.
    """
    text = (text or "").strip()
    if len(text) < 3:
        return False

    # Already Cyrillic? then it's not an EN-layout mistake
    if re.search(r"[А-Яа-яЁё]", text):
        return False

    # Only latin + punctuation/spaces
    return bool(re.fullmatch(r"[A-Za-z\s.,!?\"'()<>\-\[\]{}:;+/\\@#$%^&*_=`~]+", text))
