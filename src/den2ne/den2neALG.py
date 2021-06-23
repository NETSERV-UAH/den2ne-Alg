#!/usr/bin/python3

from .den2neHLMAC import HLMAC
from ..graph.graph import Graph


class Den2ne(object):
    """
        Clase para gestionar la lógica del algoritmo
    """

    def __init__(self, graft, root='150'):
        """
            Constructor de la clase Den2ne 
        """
        self.G = graft
        self.root = root

    def spread_ids(self):
        """
            Funcion para difundir los IDs entre todos los nodos del grafo
        """

        # Var aux: lista con los nodos que debemos visitar (Va a funcionar como una pila)
        nodes_to_attend = list()

        # Empezamos por el root, como no tiene padre el root, su HLMAC parent addr es None -> No hereda
        self.G.findNode(self.root).ids.append(HLMAC(None, self.root))

        # El primero en ser visitado es el root
        nodes_to_attend.append(self.root)

        # Mientras haya nodos a visitar...
        while len(nodes_to_attend) > 0:

            # Iteramos por los vecinos del primer nodo a atender
            for neighbor in self.G.findNode(nodes_to_attend[0]).neighbors:

                # No entiendo muy bien por que se tiene que heredar unicamente la ultima ID.. yo iteraría por todas
                for i in range(0, len(nodes_to_attend[0]).ids):

                    # Vamos a comprobar antes de asignar IDs al vecino, que no hay bucles
                    if HLMAC.hlmac_check_loop(HLMAC(nodes_to_attend[0].ids[i], neighbor.name), neighbor.name):
                        break

                    # Si no hay bucles asignamos la ID al vecino
                    neighbor.ids.append(HLMAC(nodes_to_attend[0].ids[i], neighbor.name))

                # Registramos el vecino emn la pila para ser visitado más adelante
                nodes_to_attend.append(neighbor)

            # Por último desalojamos al nodo atendido
            nodes_to_attend.pop(0)
