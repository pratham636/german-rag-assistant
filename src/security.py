import re
from logger import log

MAX_LEN = 500
BLOCKED_MSG = "Diese Anfrage kann ich leider nicht bearbeiten."

INJECTION_PATTERNS = [
    r"ignor\w*\s+(alle|all|previous|vorherige)",
    r"vergiss\s+(alle|deine)",
    r"forget\s+(all|your|previous)",
    r"system\s*prompt",
    r"du\s+bist\s+(jetzt|nun)",
    r"you\s+are\s+now",
    r"act\s+as",
    r"jailbreak",
    r"developer\s+mode",
    r"<\s*/?\s*(system|script)",
]

PII_PATTERNS = {
    "EMAIL": r"[\w.+-]+@[\w-]+\.[\w.]+",
    "PHONE": r"\+?\d[\d\s/-]{7,}\d",
    "IBAN": r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b",
}

def check_input(question: str):
    """Returns (ok, cleaned_question, reason)."""
    q = question.strip()

    if not q:
        return False, q, "empty"
    if len(q) > MAX_LEN:
        return False, q, "too_long"

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, q, re.IGNORECASE):
            return False, q, "prompt_injection"

    for label, pattern in PII_PATTERNS.items():
        q = re.sub(pattern, f"[{label}]", q)

    return True, q, None

def check_output(answer: str):
    """Block answers that leak the prompt instructions."""
    leaks = ["Beantworte die Frage NUR mit dem Kontext", "Kontext:\n"]
    if any(leak in answer for leak in leaks):
        log.warning("security | output blocked (prompt leak)")
        return BLOCKED_MSG
    return answer