#codigo para extrair os dados das partidas
import numpy as np
import matplotlib.pyplot as plt
import json
import csv #para processar os arquivos CSV
import random
import time
import math
import pandas as pd

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
lista_teste=list(range(len(dados)))

print('limpando dados')
for i in range(len(dados)):
    if i%1000==0:
        print(i,len(dados))
    nova=[]
    teste=0
    for j in range(len(lista)-1):
        nova.append(np.int16(100*dados[i]['data'][j+1]['x']))
        nova.append(np.int16(100*dados[i]['data'][j+1]['y']))
        if (dados[i]['data'][j+1]['x'] < 55 and dados[i]['data'][j+1]['x'] > -55) and(dados[i]['data'][j+1]['y'] < 37 and dados[i]['data'][j+1]['y'] > -37) :
            teste=teste+1
            
    if teste==22:
        jogada.append(nova)
        lista_teste[i]=-1
        
#analisando os dados jogados fora        
#soma=0
#maximo=0
#evol=[]
#for i in range(len(lista_teste)):
#    if lista_teste[i]>=0:
#        soma=soma+1
#    if lista_teste[i]<0:
#        maximo=max(soma,maximo)
#        soma=0
#    if soma>25:
#        soma=25
#    evol.append(soma) 
#
#plt.scatter(list(range(len(dados))),evol)

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
for i in range(len(jogada)):
    if i%1000==0:
        print(i,len(jogada))
    if random.random()<1/escala:
        for j in range(len(lista)-1):
            for k in range(len(lista)-1):
                temp=[]
                time1=0
                for l in range(0,len(jogada[i]),2):
                    if (l<22):
                       time1=time1+jogada[i][l]
                    if (l>21):
                       time1=time1-jogada[i][l]
                       
                for l in range(len(jogada[i])):
                    temp.append(jogada[i][l])
                
                if (k+1<12 and time1>=0) or (k+1>11 and time1<0):
                    temp = [m * -1 for m in temp]
                    
                temp.append(j+1)    #passador 
                temp.append(k+1)    #recebedor
                
                temp.append(0)      #impedimento
                jogadas_prontas.append(temp)


medida1=len(jogadas_prontas)

print('impedimentos')
#regras de impedimento
impedimentos=[]
condicao0=[]
condicao1=[]
condicao2=[]
condicao3=[]
condicao4=[]
condicao5=[]
condicao6=[]
condicao7=[]

for i in range(len(jogadas_prontas)):
    naoimpedimento=[]
    if i%1000==0:
        print(i,len(jogadas_prontas))

#passador e recebedor mesma pessoa
    if (jogadas_prontas[i][44]==jogadas_prontas[i][45]):
        naoimpedimento.append(1)
    else:
        naoimpedimento.append(0)
        
#jogador fora de campo nao tem impedimento
    if (jogadas_prontas[i][2*jogadas_prontas[i][45]-1]<-3500 or jogadas_prontas[i][2*jogadas_prontas[i][45]-1]>3500 or jogadas_prontas[i][2*jogadas_prontas[i][45]-2]>5400 or jogadas_prontas[i][2*jogadas_prontas[i][45]-2]<-5400):
        naoimpedimento.append(1)
    else:
        naoimpedimento.append(0)
    
#passe de jogador do outro time nao tem impedimento
    if ((jogadas_prontas[i][44]>11 and jogadas_prontas[i][45]<12) or (jogadas_prontas[i][44]<12 and jogadas_prontas[i][45]>11)):
        naoimpedimento.append(1)
    else:
        naoimpedimento.append(0)
        
#cobranca de lateral nao tem impedimento
    if (jogadas_prontas[i][2*jogadas_prontas[i][44]-1]<-3500 or jogadas_prontas[i][2*jogadas_prontas[i][44]-1]>3500):
        naoimpedimento.append(1)
    else:
        naoimpedimento.append(0)

#jogador no campo de defesa nao tem impedimento
    if (jogadas_prontas[i][2*jogadas_prontas[i][45]-2]<0):
        naoimpedimento.append(1)
    else:
        naoimpedimento.append(0)

#passe para tras nao tem impedimento
    if (jogadas_prontas[i][2*jogadas_prontas[i][44]-2]>jogadas_prontas[i][2*jogadas_prontas[i][45]-2]):
        naoimpedimento.append(1)
    else:
        naoimpedimento.append(0)
        
#impedimento se numero de jogadores a frente do recebedor <2
    numerojogadoresfrente=0
    if jogadas_prontas[i][45]>11:
        for j in range(11):
            if jogadas_prontas[i][2*j]>jogadas_prontas[i][2*jogadas_prontas[i][45]-2]:
                numerojogadoresfrente=numerojogadoresfrente+1
    if jogadas_prontas[i][45]<12:
        for j in range(11):
            if jogadas_prontas[i][2*j+22]>jogadas_prontas[i][2*jogadas_prontas[i][45]-2]:
                numerojogadoresfrente=numerojogadoresfrente+1
    
    if numerojogadoresfrente>1:
        naoimpedimento.append(1)
    else:
        naoimpedimento.append(0)
    
    if sum(naoimpedimento)==0:
        impedimentos.append(i)
        jogadas_prontas[i][46]=1
    
    if sum(naoimpedimento)==1:
        if naoimpedimento[0]==1:
            condicao1.append(i)
        if naoimpedimento[1]==1:
            condicao2.append(i)
        if naoimpedimento[2]==1:
            condicao3.append(i)
        if naoimpedimento[3]==1:
            condicao4.append(i)
        if naoimpedimento[4]==1:
            condicao5.append(i)
        if naoimpedimento[5]==1:
            condicao6.append(i)
        if naoimpedimento[6]==1:
            condicao7.append(i)
    
    if sum(naoimpedimento)==7:
        condicao0.append(i)
                       
    
