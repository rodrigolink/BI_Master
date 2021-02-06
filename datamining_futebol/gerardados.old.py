#codigo para extrair os dados das partidas
import numpy as np
import matplotlib.pyplot as plt
import json
import csv #para processar os arquivos CSV
import random
import time

start_time = time.time()

print('lendo dados')
#importando dados da partida
filename='tr-ft.json'
with open(filename) as json_file:
    dados = json.load(json_file)

#importando descricao da partida
filename2='tr-ft-gamedesc.json'    
with open(filename2) as json_file:
    dados2 = json.load(json_file)

#jogadores x time
lista=[]
for i in dados2['player'].keys():
    times=[i,dados2['player'][i]['team']]
    
    lista.append(times)

#lista de todas as posicoes (x,y) dos 22 jogadores (time1 e depois time2)    
#ha erros na posicao dos jogadores. eliminando posicoes mais de 2m fora do campo
jogada=[]
x=[]
y=[]
print('limpando dados')
for i in range(len(dados)):
    if i%1000==0:
        print(i,len(dados))
    nova=[]
    teste=0
    for j in range(len(lista)-1):
        nova.append(np.int16(100*dados[i]['data'][j+1]['x']))
        nova.append(np.int16(100*dados[i]['data'][j+1]['y']))
        if (dados[i]['data'][j+1]['x'] < 5500 and dados[i]['data'][j+1]['x'] > -5500) and(dados[i]['data'][j+1]['y'] < 3700 and dados[i]['data'][j+1]['y'] > -3700) :
            x.append(dados[i]['data'][j+1]['x'])
            y.append(dados[i]['data'][j+1]['y'])
            teste=teste+1
            
    if teste==22:
        jogada.append(nova)
        
        
#data aumengtation
#variacao da posicao de cada jogador, (x,y)+rand(-2,2)
#triplicando numero de jogadas
repeticoes=2
print('aumentando dados')
for i in range(len(jogada)):
    if i%1000==0:
        print(i,len(jogada))
    for k in range(repeticoes):
        nova=[]
        for j in range(len(jogada[i])):
            nova.append(np.int16(jogada[i][j]+random.uniform(-200,200)))
        jogada.append(nova)

    
print('passador e recebedor')
escala=10
jogadas_prontas=[]
#criando colunas "passador" e "recebedor"
for i in range(int(len(jogada)/escala)):
    if i%2==0:
        print(i,int(len(jogada)/escala))
    for j in range(len(lista)-1):
        for k in range(len(lista)-1):
            temp=[]
            time1=0
            time2=0
            for l in range(len(jogada[i])):
                if (l<22 and l%2==0):
                   time1=time1+jogada[i][l]
                if (l>21 and l%2==0):
                   time2=time2+jogada[i][l]
                   
            for l in range(len(jogada[i])):
                if (k+1<12 and time1>=time2):
                    temp.append(-1*jogada[i][l])
                if (k+1<12 and time1<time2):
                    temp.append(jogada[i][l])
                if (k+1>11 and time1<time2):
                    temp.append(-1*jogada[i][l])
                if (k+1>11 and time1>=time2):
                    temp.append(jogada[i][l])
                    
            temp.append(j+1)    #passador 
            temp.append(k+1)    #recebedor
            
            temp.append(0)      #impedimento
            jogadas_prontas.append(temp)


print('impedimentos')
#regras de impedimento
impedimentos=[]
tipo1=[]
tipo2=[]
tipo3=[]
tipo4=[]
tipo5=[]
tipo6=[]
tipo7=[]

for i in range(len(jogadas_prontas)):
    naoimpedimento=0
    if i%1000==0:
        print(i,len(jogadas_prontas))

#passador e recebedor mesma pessoa
    if (jogadas_prontas[i][44]==jogadas_prontas[i][45]):
        naoimpedimento=1
        tipo1.append(i)
        
