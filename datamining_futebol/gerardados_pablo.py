# codigo para extrair os dados das partidas
import numpy as np
import matplotlib.pyplot as plt
import json
import csv  # para processar os arquivos CSV
import random
import time

start_time = time.time()

print('lendo dados')
# importando dados da partida
filename = 'tr-ft.json'
with open(filename) as json_file:
    dados = json.load(json_file)

# importando descricao da partida
filename2 = 'tr-ft-gamedesc.json'
with open(filename2) as json_file:
    dados2 = json.load(json_file)

# jogadores x time
lista = []
for i in dados2['player'].keys():
    times = [i, dados2['player'][i]['team']]

    lista.append(times)

# lista de todas as posicoes (x,y) dos 22 jogadores (time1 e depois time2)
# ha erros na posicao dos jogadores. eliminando posicoes mais de 2m fora do campo
jogada = []
x = []
y = []
print('limpando dados')
for i in range(len(dados)):
    if i % 1000 == 0:
        print(i, len(dados))
    nova = []
    teste = 0
    for j in range(len(lista) - 1):
        nova.append(np.int16(100 * dados[i]['data'][j + 1]['x']))
        nova.append(np.int16(100 * dados[i]['data'][j + 1]['y']))
        if (5500 > dados[i]['data'][j + 1]['x'] > -5500) and (3700 > dados[i]['data'][j + 1]['y'] > -3700):
            x.append(dados[i]['data'][j + 1]['x'])
            y.append(dados[i]['data'][j + 1]['y'])
            teste = teste + 1

    if teste == 22:
        jogada.append(nova)

# data augmentation
# variacao da posicao de cada jogador, (x,y)+rand(-2,2)
# triplicando numero de jogadas
repeticoes = 2
print('aumentando dados')
for i in range(len(jogada)):
    if i % 1000 == 0:
        print(i, len(jogada))
    for k in range(repeticoes):
        nova = []
        for j in range(len(jogada[i])):
            nova.append(np.int16(100 * (jogada[i][j] + random.uniform(-200, 200))))
        jogada.append(nova)

print('passador e recebedor')
escala = 4
print('impedimentos')
# regras de impedimento
impedimentos = []
tipo1 = []
tipo2 = []
tipo3 = []
tipo4 = []
tipo5 = []
tipo6 = []
tipo7 = []

n1 = 0
n2 = 0
n3 = 0
n4 = 0
n5 = 0
n6 = 0
n7 = 0

jogadas_prontas = []

k = 0

