import networkx as nx

"""
Podamos los grafo que solo tengan grado 1 ya que hemos partido de un influencer 
inicialy podemos sobreentender que todos siguen a ese (de esta manera ahorramos 
recursos facilitando los calculos)
"""
G = nx.read_gml('./grafo.gml')
G = G.to_undirected()

"""
    k_core saca subgrafos masximales que contengan nodos de grado k o mayor
    lo pasamos a no dirigido
"""
G= nx.k_core(G,k=2)

nx.write_gml(G, 'grafo_con_poda.gml')
