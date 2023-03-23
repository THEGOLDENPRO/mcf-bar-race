from novauniverse import MCF, Search

mcf = MCF().search(Search(name="2022-02-05"))

for player in mcf.players:
    print(player)