from tabela import Tabela, uradi_sve

atributi = ["Ime", "Kosa", "Visina", "Masa", "Koristi zaštitnu kremu", "Izgoreo/la"]

podaci = [
    ["Aleksa", "Plava", "Prosečna", "Laka", "Ne", "Da"],
    ["Bojan", "Plava", "Visoka", "Prosečna", "Da", "Ne"],
    ["Ceca", "Braon", "Niska", "Prosečna", "Da", "Ne"],
    ["Darko", "Plava", "Niska", "Prosečna", "Ne", "Da"],
    ["Ema", "Crvena", "Prosečna", "Teška", "Ne", "Da"],
    ["Filip", "Braon", "Visoka", "Teška", "Ne", "Ne"],
    ["Goran", "Braon", "Prosečna", "Teška", "Ne", "Ne"],
    ["Helena", "Plava", "Niska", "Laka", "Da", "Ne"],
]

tabela = Tabela(atributi, podaci, "Ime", atributi[1:-1], "Izgoreo/la")

uradi_sve(tabela)
