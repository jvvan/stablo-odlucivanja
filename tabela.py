import math
import json
from python_mermaid.diagram import MermaidDiagram, Node, Link
from base64 import b64encode


def izracunaj_entropiju(podaci: list, atribut: int) -> float:
    ukupno = len(podaci)
    brojaci = {}

    # Broj svake odluke
    for red in podaci:
        odluka = red[atribut]
        if odluka not in brojaci:
            brojaci[odluka] = 0
        brojaci[odluka] += 1

    # Izracunaj entropiju
    entropija = 0
    for broj in brojaci.values():
        procenat_pojavljivanja = broj / ukupno
        entropija -= procenat_pojavljivanja * math.log2(procenat_pojavljivanja)

    return entropija


def izracunaj_dobit(podaci, atribut, atribut_odluke):
    ukupna_entropija = izracunaj_entropiju(podaci, atribut_odluke)
    ukupno = len(podaci)

    grupe = {}
    for red in podaci:
        vrednost = red[atribut]
        if vrednost not in grupe:
            grupe[vrednost] = []
        grupe[vrednost].append(red)

    # Entropija za svaku grupu
    entropija = 0
    for grupa in grupe.values():
        entropija += len(grupa) / ukupno * izracunaj_entropiju(grupa, atribut_odluke)

    # Koliko se entropija smanjila
    return ukupna_entropija - entropija


class Tabela:
    def __init__(
        self, atributi, podaci, atribut_imena, atributi_vrednosti, atribut_odluke
    ):
        self.atributi = atributi
        self.podaci = podaci
        self.atribut_imena = atribut_imena
        self.atributi_vrednosti = atributi_vrednosti
        self.atribut_odluke = atribut_odluke


def napravi_stablo(tabela):
    atribut_odluke = tabela.atributi.index(tabela.atribut_odluke)
    moguce_odluke = [row[atribut_odluke] for row in tabela.podaci]

    # Sve odluke su iste
    if all(decision == moguce_odluke[0] for decision in moguce_odluke):
        return moguce_odluke[0]

    # Nema vise atributa za podelu
    if not tabela.atributi_vrednosti:
        return max(set(moguce_odluke), key=moguce_odluke.count)

    # Najbolji atribut za podelu, onaj koji ima najvecu dobit
    najbolji_atribut = max(
        tabela.atributi_vrednosti,
        key=lambda atribut: izracunaj_dobit(
            tabela.podaci, tabela.atributi.index(atribut), atribut_odluke
        ),
    )

    stablo = {najbolji_atribut: {}}

    # Grupisi redove po vrednosti najboljeg atributa
    najbolji_atribut_idx = tabela.atributi.index(najbolji_atribut)
    vrednosti = set(row[najbolji_atribut_idx] for row in tabela.podaci)

    for vrednost in vrednosti:
        podskup = [
            red for red in tabela.podaci if red[najbolji_atribut_idx] == vrednost
        ]
        if not podskup:
            stablo[najbolji_atribut][vrednost] = max(
                set(moguce_odluke), key=moguce_odluke.count
            )
        else:
            stablo[najbolji_atribut][vrednost] = napravi_stablo(
                Tabela(
                    tabela.atributi,
                    podskup,
                    tabela.atribut_imena,
                    [
                        attr
                        for attr in tabela.atributi_vrednosti
                        if attr != najbolji_atribut
                    ],
                    tabela.atribut_odluke,
                )
            )

    return stablo


def prikazi_stablo(tabela, stablo, nivo=0, trenutni_podaci=None):
    indent = "    " * nivo

    if trenutni_podaci is None:
        trenutni_podaci = tabela.podaci

    if isinstance(stablo, dict):
        for atribut, grane in stablo.items():
            for vrednost, podstablo in grane.items():
                print(f"{indent}{atribut} == {vrednost}?")

                index = tabela.atributi.index(atribut)

                novi_podaci = [red for red in trenutni_podaci if red[index] == vrednost]

                prikazi_stablo(tabela, podstablo, nivo + 1, novi_podaci)
    else:
        print(f"{indent}{tabela.atribut_odluke}: {stablo}")
        index = tabela.atributi.index(tabela.atribut_imena)
        for red in trenutni_podaci:
            print(f"{indent}  - {red[index]}")


def napravi_mermaid_stablo(stablo, tabela, naziv="Stablo Odluke"):
    nodes = []
    links = []

    def dodaj_granu(stablo, roditelj=None):
        if isinstance(stablo, dict):
            for atribut, grane in stablo.items():
                for vrednost_grane, podstablo in grane.items():
                    trenutni_cvor = Node(
                        f"{atribut}_{vrednost_grane}", f"{atribut} == {vrednost_grane}"
                    )
                    nodes.append(trenutni_cvor)

                    if roditelj:
                        links.append(Link(roditelj, trenutni_cvor))

                    dodaj_granu(podstablo, trenutni_cvor)
        else:
            odgovor_cvor = Node(
                f"odluka_{stablo}", f"{tabela.atribut_odluke} - {stablo}"
            )
            nodes.append(odgovor_cvor)

            if roditelj:
                links.append(Link(roditelj, odgovor_cvor))

    dodaj_granu(stablo)

    chart = MermaidDiagram(title=naziv, nodes=nodes, links=links)

    return str(chart)


def napravi_mermaid_url(mermaid_str):
    data = {
        "code": mermaid_str,
        "mermaid": '{\n  "theme": "dark"\n}',
    }

    encoded_str = b64encode(json.dumps(data).encode()).decode()

    mermaid_url = f"https://mermaid.live/edit#{encoded_str}"
    return mermaid_url


def uradi_sve(tabela):
    stablo = napravi_stablo(tabela)
    prikazi_stablo(tabela, stablo)
    mermaid = napravi_mermaid_stablo(stablo, tabela)
    print("\n\nMermaid Link:")
    print(napravi_mermaid_url(mermaid))
