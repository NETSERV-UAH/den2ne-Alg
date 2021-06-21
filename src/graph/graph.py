#!/usr/bin/python3

from node import Node
from link import Link


class Graph(object):
    """
        Clase para gestionar el gráfo que representará la red de distribución eléctrica 
    """

    def __init__(self, state, loads, edges, switches, root=150):
        """
            Constructor de la clase Graph el cual conformará el grafo a partir de los datos procesados.
        """
        self.root = root
        self.nodes = list()
        self.buildGraph()

    def buildGraph(self, delta, loads, edges, switches):
        """
            Función para generar el grafo
        """

        # Primero vamos a añadir todos los nodos normales del grafo, ya que los tenemos listados con sus cargas en loads.
        for node in loads:
            self.nodes.append(Node(node, Node.NORMAL, loads[node][delta]))

        # A continuación, vamos a añadir a esos nodos normales sus vecinos.
        # Pero ojo, pueden ser virtuales. Un nodo es virtual si aparece en un enlace
        # pero este no es productor ni consumidor. En caso de ser virtual, vamos a ver que enlace
        # tipo switch tiene asociado.
        for node in self.nodes:
            if node.type == Node.NORMAL:
                links = [match_links for edge in edges if edge["node_a"] == node.name]

                # Vamos a ver si hay que añadir algun nodo virtual y añadimos los vecinos al nodo normal
                for link in links:
                    if [match_virtual_nodes for nodes in self.nodes if nodes.name == link["node_b"]] is None:
                        self.nodes.append(Node(link["node_b"], Node.VIRTUAL, 0))

                    # Añadimos los vecinos
                    node.addNeigbor(self.findNode(link["node_b"]), Link.NORMAL, Link.CLOSED, link["dist"], link["cap"])

            elif node.type == Node.VIRTUAL:
                pass

    def findNode(self, name):
        """
            Funcion para buscar un nodo en la lista del grafo
        """

        for node in self.nodes:
            if node.name == name:
                return node

        return None
