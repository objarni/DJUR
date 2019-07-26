# coding: utf-8
from pprint import pprint

from src.djur import djur


def test_approval_test_game_correct_guesses():
    got = []

    db = (
        'Kan djuret simma', 'j',
        ('gädda',),
        ('Krälar djuret', 'n', ('örn',), ('orm',))
    )

    fake_answers = ['spela', 'q', 'K', 'y', 'j', 'j', 'S', 'k', 'n', 'j', 'j', 'a']
    def fake_input():
        next_answer = fake_answers.pop(0)
        got.append(f"INP {next_answer}")
        return next_answer

    def fake_print(msg):
        got.append(f"PRN {msg}")

    # print, input
    djur(db, _input=fake_input, _print=fake_print)
    pprint(got)
    expected = [
        "PRN Välkommen till GISSA DJUR!",
        "PRN --------------------------",
        "PRN Jag känner till 3 djur.",
        "PRN (S)pela eller (A)vsluta?",
        "INP spela",
        "PRN Tänk på ett djur, så ska jag gissa vilket du tänker på!",
        "PRN När du tänkt klart, skriv (K)lart.",
        "INP q",
        "PRN Va? Skriv k när du är klar!",
        "INP K",
        "PRN OK då kör vi...",
        "PRN Kan djuret simma - (J)a eller (N)ej?",
        "INP y",
        "PRN Jag förstår bara j och n, svenska alltså!",
        "PRN Kan djuret simma - (J)a eller (N)ej?",
        "INP j",
        "PRN Jag gissar att du tänkte på gädda!",
        "PRN Hade jag rätt? (J)a eller (N)ej?",
        "INP j",
        "PRN Vad kul! :D :D :D",
        "PRN (S)pela eller (A)vsluta?",
        "INP S",
        "PRN Tänk på ett djur, så ska jag gissa vilket du tänker på!",
        "PRN När du tänkt klart, skriv (K)lart.",
        "INP k",
        "PRN OK då kör vi...",
        "PRN Kan djuret simma - (J)a eller (N)ej?",
        "INP n",
        "PRN Krälar djuret - (J)a eller (N)ej?",
        "INP j",
        "PRN Jag gissar att du tänkte på orm!",
        "PRN Hade jag rätt? (J)a eller (N)ej?",
        "INP j",
        "PRN Vad kul! :D :D :D",
        "PRN (S)pela eller (A)vsluta?",
        "INP a",
        "PRN Tack för att du spelade!",
    ]
    assert expected == got


def test_approval_test_no_actual_game():
    got = []

    fake_answers = ['q', '', 'a']
    def fake_input():
        next_answer = fake_answers.pop(0)
        got.append(f"INP {next_answer}")
        return next_answer

    def fake_print(msg):
        got.append(f"PRN {msg}")

    # print, input
    djur(('häst',), _input=fake_input, _print=fake_print)
    pprint(got)
    expected = [
        "PRN Välkommen till GISSA DJUR!",
        "PRN --------------------------",
        "PRN Jag känner till 1 djur.",
        "PRN (S)pela eller (A)vsluta?",
        "INP q",
        "PRN Jag förstår inte 'q'!",
        "PRN (S)pela eller (A)vsluta?",
        "INP ",
        "PRN Jag förstår inte ' '!",
        "PRN (S)pela eller (A)vsluta?",
        "INP a",
        "PRN Tack för att du spelade!"
    ]
    assert expected == got


# önskvärda features |||
## svar med både "n" och "j" som vänster krok
# djurformattering exvis "GÄDDA " --> "gädda"
# frågeformattering exvis "kan den flyga?" -> "Kan den flyga"
