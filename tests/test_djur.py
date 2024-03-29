# coding: utf-8
import json
from pathlib import Path
from pprint import pprint

from src.djur import (
    confirm,
    djur,
    dotgraph,
    find_leaves,
    find_nodes,
    format_animal,
    format_question,
)


def run_session(db, fakes):
    djur(
        db,
        _input=fakes.fake_input,
        _print=fakes.fake_print,
        _save_db=fakes.fake_save,
    )


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
    run_session(['häst'], fakes)
    fakes.verify_interaction_consumed()


def test_approval_test_game_correct_guesses():

    db = [
        'Kan djuret simma', True,
        ['gädda'],
        ['Krälar djuret', False, ['örn'], ['orm']]
    ]

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
PRN Kan djuret simma? Svara med (J)a eller (N)ej.
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
PRN Kan djuret simma? Svara med (J)a eller (N)ej.
INP n
PRN Krälar djuret? Svara med (J)a eller (N)ej.
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
    run_session(db, fakes)
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
PRN Kan djuret simma? Svara med (J)a eller (N)ej.
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
    run_session(db, fakes)
    fakes.verify_interaction_consumed()


def test_confirm_interaction():
    expected = """\
INP y
PRN Jag förstår bara svenska; (J)a eller (N)ej?
INP no""".splitlines()
    fakes = InteractionTest(expected)
    assert confirm(_input=fakes.fake_input, _print=fakes.fake_print) is False
    fakes.verify_interaction_consumed()

    expected = """\
INP Ja""".splitlines()
    fakes = InteractionTest(expected)
    assert confirm(_input=fakes.fake_input, _print=fakes.fake_print) is True
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

    def fake_save(self, db):
        pass

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
PRN Kan djuret simma? Svara med (J)a eller (N)ej.
INP n
PRN Krälar djuret? Svara med (J)a eller (N)ej.
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


def test_format_animal():
    testdb_path = Path().absolute() / 'tests/testdata/djur.json'
    testdb = json.loads(testdb_path.read_text())
    raw_animals = """\
Padda
Schimpans
blå val
fiskmås
gädda
hund
häst
igelkott
katt
mus
orm
skölpadda
varg
örn""".splitlines()
    assert raw_animals == sorted(list(find_leaves(testdb)))
    formatted_animals = """\
blå val
fiskmås
gädda
hund
häst
igelkott
katt
mus
orm
padda
schimpans
skölpadda
varg
örn
""".splitlines()
    assert formatted_animals == sorted(format_animal(x) for x in raw_animals)


def test_format_questions():
    testdb_path = Path().absolute() / 'tests/testdata/djur.json'
    testdb = json.loads(testdb_path.read_text())
    raw_questions = """\
Kan djuret flyga?
Kan djuret hoppa?
Kan djuret simma
Krälar djuret
flyter djuret på vatten?
har djuret ett skal på rygen?
har djuret svans?
har djuret tagar på rygen?
kan djuret klättra?
är djuret störe än en buss
är djuret vilt?
äter djuret hö?
äter djuret ost?
""".splitlines()
    assert raw_questions == sorted(list(find_nodes(testdb)))
    formatted_questions = """\
Flyter djuret på vatten?
Har djuret ett skal på rygen?
Har djuret svans?
Har djuret tagar på rygen?
Kan djuret flyga?
Kan djuret hoppa?
Kan djuret klättra?
Kan djuret simma?
Krälar djuret?
Är djuret störe än en buss?
Är djuret vilt?
Äter djuret hö?
Äter djuret ost?
""".splitlines()
    assert formatted_questions == sorted(format_question(x) for x in raw_questions)

def test_dotgraph():
    db = [
        'Kan djuret simma', True,   #q1
        ['gädda'],   # a1
        ['Krälar djuret', False, ['örn'], ['orm']] #q2, a2, a3
    ]
    #  Skiss:
    #     q1
    #  a1    q2
    #       a2 a3
    # print(dotgraph(db))
    assert dotgraph(db) == """\
digraph djur {
n0 [label="Kan djuret simma"];
n1 [label="gädda"];
n2 [label="Krälar djuret"];
n3 [label="örn"];
n4 [label="orm"];
n0 -> n1;
n0 -> n2;
n2 -> n3;
n2 -> n4;
}"""
# önskvärda features |||
# --graph option