#jogador fora de campo nao tem impedimento
    if (naoimpedimento==0 and (jogadas_prontas[i][2*jogadas_prontas[i][45]-1]<-3500 or jogadas_prontas[i][2*jogadas_prontas[i][45]-1]>3500 or jogadas_prontas[i][2*jogadas_prontas[i][45]-2]>5400 or jogadas_prontas[i][2*jogadas_prontas[i][45]-2]<-5400)):
        naoimpedimento=1
        tipo2.append(i)
    
#passe de jogador do outro time nao tem impedimento
    if (naoimpedimento==0 and (jogadas_prontas[i][44]>11 and jogadas_prontas[i][45]<12)):
        naoimpedimento=1
        tipo3.append(i)
    if (naoimpedimento==0 and (jogadas_prontas[i][44]<12 and jogadas_prontas[i][45]>11)):
        naoimpedimento=1
        tipo3.append(i)
    
#cobranca de lateral nao tem impedimento
    if (naoimpedimento==0 and (jogadas_prontas[i][2*jogadas_prontas[i][44]-1]<-3500 or jogadas_prontas[i][2*jogadas_prontas[i][44]-1]>3500)):
        naoimpedimento=1
        tipo4.append(i)

#passe para tras nao tem impedimento
    if (naoimpedimento==0 and jogadas_prontas[i][2*jogadas_prontas[i][44]-2]>jogadas_prontas[i][2*jogadas_prontas[i][45]-2]):
        naoimpedimento=1
        tipo5.append(i)

#jogador no campo de defesa nao tem impedimento
    if (naoimpedimento==0 and jogadas_prontas[i][2*jogadas_prontas[i][45]-2]<0):
        naoimpedimento=1
        tipo6.append(i)
        
#impedimento se numero de jogadores a frente do recebedor <2
    if naoimpedimento==0:
        numerojogadoresfrente=0
        if jogadas_prontas[i][45]>11:
            for j in range(11):
                if jogadas_prontas[i][2*j]>jogadas_prontas[i][2*jogadas_prontas[i][45]-2]:
                    numerojogadoresfrente=numerojogadoresfrente+1
        if jogadas_prontas[i][45]<12:
            for j in range(11):
                if jogadas_prontas[i][2*j+22]>jogadas_prontas[i][2*jogadas_prontas[i][45]-2]:
                    numerojogadoresfrente=numerojogadoresfrente+1
        
        if numerojogadoresfrente<2:
            jogadas_prontas[i][46]=1
            impedimentos.append(i)
        else:
            tipo7.append(i)

print('balanceando')
balanco=[]
if len(tipo1)<len(impedimentos):
    balanco.append(tipo1)
else:
    balanco1=random.sample(tipo1,len(impedimentos))
    balanco.append(balanco1)
if len(tipo2)<len(impedimentos):
    balanco.append(tipo2)
else:
    balanco2=random.sample(tipo2,len(impedimentos))
    balanco.append(balanco2)
if len(tipo3)<len(impedimentos):
    balanco.append(tipo3)
else:
    balanco3=random.sample(tipo3,len(impedimentos))
    balanco.append(balanco3)
if len(tipo4)<len(impedimentos):
    balanco.append(tipo4)
else:
    balanco4=random.sample(tipo4,len(impedimentos))
    balanco.append(balanco4)
if len(tipo5)<len(impedimentos):
    balanco.append(tipo5)
else:
    balanco5=random.sample(tipo5,len(impedimentos))
    balanco.append(balanco5)
if len(tipo6)<len(impedimentos):
    balanco.append(tipo6)
else:
    balanco6=random.sample(tipo6,len(impedimentos))
    balanco.append(balanco6)
if len(tipo7)<len(impedimentos):
    balanco.append(tipo7)
else:
    balanco7=random.sample(tipo7,len(impedimentos))
    balanco.append(balanco7)

balanco.append(impedimentos)

jogadas_balanceado=[]
for i in range(len(balanco)):
    for j in range(len(balanco[i])):
        jogadas_balanceado.append(jogadas_prontas[balanco[i][j]])

elapsed_time = time.time() - start_time

print('gravando dados')

