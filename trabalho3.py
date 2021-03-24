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

# Nós "filtrados"
def nos_filtrados(grafo):
    vertices = []
    for n in grafo:
        vertices.append(n)
        vertices += [x[0] for x in grafo[n]]

    q = set(vertices)
    return q

# Executa o algoritmo de Dijkstra dado uma origem e um destino
# Para os casos em que o grafo é não ponderado, ou seja, não possui
# peso, o peso informado é 0
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

# Faz o cálculo do menor caminho
def menor_caminho(pr, vertice):  
    p = []
    while vertice is not None:
        p.append(vertice)
        vertice = pr[vertice]
    return p[::-1]

def main(argv):
    # Salva o caminho do arquivo
    arquivo = argv[0]

    # Imprime um header simples
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
        # Pula as 2 primeiras linhas do arquivo lido
        next(fd)
        next(fd)

        # Inicializa uma lista de arestas vazia
        arestas = []

        # Percorre as linhas do arquivo
        for line in fd:
            # Separa a linha em 3 "partes" usando TABS
            # É necessário que todo arquivo passado esteja no
            # mesmo formato dos arquivos de teste enviados 
            # (dados separados por TABS)
            line = line.strip().split('\t')
            
            # Verifica se a linha atual possui o elemento de peso
            # (ponderado ou não ponderado)
            if len(line) == 3:
                # Cria uma estrutura contendo: ORIGEM, DESTINO, PESO (caso ponderado)
                aresta = (str(line[0]), str(line[1]), int(line[2]))
                mostraDistancia = True
            else:
                # Cria uma estrutura contendo: ORIGEM, DESTINO (caso não ponderado)
                aresta = (str(line[0]), str(line[1]), 0)
                mostraDistancia = False

            # Adiciona a estrutura da aresta atual na lista de arestas
            arestas.append(aresta)

        # Cria o grafo e a lista de nós
        g = cria_grafo(arestas)
        nos = nos_filtrados(g)

        # Mostra um feedback pro usuário que o 
        # script está rodando
        print("\nCalculando...")

        # Se o usuário digitou ORIGEM e DESTINO
        if origem != '' and destino != '':
            # Inicializa o contador de tempo de execução
            start_time = time.time()

            # Calcula o menor caminho
            d, antecessor = dijkstra(g, str(origem), str(destino))
            caminho = menor_caminho(antecessor, str(destino))

            # Finaliza o contador de tempo de execução
            end_time = time.time()
            tempo_execucao = end_time - start_time

            # Imprime o resultado para o usuário
            print('\n=== Resultado === ')
            if mostraDistancia:
                print('{} -> {} | distancia: {} | tempo execução: {} s | menor caminho: {}'.format(origem, destino, d, round(tempo_execucao,2), caminho))
            else:
                print('{} -> {} | tempo execução: {} s | menor caminho: {}'.format(origem, destino, round(tempo_execucao,2), caminho))

        # Se o usuário digitou somente ORIGEM
        if origem != '' and destino == '':
            # Inicializa o contador de tempo de execução
            start_time_total = time.time()

            print('\n=== Resultado ===')
            # Percorre todos os vértices do grafo
            for n in nos:
                # Se o vértice for igual a origem, não calcula
                if n != origem:
                    # Inicializa o contador de tempo de execução
                    start_time = time.time()

                    # Calcula o menor caminho
                    d, antecessor = dijkstra(g, str(origem), str(n))
                    caminho = menor_caminho(antecessor, str(n))

                    # Finaliza o contador de tempo de execução
                    end_time = time.time()
                    tempo_execucao = end_time - start_time

                    # Imprime o resultado para o usuário
                    if mostraDistancia:
                        print('{} -> {} | distancia: {} | tempo execução: {} s | menor caminho: {}'.format(origem, n, d, round(tempo_execucao,2), caminho))
                    else:
                        print('{} -> {} | tempo execução: {} s | menor caminho: {}'.format(origem, n, round(tempo_execucao,2), caminho))

            # Finaliza o contador de tempo de execução
            end_time_total = time.time()
            tempo_execucao_total = end_time - start_time

            # Imprime o tempo de execução total
            print('\nTempo Execução Total: {} s'.format(round(tempo_execucao_total,2)))
            
    # Fecha o arquivo
    fd.close()

# Ponto de partida do script
if __name__ == "__main__":
   main(sys.argv[1:])