medida2=len(impedimentos)
    
print('balanceando')
balanco=[]
if len(condicao0)>0:
    for i in range(len(condicao0)):
        balanco.append(condicao0[i])
if len(condicao1)>0:
    for i in range(len(condicao1)):
        balanco.append(condicao1[i])
if len(condicao2)>0:
    for i in range(len(condicao2)):
        balanco.append(condicao2[i])
if len(condicao3)>0:
    for i in range(len(condicao3)):
        balanco.append(condicao3[i])
if len(condicao4)>0:
    for i in range(len(condicao4)):
        balanco.append(condicao4[i])
if len(condicao5)>0:
    for i in range(len(condicao5)):
        balanco.append(condicao5[i])
if len(condicao6)>0:
    for i in range(len(condicao6)):
        balanco.append(condicao6[i])

medida3=len(balanco)
medida4=len(condicao7)

lista_bal=list(range(len(jogadas_prontas)))
for i in range(len(balanco)):
    lista_bal[balanco[i]]=-1

for i in range(len(condicao7)):
    lista_bal[condicao7[i]]=-1

cond7=random.sample(condicao7,len(balanco))

for i in range(len(balanco)):
    balanco.append(cond7[i])

for i in range(len(impedimentos)):
    lista_bal[impedimentos[i]]=-1
    
lista2=list(filter(lambda teste: teste>=0,lista_bal))

normais=random.sample(lista2,len(balanco))

for i in range(len(normais)):
    balanco.append(normais[i])

medida5=len(balanco) #tem que ser 4*medida3

jogadas_naoimpedimento=[]
for i in range(len(balanco)):
    if i%1000==0:
        print(i,len(balanco))
    nova=[]    
    for j in range(len(jogadas_prontas[balanco[i]])):
        nova.append(jogadas_prontas[balanco[i]][j])
        
    jogadas_naoimpedimento.append(nova)


#####################################
jogadas_impedimento=[]
for i in range(len(impedimentos)):
    if i%1000==0:
        print(i,len(impedimentos))
    nova=[]    
    for j in range(len(jogadas_prontas[impedimentos[i]])):
        nova.append(jogadas_prontas[impedimentos[i]][j])
        
    jogadas_impedimento.append(nova)


resize=math.floor(len(balanco)/len(impedimentos))-1
for i in range(len(jogadas_impedimento)):
    if i%1000==0:
        print(i,len(jogadas_impedimento))
    for j in range(resize):
        nova=[]
        for k in range(len(jogadas_impedimento[i])-3):
            if k%2==1 and k!=2*jogadas_impedimento[i][44]-1 and k!=2*jogadas_impedimento[i][45]-1:
                nova.append(np.int16(jogadas_impedimento[i][k]+random.uniform(-500,500)))
            if (k==2*jogadas_impedimento[i][44]-1): 
                nova.append(np.int16(jogadas_impedimento[i][k]))
            if (k==2*jogadas_impedimento[i][45]-1): 
                nova.append(np.int16(jogadas_impedimento[i][k]))            
            if k%2==0:
                nova.append(np.int16(jogadas_impedimento[i][k]))
                
        nova.append(np.int16(jogadas_impedimento[i][44]))
        nova.append(np.int16(jogadas_impedimento[i][45]))
        nova.append(np.int16(jogadas_impedimento[i][46]))
        if len(nova)!=47:
            print(i,'opa')
        jogadas_impedimento.append(nova)

resto=len(balanco)-len(jogadas_impedimento)
maisimp=random.sample(list(range(len(jogadas_impedimento))),resto)

for i in range(len(maisimp)):
    if i%1000==0:
        print(i,len(maisimp))

    nova=[]
    for j in range(len(jogadas_impedimento[maisimp[i]])-3):
        if k%2==1 and k!=2*jogadas_impedimento[maisimp[i]][44]-1 and k!=2*jogadas_impedimento[maisimp[i]][45]-1:
            nova.append(np.int16(jogadas_impedimento[maisimp[i]][k]+random.uniform(-500,500)))
        if (k==2*jogadas_impedimento[maisimp[i]][44]-1): 
            nova.append(np.int16(jogadas_impedimento[maisimp[i]][k]))
        if (k==2*jogadas_impedimento[maisimp[i]][45]-1): 
            nova.append(np.int16(jogadas_impedimento[maisimp[i]][k]))            
        if k%2==0:
            nova.append(np.int16(jogadas_impedimento[maisimp[i]][k]))            

    nova.append(np.int16(jogadas_impedimento[maisimp[i]][44]))
    nova.append(np.int16(jogadas_impedimento[maisimp[i]][45]))
    nova.append(np.int16(jogadas_impedimento[maisimp[i]][46]))
    
    jogadas_impedimento.append(nova)



elapsed_time = time.time() - start_time

print('gravando dados')
jogadas_balanceado=[]
for i in range(len(jogadas_naoimpedimento)):
    jogadas_balanceado.append(jogadas_naoimpedimento[i])
    jogadas_balanceado.append(jogadas_impedimento[i])

with open('eventos_final.csv', 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'X5', 'Y5', 'X6', 'Y6', 'X7', 'Y7', 'X8', 'Y8', 'X9', 'Y9', 'X10', 'Y10', 'X11', 'Y11', 'X12', 'Y12', 'X13', 'Y13', 'X14', 'Y14', 'X15', 'Y15', 'X16', 'Y16', 'X17', 'Y17', 'X18', 'Y18', 'X19', 'Y19', 'X20', 'Y20', 'X21', 'Y21', 'X22', 'Y22','Passador','Recebedor','Impedimento'])
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