with open('eventos_esc10b.csv', 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'X5', 'Y5', 'X6', 'Y6', 'X7', 'Y7', 'X8', 'Y8', 'X9', 'Y9', 'X10', 'Y10', 'X11', 'Y11', 'X12', 'Y12', 'X13', 'Y13', 'X14', 'Y14', 'X15', 'Y15', 'X16', 'Y16', 'X17', 'Y17', 'X18', 'Y18', 'X19', 'Y19', 'X20', 'Y20', 'X21', 'Y21', 'X22', 'Y22','Passador','Recebor','Impedimento'])
    writer.writerows(jogadas_balanceado)



# Create data
campox=[]
campoy=[]
for i in range(-5400,5400,10):
    campox.append(i)
    campoy.append(-3500)
    campox.append(i)
    campoy.append(3500)
    
for i in range(-3500,3500,10):
    campox.append(-5400)
    campoy.append(i)
    campox.append(5400)
    campoy.append(i)
    campox.append(0)
    campoy.append(i)

for i in range(360):
    campox.append(915*math.cos(math.radians(i)))
    campoy.append(915*math.sin(math.radians(i)))
    
for i in range(0,2016,10):
    campox.append(5400-1650)
    campoy.append(i)
    campox.append(5400-1650)
    campoy.append(-i)
    campox.append(-5400+1650)
    campoy.append(i)
    campox.append(-5400+1650)
    campoy.append(-i)
    
for i in range(5400,5400-1650,-10):
    campox.append(i)
    campoy.append(2016)
    campox.append(i)
    campoy.append(-2016)
    campox.append(-i)
    campoy.append(-2016)
    campox.append(-i)
    campoy.append(2016)
    
for i in range(0,366+550,10):
    campox.append(5400-550)
    campoy.append(i)
    campox.append(5400-550)
    campoy.append(-i)
    campox.append(-5400+550)
    campoy.append(i)
    campox.append(-5400+550)
    campoy.append(-i)
    
for i in range(5400,5400-550,-10):
    campox.append(i)
    campoy.append(366+550)
    campox.append(i)
    campoy.append(-366-550)
    campox.append(-i)
    campoy.append(-366-550)
    campox.append(-i)
    campoy.append(366+550)

for i in range(360):
    if 5400-1100 + 915*math.cos(math.radians(i))<5400-1650:
        campox.append(5400-1100 + 915*math.cos(math.radians(i)))
        campoy.append(915*math.sin(math.radians(i)))

for i in range(360):
    if -5400+1100 + 915*math.cos(math.radians(i))>-5400+1650:
        campox.append(-5400+1100 + 915*math.cos(math.radians(i)))
        campoy.append(915*math.sin(math.radians(i)))

    campox.append(5400-1100)
    campoy.append(0)
    campox.append(-5400+1100)
    campoy.append(0)
    
jog=random.choice(range(len(jogadas_balanceado)))
g1 = (jogadas_balanceado[jog][:22:2],jogadas_balanceado[jog][1:23:2])
g2 = (jogadas_balanceado[jog][22:44:2],jogadas_balanceado[jog][23:44:2])
g3 = (jogadas_balanceado[jog][2*jogadas_balanceado[jog][45]-2],jogadas_balanceado[jog][2*jogadas_balanceado[jog][45]-1])
g4 = (jogadas_balanceado[jog][2*jogadas_balanceado[jog][44]-2],jogadas_balanceado[jog][2*jogadas_balanceado[jog][44]-1])
data = (g3,g4,g1, g2)
colors = ("green","purple","red", "blue")
groups = ("recebedor","passador","time1", "time2")
size=(70,70,30,30)

# Create plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

plt.scatter(campox,campoy,s=5,c="black",alpha=0.3)    

for data, color, group, size in zip(data, colors, groups, size):
    x, y = data
    ax.scatter(x, y, alpha=0.8, c=color, edgecolors='none', s=size, label=group)

plt.ylim(-3700, 3700)
plt.xlim(-5500, 5500)
plt.title('Jogada: '+str(jog)+", Imp: "+str(jogadas_balanceado[jog][-1]))
plt.legend(loc=2)
plt.show()

