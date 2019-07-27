# coding: utf-8

def count(db):
    if len(db) == 1:
        return 1
    else:
        return count(db[2]) + count(db[3])


def djur(db, _input=None, _print=None):
    _inp = _input or input

    def inp():
        print(">>> ", end='')
        ans = _inp().lower()
        return ans[0] if len(ans) > 0 else ' '

    def full_inp():
        print(">>> ", end='')
        return _inp()


    prn = _print or print
    prn("Välkommen till GISSA DJUR!")
    prn("--------------------------")
    while True:
        antal = count(db)
        prn(f"Jag känner till {antal} djur.")
        prn("(S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.")
        ans = inp()
        if ans == 'a':
            prn("Tack för att du spelade!")
            return
        elif ans == 's':
            prn("Tänk på ett djur, så ska jag gissa vilket du tänker på!")
            prn("När du tänkt klart, skriv (K)lart.")
            while inp() != 'k':
                prn("Va? Skriv k när du är klar!")
            prn("OK då kör vi...")
            pos = db
            # Questions are 4 length tuples!
            while len(pos) == 4:
                prn(f"{pos[0]} - (J)a eller (N)ej?")
                ans = inp()
                if ans not in "jn":
                    prn("Jag förstår bara j och n, svenska alltså!")
                    continue
                if ans == pos[1]:
                    pos = pos[2]
                else:
                    pos = pos[3]
            djur = pos[0]
            prn(f"Jag gissar att du tänkte på {djur}!")
            prn("Hade jag rätt? (J)a eller (N)ej?")
            ans = inp()
            if ans == 'j':
                prn("Vad kul! :D :D :D")
            else:
                prn("OK, men vilket djur tänkte du på då?")
                new_djur = full_inp()
                prn(f"Kom på en fråga som skiljer {new_djur} och {djur} åt.")
                prn("T.ex. 'Kan djuret simma?'")
                new_question = full_inp()
                prn(f"OK, och för {new_djur} är svaret på frågan '{new_question}' (J)a eller (N)ej?")
                ans = inp()
                prn(f"Tack för att du lärt mig något om {new_djur}!")
                pos[:] = [new_question, ans, [new_djur], [djur]]
                # from pprint import pprint
                # pprint(db)
        else:
            prn(f"Jag förstår inte '{ans}'!")


if __name__ == '__main__':
    print("\n" * 100)
    db = (
        'Kan djuret simma', 'j',
        ('gädda',),
        ('Krälar djuret', 'n', ('örn',), ('orm',))
    )
    djur(db)
