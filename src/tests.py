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

     # Master Rechtsinformatik (FStuPO)
    ("Wie oft darf man ein nicht bestandenes Modul im Master Rechtsinformatik wiederholen?", "beliebig oft wiederholt"),
    ("Wie lang darf die Masterarbeit im Master Rechtsinformatik höchstens sein?", "80.000 Zeichen"),
    ("Welche Sprachkenntnisse braucht man zusätzlich für den Master Rechtsinformatik?", "englische Sprachkenntnisse"),
    ("Zu welchem Semester kann man den Master Rechtsinformatik beginnen?", "zum Sommersemester aufgenommen"),
    ("Welche Programmiersprache lernt man im Modul Softwareentwicklung für Juristen?", "Programmiersprache Python"),

    # Allgemeine Studien- und Prüfungsordnung Master (AStuPO-M-JUR)
    ("Kann man den Master Rechtsinformatik auch in Teilzeit studieren?", "hälftigen Teilzeit"),
    ("Wie viele Modulprüfungen darf man freiwillig zur Notenverbesserung wiederholen?", "können bis zu drei"),
    ("Wie lange dauert eine Hausarbeit mit kurzer Bearbeitungsfrist?", "90 Minuten"),
    ("Kann für Vorlesungen eine Anwesenheitspflicht festgelegt werden?", "Anwesenheitspflicht nicht festgelegt"),
    ("Wie lange ist die Bearbeitungszeit für die Masterarbeit?", "15 Wochen"),
    ("Um wie viele Wochen kann die Bearbeitungszeit der Masterarbeit maximal verlängert werden?", "acht Wochen"),
    ("Darf man die Masterarbeit auch auf Englisch schreiben?", "englischer Sprache"),
    ("In wie vielen gedruckten Exemplaren muss die Masterarbeit abgegeben werden?", "zwei gedruckten Exemplaren"),
    ("Bis wann muss man die Einsicht in Prüfungsakten beantragen?", "binnen eines Monats"),

    # LL.B. Legal Tech (Studien- und Prüfungsordnung)
    ("Wie lange ist die Regelstudienzeit im LL.B. Legal Tech?", "acht Semester"),
    ("Zu welchem Semester kann man den LL.B. Legal Tech beginnen?", "nur im Wintersemester"),
    ("Wie lange hat man Zeit für die Bachelorarbeit im LL.B. Legal Tech?", "Abgabe beträgt sechs Wochen"),

    # FAQ und Modulkatalog LL.B. Legal Tech
    ("Wie lange muss das Praktikum im LL.B. Legal Tech dauern?", "6 Wochen in Teilzeit"),
    ("Gibt es für den LL.B. Legal Tech einen Numerus clausus?", "zulassungsfrei"),
    ("Muss man für den LL.B. Legal Tech gut in Mathematik sein?", "mathematische Inhalte fast völlig"),
    ("In welcher Sprache werden die Veranstaltungen im LL.B. Legal Tech gehalten?", "Alle Veranstaltungen werden auf Deutsch"),
    ("Kann man mit dem Bachelor Legal Tech Rechtsanwalt oder Richter werden?", "Zugang zum Referendariat"),
    ("Was ist ELSA?", "European Law Students"),
    ("Wo hat Recode:Law seinen Sitz?", "Sitz in Münster"),

    # Studien- und Prüfungsordnung Rechtswissenschaft
    ("Wie lange dauert eine Klausur im Studiengang Rechtswissenschaft?", "einhundertzwanzig"),
    ("Innerhalb welcher Frist kann man Einwendungen gegen eine Bewertung erheben (Remonstration)?", "innerhalb von zwei Wochen"),
    ("Darf man Jura-Klausuren auch am Laptop schreiben?", "handschriftlich oder mit einem elektronischen"),
    ("Wie lange dauert das Jurastudium ohne Prüfungszeit?", "viereinhalb Jahre"),
    ("Wie wird die Zwischenprüfung bewertet?", "Die Zwischenprüfung wird als"),

    # Doppelmaster Krasnojarsk
    ("Wie viele ECTS-Credits umfasst der Doppelmaster Deutsches und Russisches Recht?", "120 ECTS-Credits"),
    ("Vor wie vielen Prüfern findet die Verteidigung der Masterarbeit im Doppelmaster statt?", "fünf Prüfern"),

    # Master Deutsches Recht für ausländische Studierende
    ("Welchen Sprachnachweis braucht man für den Master Deutsches Recht für ausländische Studierende?", "DSH 1"),

    # Bekanntmachung Präsenzprüfungen WiSe 2026/27
    ("Bis wann muss man den Erstantrag auf Nachteilsausgleich stellen?", "16. November 2026"),
    ("Wo werden die Sitzpläne für die zentral organisierten Prüfungen veröffentlicht?", "Sitzpläne"),
    ("Wann ist die Prüfung Introduction to Deep Learning?", "Introduction to Deep Learning"),

    # Verzeichnis Universitätsgebäude
    ("Wo befindet sich das Zentrum für Informationstechnologie und Medienmanagement (ZIM)?", "Innstraße 33"),
    ("Wo ist das CampusCard-Büro?", "CampusCard-Büro"),
    ("In welchem Gebäude ist das Praktikumsamt?", "Praktikumsamt"),

    # Study Organisation (English questions!)
    ("When do lectures usually start in the winter semester?", "second week of October"),
    ("How many hours of workload does one ECTS credit correspond to?", "30 hours"),

]

OUT_OF_SCOPE = [
    "Was ist die Hauptstadt von Frankreich?",
    "Wie backe ich einen Kuchen?",
    "Wer hat die Fußball-WM 2014 gewonnen?",
]


# Real user questions (written by a student, not AI)
REAL_TESTS = [
    ("Wann beginnt und endet das Wintersemester?", ["1. Oktober", "October 1"]),
    ("Wann beginnt und endet das Sommersemester?", ["1. April", "April 1"]),
    ("Wann kann ich mich für Prüfungen anmelden?", ["15. Dezember 2026", "Campusportal"]),
    ("Muss ich bei allen Kursen anwesend sein?", ["keine Anwesenheitspflicht", "Anwesenheitspflicht nicht festgelegt"]),
    ("Kann ich eine Prüfung schreiben, ohne mich angemeldet zu haben?", ["Ohne Anmeldung besteht", "Anmeldung ist immer erforderlich"]),
    ("Wo kann ich etwas ausdrucken?", ["Kopierzentrale"]),
    ("Wo sehe ich, in welchem Raum meine Vorlesung ist?", ["StudIP", "Stundenplan"]),
    ("Wo kann ich als Student wohnen?", ["Stud. Wohnen"]),
]

# Real questions with NO answer in the documents -> system should say "no info"
REAL_NO_ANSWER = [
    "Kann ich während des Semesters Vollzeit arbeiten?",
    "An wie vielen Tagen hat die Uni geöffnet?",
    "Wann hat die Bibliothek geöffnet?",
    "Gibt es an der Uni einen Dresscode?",
    "Ist die Mensa günstig?",
    "Wie hoch ist die Miete in Deutschland normalerweise?",
    "Wo kann ich Fragen zu meinem Visum stellen?",
]