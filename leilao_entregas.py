# Versão 1: Algoritmo Básico
def ler_conexoes(arquivo):
    conexoes = {}
    with open(arquivo, 'r') as f:
        for linha in f:
            origem, destino, tempo = linha.strip().split(',')
            if origem not in conexoes:
                conexoes[origem] = {}
            conexoes[origem][destino] = int(tempo)
            if destino not in conexoes:
                conexoes[destino] = {}
            conexoes[destino][origem] = int(tempo)
    return conexoes

def ler_entregas(arquivo):
    entregas = []
    with open(arquivo, 'r') as f:
        for linha in f:
            horario, destino, bonus = linha.strip().split(',')
            #le o arquivo que abriu e coloca em cada variavel
            entregas.append((int(horario), destino, int(bonus)))
            # coloca tudo dentro da lista vazia e transforma em inteiro
    return entregas

def leilao_basico(conexoes, entregas):
    #precisa das duas funções anteriores para poder funcionar
    lucro_total = 0
    #lucro zeroi pois acabou de começar 
    sequencia_entregas = []
    #lista vazia no inicio do código
    tempo_atual = 0
    #considera como um ponto de partida
    posicao_atual = 'A'
    
    for entrega in entregas:
        #cada indice das entregas retornadas pela função anterior
        horario, destino, bonus = entrega
        #primeira iteração, horario é 0, destino é B e o bonus é 1
        #segundo a iteração, horario é 5, destino é c e o bonus é 10
        #cada variavel recebe o valor da tupla
        if destino in conexoes[posicao_atual]:
            #se o destino estiver na lista de conexões, na primeira iteração será A
            tempo_viagem = conexoes[posicao_atual][destino]
            #variavel tempo de viagem, declarada aqui pela primeira vez
            #irá receber o valor do dicionário de conexões, onde o primeiro valor é o ponto de partida e o segundo o destino
            #tempo de viagem é o tempo que leva para ir de A a B, por exemplo
            if tempo_atual + tempo_viagem <= horario:
                #se o tempo atual, mais o tempo de viagem,
                # for menor que o horário, contido no arquivo de entregas:
                lucro_total += bonus
                #lucro total até então zerado recebe o bonus do arquivo de entregas de forma dinamica
                sequencia_entregas.append((horario, destino, bonus))
                #a lista de entregas recebe a entrega recém feita
                tempo_atual += tempo_viagem * 2  # Ida e volta
                posicao_atual = 'A'  # Retorna ao ponto de partida
    
    return sequencia_entregas, lucro_total

# Executando o algoritmo básico
conexoes = ler_conexoes('conexoes.txt')
entregas = ler_entregas('entregas.txt')
sequencia, lucro = leilao_basico(conexoes, entregas)
print("Sequência de entregas (Básico):", sequencia)
print("Lucro esperado (Básico):", lucro)

# Versão 2: Algoritmo Otimizado com Programação Dinâmica
def leilao_otimizado(conexoes, entregas):
    n = len(entregas)
    dp = [0] * (n + 1)  # Tabela de programação dinâmica
    
    for i in range(1, n + 1):
        horario, destino, bonus = entregas[i - 1]
        if destino in conexoes['A']:
            dp[i] = max(dp[i - 1], dp[i - 1] + bonus)
        else:
            dp[i] = dp[i - 1]
    
    # Reconstruir a sequência de entregas
    sequencia_entregas = []
    lucro_total = dp[n]
    for i in range(n, 0, -1):
        if dp[i] != dp[i - 1]:
            sequencia_entregas.append(entregas[i - 1])
    
    sequencia_entregas.reverse()
    return sequencia_entregas, lucro_total

# Executando o algoritmo otimizado
sequencia_otimizada, lucro_otimizado = leilao_otimizado(conexoes, entregas)
print("Sequência de entregas (Otimizado):", sequencia_otimizada)
print("Lucro esperado (Otimizado):", lucro_otimizado)

import time

# Medindo o tempo de execução da versão básica
inicio_basico = time.perf_counter()  # Usando perf_counter para alta precisão
sequencia_basico, lucro_basico = leilao_basico(conexoes, entregas)
tempo_basico = (time.perf_counter() - inicio_basico) * 1000  # Convertendo para milissegundos

# Medindo o tempo de execução da versão otimizada
inicio_otimizado = time.perf_counter()  # Usando perf_counter para alta precisão
sequencia_otimizada, lucro_otimizado = leilao_otimizado(conexoes, entregas)
tempo_otimizado = (time.perf_counter() - inicio_otimizado) * 1000  # Convertendo para milissegundos

# Exibindo os resultados
print("\nComparação de Desempenho:")
print("Versão Básica:")
print(f"Tempo de execução: {tempo_basico:.6f} ms")  # Exibindo com 6 casas decimais
print(f"Lucro: {lucro_basico}")

print("\nVersão Otimizada:")
print(f"Tempo de execução: {tempo_otimizado:.6f} ms")  # Exibindo com 6 casas decimais
print(f"Lucro: {lucro_otimizado}")

import matplotlib.pyplot as plt

# Dados para o gráfico
versoes = ['Básica', 'Otimizada']
tempos = [tempo_basico, tempo_otimizado]
lucros = [lucro_basico, lucro_otimizado]

# Gráfico de tempo de execução
plt.figure(figsize=(10, 5))
plt.bar(versoes, tempos, color=['blue', 'green'])
plt.title('Tempo de Execução das Versões')
plt.ylabel('Tempo (segundos)')
plt.show()

# Gráfico de lucro obtido
plt.figure(figsize=(10, 5))
plt.bar(versoes, lucros, color=['blue', 'green'])
plt.title('Lucro Obtido pelas Versões')
plt.ylabel('Lucro')
plt.show()
