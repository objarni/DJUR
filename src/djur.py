# coding: utf-8
import json
import pathlib


DBPATH = 'djur.json'


def save(db):
    try:
        pathlib.Path(DBPATH).write_text(json.dumps(db, indent=2))
    except:
        print(f"Kunde inte spara filen {DBPATH} :(")


def djur(db, _input=input, _print=print, _save_db=save):

    def inp():
        print(">>> ", end='')
        ans = _input().lower()
        return ans[0] if len(ans) > 0 else ' '

    def full_inp():
        print(">>> ", end='')
        return _input()

    _print("Välkommen till GISSA DJUR!")
    _print("--------------------------")
    while True:
        antal = count(db)
        _print(f"Jag känner till {antal} djur.")
        _print("(S)pela eller (A)vsluta? Tryck S eller A och sedan Enter.")
        ans = inp()
        if ans == 'a':
            _print("Tack för att du spelade!")
            return
        elif ans == 's':
            _print("Tänk på ett djur, så ska jag gissa vilket du tänker på!")
            _print("När du tänkt klart, skriv (K)lart.")
            while inp() != 'k':
                _print("Va? Skriv k när du är klar!")
            _print("OK då kör vi...")
            pos = db
            # Questions are 4 length tuples!
            while len(pos) == 4:
                question = format_question(pos[0])
                _print(f"{question} Svara med (J)a eller (N)ej.")
                go_left = confirm(full_inp, _print)
                go_left = go_left if pos[1] else not go_left
                if go_left:
                    pos = pos[2]
                else:
                    pos = pos[3]
            djur = format_animal(pos[0])
            _print(f"Jag gissar att du tänkte på {djur}!")
            _print("Hade jag rätt? (J)a eller (N)ej?")
            if confirm(full_inp, _print):
                _print("Vad kul! :D :D :D")
            else:
                _print("OK, men vilket djur tänkte du på då?")
                new_djur = format_animal(full_inp())
                _print(f"Kom på en fråga som innehåller ordet 'djuret',")
                _print(f"som skiljer {new_djur} och {djur} åt.")
                _print("T.ex. 'Kan djuret simma?'")
                while True:
                    new_question = format_question(full_inp())
                    if 'djuret' not in new_question:
                        _print("Snälla ta med ordet 'djuret' i frågan!")
                        _print("Försök igen:")
                    else:
                        break
                readable_question = new_question.replace("djuret", new_djur)
                _print(
                    f"OK, och för {new_djur} är svaret på frågan '{readable_question}' (J)a eller (N)ej?")
                ans = confirm(full_inp, _print)
                while True:
                    _print("Denna fråga lär jag mig då:")
                    _print(f"  {readable_question}")
                    _print(f"  Rätt svar: {swedish_bool(ans)}")
                    _print("Ser det rätt ut?")
                    yes = confirm(full_inp, _print)
                    if yes:
                        break
                    else:
                        _print("Hmm, tvärtom alltså?")
                        ans = not ans

                _print(f"Tack för att du lärt mig något om djuret {new_djur}!")
                pos[:] = [new_question, ans, [new_djur], [djur]]

                _save_db(db)
        else:
            _print(f"Jag förstår inte '{ans}'!")


def confirm(_input=input, _print=print):
    while True:
        ans = _input().lower()
        if len(ans) > 0 and ans[0] in 'jn':
            return ans[0] == 'j'
        else:
            _print("Jag förstår bara svenska; (J)a eller (N)ej?")


def find_leaves(db):
    if len(db) == 1:
        yield db[0]
    else:
        for leaf in find_leaves(db[2]):
            yield leaf
        for leaf in find_leaves(db[3]):
            yield leaf


def find_nodes(db):
    if len(db) == 4:
        yield db[0]
        for node in find_nodes(db[2]):
            yield node
        for node in find_nodes(db[3]):
            yield node


def format_animal(a):
    return a.lower().strip()


def format_question(q):
    words = q.split()
    q = words[0].title() + ' ' + ' '.join(words[1:])
    if not q.endswith('?'):
        q = q + '?'
    return q


def count(db):
    return len(list(find_leaves(db)))


def swedish_bool(b):
    return 'ja' if b else 'nej'


def dfs(db, cb):
    cb(db)
    if len(db) == 4:
        dfs(db[2], cb)
        dfs(db[3], cb)


def dotgraph(db):
    """Return a DOT compatible string representation of db"""
    labels = []
    dfs(db, lambda node: labels.append(node[0]))
    lbls = [f'n{num} [label="{s}"];\n' for (num, s) in enumerate(labels)]
    print(labels)
    edges = []
    def visit_node(node):
        if len(node) == 4:
            parent_ix = labels.index(node[0])
            lchild_ix = labels.index(node[2][0])
            rchild_ix = labels.index(node[3][0])
            edges.append((parent_ix, lchild_ix))
            edges.append((parent_ix, rchild_ix))
    dfs(db, visit_node)
    edges = [f'n{parent} -> n{child};\n' for (parent, child) in edges]
    print(edges)
    return "digraph djur {\n" + ''.join(lbls) + ''.join(edges) + "}"


if __name__ == '__main__':
    print("\n" * 100)
    try:
        db = json.loads(pathlib.Path(DBPATH).read_text())
    except:
        db = [
            'Kan djuret simma', True,
            ['gädda'],
            ['Krälar djuret', False, ['örn'], ['orm']]
        ]
    print(dotgraph(db))
    djur(db)
