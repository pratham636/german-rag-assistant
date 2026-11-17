import time
from answer import ask as ask_simple
from graph import ask as ask_agent

QUESTIONS = [
    "Wie oft darf man eine Prüfung wiederholen?",
    "Was passiert, wenn man eine Frist aus Gründen nicht einhalten kann, die man nicht zu vertreten hat?",
    "Wo ist das Centrum für Europarecht?",
    "Was muss man nach der Masterarbeit im Doppelmaster machen?",
    "Bis wann kann man von Prüfungen zurücktreten?",
]

for q in QUESTIONS:
    print(f"\n=== {q}")
    t = time.time(); a1, _ = ask_simple(q); t1 = time.time() - t
    t = time.time(); a2, _ = ask_agent(q);  t2 = time.time() - t
    print(f"SIMPLE ({t1:.1f}s): {a1}")
    print(f"AGENT  ({t2:.1f}s): {a2}")