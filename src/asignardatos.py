import random
"""
    Por ahora, para tener distintas formas de producir numeros aleatorios
"""
def conf_edges_aleatorio():
    edges_conf = dict()
    n_conf = random.randint(5, 20)
    for i in range(n_conf):
        edges_conf[i] = dict()
        edges_conf[i]['coef_r'] = random.uniform(0, 2.5)
        edges_conf[i]['i_max'] = random.randint(40, 200)
        edges_conf[i]['section'] = random.randint(0, 100) #Este no lo entiendo muy bien, si ya genero las posiciones en brite, ¿hace falta?
    return edges_conf

def cargas_aleatorias(nodos):
    cargas = list()
    for i in range(nodos):
        cargas.append(random.uniform(-4, 4))
    return cargas

#Ahora con un distribución normal
#Los valores estan puestos más o menos a ojo
def conf_edges_gauss():
    edges_conf = dict()
    n_conf = int(random.gauss(10, 2))
    for i in range(n_conf):
        edges_conf[i] = dict()
        edges_conf[i]['coef_r'] = random.gauss(1.25, 0.4)
        edges_conf[i]['i_max'] = int(random.gauss(100, 30))
        edges_conf[i]['section'] = int(random.gauss(50, 20)) #Este no lo entiendo muy bien, si ya genero las posiciones en brite, ¿hace falta?
    return edges_conf

def cargas_gauss(nodos):
    cargas = list()
    for i in range(nodos):
        cargas.append(random.gauss(0, 1.5))
    return cargas

#Ahora con un distribución gamma
#Los valores estan puestos más o menos a ojo
def conf_edges_gamma():
    edges_conf = dict()
    n_conf = int(random.gammavariate(15, 0.6))
    for i in range(n_conf):
        edges_conf[i] = dict()
        edges_conf[i]['coef_r'] = random.gammavariate(1, 0.6)
        edges_conf[i]['i_max'] = int(random.gammavariate(25, 4))
        edges_conf[i]['section'] = int(random.gammavariate(4, 10)) #Este no lo entiendo muy bien, si ya genero las posiciones en brite, ¿hace falta?
    return edges_conf
#Para las cargas lo hago tambien con la normal porque la gamma da solo positivos
#def cargas_gamma(nodos):
#    cargas = list()
#    for i in range(nodos):
#        cargas.append(random.gammavariate(2, 1.1))
#    return cargas
