#!/usr/bin/python3

from .node import Node
from .link import Link
import networkx as nx
import matplotlib.pyplot as plt


class Graph(object):
    """
        Clase para gestionar el gráfo que representará la red de distribución eléctrica
    """

    def __init__(self, delta, loads, edges, switches, root='150'):
        """
            Constructor de la clase Graph el cual conformará el grafo a partir de los datos procesados.
        """
        self.nodes = list()
        self.root = root
        self.sw_config = self.buildSwitchConfig(switches)
        self.buildGraph(delta, loads, edges, switches)

    def buildGraph(self, delta, loads, edges, switches):
        """
            Función para generar el grafo
        """

        # Primero vamos a añadir todos los nodos normales del grafo, ya que los tenemos listados con sus cargas en loads.
        for node in loads:
            self.nodes.append(Node(node, Node.NORMAL, loads[node][delta]))

        # Acto seguido vamos añadir todos los nodos virtuales
        for edge in edges:
            if self.findNode(edge["node_a"]) is None:
                self.nodes.append(Node(edge["node_a"], Node.VIRTUAL, 0))
            elif self.findNode(edge["node_b"]) is None:
                self.nodes.append(Node(edge["node_b"], Node.VIRTUAL, 0))

        for sw_edge in switches:
            if self.findNode(sw_edge["node_a"]) is None:
                self.nodes.append(Node(sw_edge["node_a"], Node.VIRTUAL, 0))
            elif self.findNode(sw_edge["node_b"]) is None:
                self.nodes.append(Node(sw_edge["node_b"], Node.VIRTUAL, 0))

        # A continuación, vamos a añadir a los nodos sus vecinos. Cada enlace es bi-direccional.
        for edge in edges:
            self.nodes[(self.findNode(edge["node_a"])[0])].addNeighbor(edge["node_b"], Link.NORMAL, 'closed', edge["dist"], edge["cap"])
            self.nodes[(self.findNode(edge["node_b"])[0])].addNeighbor(edge["node_a"], Link.NORMAL, 'closed', edge["dist"], edge["cap"])

        for sw_edge in switches:
            self.nodes[self.findNode(sw_edge["node_a"])[0]].addNeighbor(sw_edge["node_b"], Link.SWITCH, sw_edge["state"], 0, 3)
            self.nodes[self.findNode(sw_edge["node_b"])[0]].addNeighbor(sw_edge["node_a"], Link.SWITCH, sw_edge["state"], 0, 3)


    def buildSwitchConfig(self, switch):
        """
            Función para procesar la configuración inicial de los enlaces switch
        """
        
        # Nos creamos una variable auxiliar a devolver
        sw_config = dict()

        for sw_links in switch:
            sw_config[switch.index(sw_links)] = sw_links

        return sw_config

    def findNode(self, name):
        """
            Funcion para buscar un nodo en la lista del grafo
        """

        for node in self.nodes:
            if node.name == name:
                return [self.nodes.index(node), node]

        return None

    def removeNode(self, name):
        """
            Funcion para eliminar un nodo del grafo
        """

        for node in self.nodes:
            if node.name == name:

                # Primero vamos a los vecinos y eleminimos los enlaces con el
                for neighbor in node.neighbors:
                    # Obtenemos el index a eliminar (Es necesario para los enlaces por ser objs, no vale hacer un remove)
                    index_del = self.nodes[self.findNode(neighbor)[0]].neighbors.index(node.name)

                    # Machacamos el nodo a eliminar como vecino, y con el index, eliminamos el enlace con el.
                    self.nodes[self.findNode(neighbor)[0]].neighbors.remove(node.name)
                    del self.nodes[self.findNode(neighbor)[0]].links[index_del]

                # Por último eliminamos el nodo de la lista del grafo
                self.nodes.remove(node)
                break

    def pruneGraph(self):
        """
            Method to automagically prune the graph.

            Returns:
                list: A list of the IDs of the nodes that have been pruned.
        """

        nodes_to_prune = {
            'sweep_1': [],
            'sweep_2': []
        }

        # First sweep
        for node in self.nodes:
            if (
                node.type == Node.VIRTUAL and
                node.name != self.root and
                len(node.links) == 1 and
                node.links[0].type == Link.SWITCH
            ):
                nodes_to_prune['sweep_1'].append(node.name)

        for node in nodes_to_prune['sweep_1']:
            self.removeNode(node)

        # Second sweep
        for node in self.nodes:
            if (
                node.type == Node.VIRTUAL and
                len(node.links) == 1 and
                node.links[0].type == Link.NORMAL
            ):
                nodes_to_prune['sweep_2'].append(node.name)

        for node in nodes_to_prune['sweep_2']:
            self.removeNode(node)

        return nodes_to_prune['sweep_1'] + nodes_to_prune['sweep_2']


    def plotGraph(self, positions, title):
        """
            Funcion para pintar el grafo
        """
        G_nx = nx.Graph()
        color_map = []

        for node in self.nodes:
            for link in node.links:
                G_nx.add_edge(
                    node.name, node.neighbors[node.links.index(link)], type_link=link.type, status=link.state)

        edge_normal = [(u, v) for (u, v, d) in G_nx.edges(data=True) if d["type_link"] == Link.NORMAL]
        edge_switch_open = [(u, v) for (u, v, d) in G_nx.edges(data=True) if d["type_link"] == Link.SWITCH and d["status"] == 'open']
        edge_switch_closed = [(u, v) for (u, v, d) in G_nx.edges(data=True) if d["type_link"] == Link.SWITCH and d["status"] == 'closed']

        pos = nx.spring_layout(G_nx, k=0.2)

        for position in positions:
            pos[position["node"]] = (position["x"], -position["y"])

        for node in G_nx:
            if self.findNode(node)[1].type == Node.NORMAL:
                color_map.append('#19affa')
            else:
                color_map.append('#95e8d6')

        fig = plt.figure()
        nx.draw_networkx_nodes(G_nx, pos, node_color=color_map, node_size=270)
        nx.draw_networkx_edges(G_nx, pos, edgelist=edge_normal, width=2)
        nx.draw_networkx_edges(G_nx, pos, edgelist=edge_switch_open, width=2, alpha=0.5, edge_color="g", style="dashed")
        nx.draw_networkx_edges(G_nx, pos, edgelist=edge_switch_closed, width=2, alpha=0.5, edge_color="r", style="dashed")
        nx.draw_networkx_labels(G_nx, pos, font_size=10, font_family="sans-serif")

        plt.axis("off")
        plt.title(title)
        plt.plot()

    @staticmethod
    def showGraph():
        """
            Función para representar las figuras generadas, para no bloquear el flujo de ejecución
        """
        # He estado a nada de meterme con threads y subprocesos con la librería de python de multiprocessing..
        # Mejor lo de dejamos así para ahorrar tiempo. Que sea el usuario quien decida cuando bloquear la ejecución..
        plt.show()
