import json
import networkx as nx

"""
    Creamos el digrafo sabiendo que tanto las claves como los valores son nodos
    y la arista va desde el influencer al seguidor (el influencer influye al seguidor)
"""

f = open('./result.json')

data = json.load(f)

nodos = set()
 
G = nx.DiGraph()


data = {str(key): [str(val) for val in vals] for key, vals in data.items()}
for influencer, seguidores in data.items():
    G.add_node(influencer)
    for seguidor in seguidores:
        G.add_node(seguidor)
        if not G.has_edge(influencer, seguidor):
            G.add_edge(influencer, seguidor)


nx.write_gml(G, "grafo.gml")