# criando colunas "passador" e "recebedor"
for i in range(int(len(jogada))):
    if i % 1000 == 0:
        print(i, int(len(jogada)))
    for j in range(len(lista) - 1):
        for k in range(len(lista) - 1):
            temp = []
            time1 = 0
            time2 = 0
            for kk in range(len(jogada[i])):
                if kk < 22 and kk % 2 == 0:
                    time1 = time1 + jogada[i][kk]
                if kk > 21 and kk % 2 == 0:
                    time2 = time2 + jogada[i][kk]

            for kk in range(len(jogada[i])):
                if k + 1 < 12 and time1 >= time2:
                    temp.append(-1 * jogada[i][kk])
                if k + 1 < 12 and time1 < time2:
                    temp.append(jogada[i][kk])
                if k + 1 > 11 and time1 < time2:
                    temp.append(-1 * jogada[i][kk])
                if k + 1 > 11 and time1 >= time2:
                    temp.append(jogada[i][kk])

            temp.append(np.int8(j + 1))  # passador
            temp.append(np.int8(k + 1))  # recebedor

            temp.append(0)  # impedimento
            naoimpedimento = 0

            # passador e recebedor mesma pessoa
            if temp[44] == temp[45]:
                naoimpedimento = 1
                if n1 % escala == 0:
                    tipo1.append(k)
                    jogadas_prontas.append(temp)
                    k += 1
                n1 += 1

            # jogador fora de campo nao tem impedimento
            if (naoimpedimento == 0 and not (
                    temp[2 * (temp[45] - 1)] < -3500 or temp[2 * (temp[45] - 1)] > 3500) or
                    temp[2 * temp[45] - 1] > 5500 or temp[2 * temp[45] - 1] < -5500):
                naoimpedimento = 1
                if n2 % escala == 0:
                    tipo2.append(k)
                    jogadas_prontas.append(temp)
                    k += 1
                n2 += 1

            # passe de jogador do outro time nao tem impedimento
            if naoimpedimento == 0 and (temp[44] > 11 and temp[45] < 12):
                naoimpedimento = 1
                if n3 % escala == 0:
                    tipo3.append(k)
                    jogadas_prontas.append(temp)
                    k += 1
                n3 += 1

            if naoimpedimento == 0 and (temp[44] < 12 and temp[45] > 11):
                naoimpedimento = 1
                if n3 % escala == 0:
                    tipo3.append(k)
                    jogadas_prontas.append(temp)
                    k += 1
                n3 += 1

            # cobranca de lateral nao tem impedimento
            if naoimpedimento == 0 and (temp[2 * (temp[44] - 1)] < -3500 or temp[2 * (temp[44] - 1)] > 3500):
                naoimpedimento = 1
                if n4 % escala == 0:
                    tipo4.append(k)
                    jogadas_prontas.append(temp)
                    k += 1
                n4 += 1

            # passe para tras nao tem impedimento
            if naoimpedimento == 0 and temp[2 * temp[44] - 2] > temp[2 * temp[45] - 2]:
                naoimpedimento = 1
                if n5 % escala == 0:
                    tipo5.append(k)
                    jogadas_prontas.append(temp)
                    k += 1
                n5 += 1

            # jogador no campo de defesa nao tem impedimento
            if naoimpedimento == 0 and temp[2 * temp[45] - 2] < 0:
                naoimpedimento = 1
                if n6 % escala == 0:
                    tipo6.append(k)
                    jogadas_prontas.append(temp)
                    k += 1
                n6 += 1

            # impedimento se numero de jogadores a frente do recebedor <2
            if naoimpedimento == 0:
                numerojogadoresfrente = 0
                if temp[45] > 11:
                    for j in range(11):
                        if temp[2 * j] > temp[2 * temp[45] - 2]:
                            numerojogadoresfrente = numerojogadoresfrente + 1
                if temp[45] < 12:
                    for j in range(11):
                        if temp[2 * j + 22] > temp[2 * temp[45] - 2]:
                            numerojogadoresfrente = numerojogadoresfrente + 1

                if numerojogadoresfrente < 2:
                    temp[46] = 1
                    impedimentos.append(k)
                    jogadas_prontas.append(temp)
                    k += 1
                else:
                    if n7 % escala == 0:
                        tipo7.append(k)
                        jogadas_prontas.append(temp)
                        k += 1
                    n7 += 1

elapsed_time = time.time() - start_time

print('gravando dados')

with open('eventos.csv', 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(
        ['X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'X5', 'Y5', 'X6', 'Y6', 'X7', 'Y7', 'X8', 'Y8', 'X9', 'Y9',
         'X10', 'Y10', 'X11', 'Y11', 'X12', 'Y12', 'X13', 'Y13', 'X14', 'Y14', 'X15', 'Y15', 'X16', 'Y16', 'X17', 'Y17',
         'X18', 'Y18', 'X19', 'Y19', 'X20', 'Y20', 'X21', 'Y21', 'X22', 'Y22', 'Passador', 'Recebedor', 'Impedimento'])
    writer.writerows(jogadas_prontas)

# # Create data
# jog=random.choice(impedimentos)
# g1 = (jogadas_prontas[jog][:22:2],jogadas_prontas[jog][1:23:2])
# g2 = (jogadas_prontas[jog][22:44:2],jogadas_prontas[jog][23:44:2])
# g3 = (jogadas_prontas[jog][2*jogadas_prontas[jog][45]-2],jogadas_prontas[jog][2*jogadas_prontas[jog][45]-1])
# g4 = (jogadas_prontas[jog][2*jogadas_prontas[jog][44]-2],jogadas_prontas[jog][2*jogadas_prontas[jog][44]-1])
# data = (g1, g2,g3,g4)
# colors = ("red", "blue","green","black")
# groups = ("time1", "time2","recebedor","passador")
#
# # Create plot
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
#
# for data, color, group in zip(data, colors, groups):
#    x, y = data
#    ax.scatter(x, y, alpha=0.8, c=color, edgecolors='none', s=30, label=group)
#
# plt.ylim(-37, 37)
# plt.xlim(-55, 55)
# plt.title('Jogada: '+str(jog))
# plt.legend(loc=2)
# plt.show()
