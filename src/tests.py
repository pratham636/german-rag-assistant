# (question, short text that MUST appear in the right chunk)
TESTS = [
    # Prüfungen / Wiederholung
    ("Wie oft darf man eine Prüfung wiederholen?", "zweimal wiederholt"),
    ("Bis wann muss die erste Wiederholung einer Prüfung stattfinden?", "innerhalb eines Jahres"),
    ("Was passiert, wenn man eine Frist aus Gründen nicht einhalten kann, die man nicht zu vertreten hat?", "auf Antrag eine"),
    ("Bei wem muss man eine krankheitsbedingte Prüfungsunfähigkeit melden?", "geltend gemacht"),

    # Prüfungsausschuss
    ("Wann ist der Prüfungsausschuss beschlussfähig?", "beschlussfähig"),

    # ECTS / Leistungspunkte
    ("Wie viele ECTS hat der LL.B. Legal Tech?", "ECTS"),
    ("Wie viele Leistungspunkte umfassen die erforderlichen Lehrveranstaltungen im Master der Juristischen Fakultät?", "45 ECTS"),
    ("Wofür steht die Abkürzung ECTS?", "European"),

    # Aufbau Jurastudium
    ("Was steht im Mittelpunkt des Hauptstudiums?", "Pflichtfächer mit den Übungen"),
    ("Was macht man im Abschlussstudium?", "Wiederholungskurse"),
    ("Wozu dienen die Schwerpunktbereiche?", "dienen der Ergänzung des Studiums"),

    # Paragraphen
    ("Was regelt § 4 der Allgemeinen Studien- und Prüfungsordnung?", "Qualifikation"),

    # FAQ Legal Tech
    ("Welche Aufgaben hat die Fachschaft?", "Interessen der Studierenden"),
    ("Was ist der Stammtisch?", "Stammtisch"),
    ("Kann man den Grundkurs Europarecht auch online an einer anderen Hochschule machen?", "Virtuellen"),

        # Doppelmaster Krasnojarsk
    ("Mit welcher Universität kooperiert der Doppelmaster Deutsches und Russisches Recht?", "Krasnojarsk"),
    ("Wie viele Semester studiert man im Doppelmaster jeweils in Passau und in Krasnojarsk?", "zwei Semester"),
    ("Was muss man nach der Masterarbeit im Doppelmaster machen?", "Verteidigung der Masterarbeit"),

    # Bekanntmachung Präsenzprüfungen
    ("Bis wann muss man sich im Wintersemester 2026/27 zu Prüfungen anmelden?", "15. Dezember 2026"),
    ("Bis wann kann man von Prüfungen zurücktreten?", "11. Januar 2027"),
    ("Was muss ich zur Prüfung mitnehmen, um mich auszuweisen?", ["Campus-Card", "Studierendenausweis"]),

    # Verzeichnis Universitätsgebäude
    ("In welchem Gebäude befindet sich das Graduiertenzentrum?", "Graduiertenzentrum"),
    ("Wo ist das Centrum für Europarecht?", "Centrum für Europarecht"),

    # Study Organisation (English questions!)
    ("When does the winter semester start and end?", "October 1"),
    ("What is the standard study duration of a master's programme?", "4 semesters standard"),
]

OUT_OF_SCOPE = [
    "Was ist die Hauptstadt von Frankreich?",
    "Wie backe ich einen Kuchen?",
    "Wer hat die Fußball-WM 2014 gewonnen?",
]