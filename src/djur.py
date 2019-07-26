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

    antal = count(db)

    prn = _print or print
    prn("Välkommen till GISSA DJUR!")
    prn("--------------------------")
    prn(f"Jag känner till {antal} djur.")
    while True:
        prn("(S)pela eller (A)vsluta?")
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
            prn(f"Jag förstår inte '{ans}'!")


if __name__ == '__main__':
    print("\n" * 100)
    db = (
        'Kan djuret simma', 'j',
        ('gädda',),
        ('Krälar djuret', 'n', ('örn',), ('orm',))
    )
    djur(db)
