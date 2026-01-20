import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        try:
            n_alb = int(self._view.txtNumAlbumMin.value)
        except ValueError:
            self._view.show_alert("Inserire un numero di album valido")
            return

        self._model.load_all_artists()
        self._model.load_artists_with_min_albums(n_alb)
        self._model.build_graph()

        self._view.ddArtist.options = [ft.dropdown.Option(a.title) for a in self._model._artists_list]
        self._view._btnCreateGraph.controls.clear()
        self._view._btnCreateGraph.controls.append(
            ft.Text(f"Grafo creato: {len(self._model._graph.nodes)} nodi(artisti), {len(self._model._graph.edges)} archi")
        )
        self._view.update()

    def handle_connected_artists(self, e):
        pass
    def handle_interfaccia(self, e):
        try:
            d_min = float(self._view.txtMaxArtists.value)
        except ValueError:
            self._view.show_alert("Inserire un numero di artisti  valido")
            return

