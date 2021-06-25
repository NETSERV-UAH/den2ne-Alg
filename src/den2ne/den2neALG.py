#!/usr/bin/python3

from .den2neHLMAC import HLMAC


class Den2ne(object):
    """
        Clase para gestionar la lógica del algoritmo
    """

    def __init__(self, graft):
        """
            Constructor de la clase Den2ne 
        """
        self.G = graft
        self.root = graft.root

    def spread_ids(self):
        """
            Funcion para difundir los IDs entre todos los nodos del grafo
        """

        # Var aux: lista con los nodos que debemos visitar (Va a funcionar como una pila)
        nodes_to_attend = list()

        # Empezamos por el root, como no tiene padre el root, su HLMAC parent addr es None -> No hereda
        self.G.nodes[self.G.findNode(self.root)[0]].ids.append(HLMAC(None, self.root))

        # El primero en ser visitado es el root
        nodes_to_attend.append(self.root)

        # Mientras haya nodos a visitar...
        while len(nodes_to_attend) > 0:

            curr_node = self.G.findNode(nodes_to_attend[0])

            # Iteramos por las posibles IDs disponibles en el nodo
            for i in range(0, len(curr_node[1].ids)):

                if not curr_node[1].ids[i].used:

                    # Iteramos por los vecinos del primer nodo a atender
                    for neighbor in curr_node[1].neighbors:

                        # Vamos a comprobar antes de asignar IDs al vecino, que no hay bucles
                        if HLMAC.hlmac_check_loop(curr_node[1].ids[i], neighbor):
                            pass
                        else:
                            # Si no hay bucles asignamos la ID al vecino
                            self.G.nodes[self.G.findNode(neighbor)[0]].ids.append(HLMAC(curr_node[1].ids[i], neighbor))

                            # Registramos el vecino emn la pila para ser visitado más adelante
                            nodes_to_attend.append(neighbor)

                    # Y tenemos que marcar la HLMAC como que ya ha sido usada
                    self.G.nodes[self.G.findNode(nodes_to_attend[0])[0]].ids[i].used = True

            # Por último desalojamos al nodo atendido
            nodes_to_attend.pop(0)

    def write_ids_report(self, filename):
        """
            Función que genera un fichero de log con el resultado de las asignaciones de las IDs
        """
        with open(filename, 'w') as file:
            for node in self.G.nodes:
                file.write('-------------------------------------------------------------------------')
                file.write('-------------------------------------------------------------------------\n')
                file.write(f'| Node: {node.name}  | Type: {node.type} | Neighbors: {len(node.neighbors)} \n')
                file.write('-------------------------------------------------------------------------')
                file.write('-------------------------------------------------------------------------\n')
                file.write('|  Status  |  ID                                                              \n')
                file.write('-------------------------------------------------------------------------')
                file.write('-------------------------------------------------------------------------\n')
                for id in node.ids:
                    file.write(f'|   {id.used}   |  {HLMAC.hlmac_addr_print(id)} \n')
                file.write('-------------------------------------------------------------------------')
                file.write('-------------------------------------------------------------------------\n')
                file.write('\n')
    
    def write_swConfig_report(self, filename):
        """
            Función que genera un fichero de log con el resultado de la config lógica de la red
        """
        with open(filename, 'w') as file:
            for key in self.G.sw_config:
                file.write('-------------------------------------------------------------------------\n')
                file.write(f'| ID: {key}  | Node A: {self.G.sw_config[key]["node_a"]} | Node B: {self.G.sw_config[key]["node_b"]} | Status: {self.G.sw_config[key]["state"]}                    |\n')
                file.write('-------------------------------------------------------------------------\n')
                file.write('\n')
    
    def write_swConfig_CSV(self, filename):
        """
            Función que genera un fichero CSV con el resultado de la config lógica de la red
        """
        with open(filename, 'w') as file:
            file.write('ID,Node A,Node B,State\n')
            for key in self.G.sw_config:
                file.write(f'{key},{self.G.sw_config[key]["node_a"]},{self.G.sw_config[key]["node_b"]},{self.G.sw_config[key]["state"]}\n')
                
                
