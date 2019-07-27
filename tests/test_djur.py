# coding: utf-8
from pprint import pprint

from src.djur import djur


def test_approval_test_no_actual_game():

    expected = [
        "PRN Välkommen till GISSA DJUR!",
        "PRN --------------------------",
        "PRN Jag känner till 1 djur.",
        "PRN (S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.",
        "INP q",
        "PRN Jag förstår inte 'q'!",
        "PRN (S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.",
        "INP ",
        "PRN Jag förstår inte ' '!",
        "PRN (S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.",
        "INP a",
        "PRN Tack för att du spelade!"
    ]

    fakes = Fakes(expected)
    djur(('häst',), _input=fakes.fake_input, _print=fakes.fake_print)
    actual = fakes.get_actual()

    assert expected == actual


class Fakes:

    def __init__(self, expected_log):
        self.fake_answers = self.filter_inp(expected_log)
        self.got = []

    def fake_input(self):
        next_answer = self.fake_answers.pop(0)
        self.got.append(f"INP {next_answer}")
        return next_answer

    def fake_print(self, msg):
        self.got.append(f"PRN {msg}")

    def get_actual(self):
        return self.got

    @staticmethod
    def filter_inp(full_log):
        return [x.partition(' ')[2] for x in full_log if x.startswith('INP')]



def test_filter_inp():
    log = [
        "INP j",
        "PRN Vad kul! :D :D :D",
        "PRN (S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.",
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
        "PRN (S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.",
        "INP a",
        "PRN Tack för att du spelade!",
    ]
    assert Fakes.filter_inp(log) == [
        'j', 'S', 'k', 'n', 'j', 'j', 'a'
    ]


def _test_approval_test_game_correct_guesses():

    db = (
        'Kan djuret simma', 'j',
        ('gädda',),
        ('Krälar djuret', 'n', ('örn',), ('orm',))
    )

    got = []

    def fake_input():
        next_answer = fake_answers.pop(0)
        got.append(f"INP {next_answer}")
        return next_answer

    def fake_print(msg):
        got.append(f"PRN {msg}")

    expected = [
        "PRN Välkommen till GISSA DJUR!",
        "PRN --------------------------",
        "PRN Jag känner till 3 djur.",
        "PRN (S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.",
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
        "PRN (S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.",
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
        "PRN (S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.",
        "INP a",
        "PRN Tack för att du spelade!",
    ]
    fake_answers = filter_inp(expected)
    djur(db, _input=fake_input, _print=fake_print)
    assert expected == got


def _test_approval_test_game_incorrect_guess():

    db = (
        'Kan djuret simma', 'j',
        ('gädda',),
        ('Krälar djuret', 'n', ('örn',), ('orm',))
    )

    got = []

    def fake_input():
        next_answer = fake_answers.pop(0)
        got.append(f"INP {next_answer}")
        return next_answer

    def fake_print(msg):
        got.append(f"PRN {msg}")

    expected = [
        "PRN Välkommen till GISSA DJUR!",
        "PRN --------------------------",
        "PRN Jag känner till 3 djur.",
        "PRN (S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.",
        "INP spela",
        "PRN Tänk på ett djur, så ska jag gissa vilket du tänker på!",
        "PRN När du tänkt klart, skriv (K)lart.",
        "INP klar",
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
        "PRN (S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.",
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
        "PRN (S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.",
        "INP a",
        "PRN Tack för att du spelade!",
    ]
    fake_answers = filter_inp(expected)
    djur(db, _input=fake_input, _print=fake_print)
    assert expected == got


# önskvärda features |||
## svar med både "n" och "j" som vänster krok
# uppdateringsalgoritm/interaktion
# djurformattering exvis "GÄDDA " --> "gädda"
# frågeformattering exvis "kan den flyga?" -> "Kan den flyga"
# persistens
