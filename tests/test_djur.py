# coding: utf-8
from pprint import pprint

from src.djur import djur, confirm


def test_approval_test_no_actual_game():

    expected = """\
PRN Välkommen till GISSA DJUR!
PRN --------------------------
PRN Jag känner till 1 djur.
PRN (S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.
INP q
PRN Jag förstår inte 'q'!
PRN Jag känner till 1 djur.
PRN (S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.
INP 
PRN Jag förstår inte ' '!
PRN Jag känner till 1 djur.
PRN (S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.
INP a
PRN Tack för att du spelade!""".splitlines()

    fakes = InteractionTest(expected)
    djur(('häst',), _input=fakes.fake_input, _print=fakes.fake_print)
    actual = fakes.get_actual()
    fakes.verify_interaction_consumed()


def test_approval_test_game_correct_guesses():

    db = (
        'Kan djuret simma', True,
        ('gädda',),
        ('Krälar djuret', False, ('örn',), ('orm',))
    )

    expected = """\
PRN Välkommen till GISSA DJUR!
PRN --------------------------
PRN Jag känner till 3 djur.
PRN (S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.
INP spela
PRN Tänk på ett djur, så ska jag gissa vilket du tänker på!
PRN När du tänkt klart, skriv (K)lart.
INP q
PRN Va? Skriv k när du är klar!
INP K
PRN OK då kör vi...
PRN Kan djuret simma - (J)a eller (N)ej?
INP y
PRN Jag förstår bara svenska; (J)a eller (N)ej?
INP j
PRN Jag gissar att du tänkte på gädda!
PRN Hade jag rätt? (J)a eller (N)ej?
INP j
PRN Vad kul! :D :D :D
PRN Jag känner till 3 djur.
PRN (S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.
INP S
PRN Tänk på ett djur, så ska jag gissa vilket du tänker på!
PRN När du tänkt klart, skriv (K)lart.
INP k
PRN OK då kör vi...
PRN Kan djuret simma - (J)a eller (N)ej?
INP n
PRN Krälar djuret - (J)a eller (N)ej?
INP j
PRN Jag gissar att du tänkte på orm!
PRN Hade jag rätt? (J)a eller (N)ej?
INP j
PRN Vad kul! :D :D :D
PRN Jag känner till 3 djur.
PRN (S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.
INP a
PRN Tack för att du spelade!""".splitlines()
    fakes = InteractionTest(expected)
    djur(db, _input=fakes.fake_input, _print=fakes.fake_print)
    fakes.verify_interaction_consumed()


def test_approval_test_game_incorrect_guess():

    db = [
        'Kan djuret simma', True,
        ['gädda'],
        ['Krälar djuret', False, ['örn',], ['orm',]]
    ]

    expected = """\
PRN Välkommen till GISSA DJUR!
PRN --------------------------
PRN Jag känner till 3 djur.
PRN (S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.
INP spela
PRN Tänk på ett djur, så ska jag gissa vilket du tänker på!
PRN När du tänkt klart, skriv (K)lart.
INP klar
PRN OK då kör vi...
PRN Kan djuret simma - (J)a eller (N)ej?
INP j
PRN Jag gissar att du tänkte på gädda!
PRN Hade jag rätt? (J)a eller (N)ej?
INP nej
PRN OK, men vilket djur tänkte du på då?
INP padda
PRN Kom på en fråga som innehåller ordet 'djuret',
PRN som skiljer padda och gädda åt.
PRN T.ex. 'Kan djuret simma?'
INP Har det ben?
PRN Snälla ta med ordet 'djuret' i frågan!
PRN Försök igen:
INP Har djuret ben?
PRN OK, och för padda är svaret på frågan 'Har padda ben?' (J)a eller (N)ej?
INP nej
PRN Denna fråga lär jag mig då:
PRN   Har padda ben?
PRN   Rätt svar: nej
PRN Ser det rätt ut?
INP nej
PRN Hmm, tvärtom alltså?
PRN Denna fråga lär jag mig då:
PRN   Har padda ben?
PRN   Rätt svar: ja
PRN Ser det rätt ut?
INP ja
PRN Tack för att du lärt mig något om djuret padda!
PRN Jag känner till 4 djur.
PRN (S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.
INP avsluta
PRN Tack för att du spelade!\
""".splitlines()
    fakes = InteractionTest(expected)
    djur(db, _input=fakes.fake_input, _print=fakes.fake_print)
    fakes.verify_interaction_consumed()


def test_confirm_interaction():
    expected = """\
INP y
PRN Jag förstår bara svenska; (J)a eller (N)ej?
INP no""".splitlines()
    fakes = InteractionTest(expected)
    assert False == confirm(_input=fakes.fake_input, _print=fakes.fake_print)
    fakes.verify_interaction_consumed()

    expected = """\
INP Ja""".splitlines()
    fakes = InteractionTest(expected)
    assert True == confirm(_input=fakes.fake_input, _print=fakes.fake_print)
    fakes.verify_interaction_consumed()


class InteractionTest:

    def __init__(self, expected_log):
        self.fake_answers = self.filter_inp(expected_log)
        self.expected_log = list(expected_log)
        self.logs = 0
        self.got = []

    def fake_input(self):
        next_answer = self.fake_answers.pop(0)
        self.add_actual(f"INP {next_answer}")
        return next_answer

    def fake_print(self, msg):
        collect = f"PRN {msg}"
        expected_print = self.expected_log[self.logs]
        if collect != expected_print:
            print(f"Failed at end of:")
            print('\n'.join(self.expected_log[self.logs-3:self.logs]))
            print(f"{expected_print} (got: {collect})")
            raise Exception()
        self.add_actual(collect)

    def add_actual(self, msg):
        self.logs += 1
        self.got.append(msg)

    def get_actual(self):
        return self.got

    def verify_interaction_consumed(self):
        if not len(self.got) == len(self.expected_log):
            print(f"Too short log produced, e.g these lines were expected")
            print('\n'.join(self.expected_log[self.logs:self.logs+3]))

    @staticmethod
    def filter_inp(full_log):
        return [x.partition(' ')[2] for x in full_log if x.startswith('INP')]


def test_filter_inp():
    log = """\
INP j
PRN Vad kul! :D :D :D
PRN (S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.
INP S
PRN Tänk på ett djur, så ska jag gissa vilket du tänker på!
PRN När du tänkt klart, skriv (K)lart.
INP k
PRN OK då kör vi...
PRN Kan djuret simma - (J)a eller (N)ej?
INP n
PRN Krälar djuret - (J)a eller (N)ej?
INP j
PRN Jag gissar att du tänkte på orm!
PRN Hade jag rätt? (J)a eller (N)ej?
INP j
PRN Vad kul! :D :D :D
PRN (S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.
INP a
PRN Tack för att du spelade!""".splitlines()
    assert InteractionTest.filter_inp(log) == [
        'j', 'S', 'k', 'n', 'j', 'j', 'a'
    ]


# önskvärda features |||
## svar med både "n" och "j" som vänster krok
## uppdateringsalgoritm/interaktion
# djurformattering exvis "GÄDDA " --> "gädda"
# frågeformattering exvis "kan den flyga?" -> "Kan den flyga"
# persistens
