###########################
#       Trabalho 3        #
# Autor: Diego S. Seabra  #
# Matrícula: 0040251      #
# #########################

# Importações
import sys
import time
from collections import defaultdict

# Cria um grafo conforme lista de arestas passadas
def cria_grafo(arestas):
    grafo = defaultdict(list)
    arestas_visitadas = defaultdict(int)
    for origem, destino, weight in arestas:
        arestas_visitadas[(origem, destino, weight)] += 1
        if arestas_visitadas[(origem, destino, weight)] > 1:  
            continue
        grafo[origem].append((destino, weight))
        grafo[destino].append((origem, weight))  
    return grafo

def nos_filtrados(grafo):
    vertices = []
    for n in grafo:
        vertices.append(n)
        vertices += [x[0] for x in grafo[n]]

    q = set(vertices)
    return q

# Executa o algoritmo de Dijkstra dado uma origem e um destino
def dijkstra(grafo, origem, destino=None):
    vertices = []
    for n in grafo:
        vertices.append(n)
        vertices += [x[0] for x in grafo[n]]

    q = set(vertices)
    vertices = list(q)
    distancia = dict()
    antecessor = dict()
    for n in vertices:
        distancia[n] = float('inf')
        antecessor[n] = None

    distancia[origem] = 0

    while q:
        u = min(q, key=distancia.get)
        q.remove(u)

        if destino is not None and u == destino:
            return distancia[destino], antecessor

        for v, w in grafo.get(u, ()):
            alt = distancia[u] + w
            if alt < distancia[v]:
                distancia[v] = alt
                antecessor[v] = u

    return distancia, antecessor

def menor_caminho(pr, vertice):  
    p = []
    while vertice is not None:
        p.append(vertice)
        vertice = pr[vertice]
    return p[::-1]

def main(argv):
    # Salva o caminho do arquivo
    arquivo = argv[0]

    print("##########################")
    print("#   Trabalho Prático 3   #")
    print("#                        #")
    print("# Aluno: Diego S. Seabra #")
    print("# Matrícula: 0040251     #")
    print("##########################")
    print("")

    # Pede ao usuário os vértices de ORIGEM e DESTINO
    origem = input("Digite o vértice de ORIGEM:\n")
    destino = input("\nDigite o vértice de DESTINO:\n(deixe em branco caso queira que o cálculo seja realizado para os DEMAIS VÉRTICES)\n")

    # Abre o arquivo
    with open(arquivo, "r") as fd:
        # Pula as 2 primeiras linhas
        next(fd)
        next(fd)

        # Inicializa uma lista de arestas
        arestas = []

        # Percorre as linhas do arquivo
        for line in fd:
            # Separa a linha em 3 "partes"
            line = line.strip().split('\t')
            
            # Cria um tuple
            # Contendo: Origem, Destino e Peso
            aresta = (str(line[0]), str(line[1]), int(line[2]))
            arestas.append(aresta)

        # Se o usuário digitou ORIGEM e DESTINO
        if origem is not '' and destino is not '':
            # Cria o grafo e a lista de nós filtrados
            g = cria_grafo(arestas)
            nos = nos_filtrados(g)

            # Calcula o menor caminho
            d, antecessor = dijkstra(g, str(origem), str(destino))
            caminho = menor_caminho(antecessor, str(destino))

            # Imprime os resultados para o usuário
            print('=== Menor Caminho (Origem -> Destino) ===')
            print('{} -> {} | distancia: {} | menor caminho: {}'.format(origem, destino, d, caminho))

        # Se o usuário digitou somente ORIGEM
        if origem is not '' and destino is '':
            print("Digitou somente origem")

        # print('=== Caminho Minimo (Origem -> Destino) ===')

        # print('')
        # print('=== Matriz Distancias ===')
        # header = '\t'
        # distancias = ''
        # for no in nos:
        #     ds, antecessor = dijkstra(g, no)
        #     header += no + '\t'
        #     distancias += no + '\t'
        #     for k in ds:
        #         distancias += str(ds[k]) + '\t'
        #     distancias += '\n'

        # print(nos)

    # Fecha o arquivo
    fd.close()

if __name__ == "__main__":
   main(sys.argv[1:])