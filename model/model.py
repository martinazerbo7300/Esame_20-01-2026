import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists_list = []
        self.artist_genre_map = {}
        self.load_all_artists()
        self.id_map = {}
        self._nodes = []

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        print(f"Artisti: {self._artists_list}")

    def load_artists_with_min_albums(self, n_alb):
        self._artists_list = DAO.artisti_by_min_albums(n_alb)
        self.id_map = {a.id: a for a in self._artists_list}


    def build_graph(self, n ,e):
        self._graph.clear()
        self._graph.add_nodes_from(self._artists_list)

        for i, a1 in enumerate(self._artists_list):
            for a2 in self._artists_list[i + 1:]:
                if self.artist_genre_map[a1] & self.artist_genre_map[a2]:
                    self._graph.add_edge(a1, a2, weight = w)

    def get_neighbors(self, artist):
        vicini = []
        for n in self._graph.neighbors(artist):
            w = self._graph[artist][n]["weight"]
            vicini.append((n, w))
        return sorted(vicini, key=lambda x: x[1], reverse=True)

    def get_nodes(self):
        return self._graph.nodes()

    def get_edges(self):
        return list(self._graph.edges(data=True))

    def get_num_of_nodes(self):
        return self._graph.number_of_nodes()

    def get_num_of_edges(self):
        return self._graph.number_of_edges()

