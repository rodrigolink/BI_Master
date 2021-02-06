#codigo para extrair os dados das partidas
import numpy as np
import matplotlib.pyplot as plt
import csv #para processar os arquivos CSV
import random
import time
import math
import pandas as pd

print('lendo dados')
#importando dados da partida1
filename='2013-11-03_tromso_stromsgodset_raw_first.csv'
with open(filename) as cvs_file:
    dados1 = pd.read_csv(cvs_file,header=None)
    
dados1=pd.DataFrame.drop(dados1,0,axis=1)
dados1=pd.DataFrame.drop(dados1,list(range(4,9)),axis=1)

eventos1=[]
jogada1=[]

for i in range(len(dados1)):
    if i%100==0:
        print(i)
    
    if i%11==0 and i>0:
        eventos1.append(jogada1)
        jogada1=[]

    jogada1.append(dados1[2][i])
    jogada1.append(dados1[3][i])
        
eventos1.append(jogada1)

    
#importando dados da partida2
filename='2013-11-03_tromso_stromsgodset_raw_second.csv'
with open(filename) as cvs_file:
    dados2 = pd.read_csv(cvs_file,header=None)
    
dados2=pd.DataFrame.drop(dados2,0,axis=1)
dados2=pd.DataFrame.drop(dados2,list(range(4,9)),axis=1)

eventos2=[]
jogada2=[]

for i in range(len(dados2)):
    if i%100==0:
        print(i)
    
    if i%11==0 and i>0:
        eventos2.append(jogada2)
        jogada2=[]

    jogada2.append(dados2[2][i])
    jogada2.append(dados2[3][i])
        
eventos2.append(jogada2)
    
#importando dados da partida3
filename='2013-11-07_tromso_anji_raw_first.csv'
with open(filename) as cvs_file:
    dados3 = pd.read_csv(cvs_file,header=None)
    
dados3=pd.DataFrame.drop(dados3,0,axis=1)
dados3=pd.DataFrame.drop(dados3,list(range(4,9)),axis=1)

eventos3=[]
jogada3=[]

for i in range(len(dados3)):
    if i%100==0:
        print(i)
    
    if i%11==0 and i>0:
        eventos3.append(jogada3)
        jogada3=[]

    jogada3.append(dados3[2][i])
    jogada3.append(dados3[3][i])
        
eventos3.append(jogada3)
    
#importando dados da partida4
filename='2013-11-07_tromso_anji_raw_second.csv'
with open(filename) as cvs_file:
    dados4 = pd.read_csv(cvs_file,header=None)
    
dados4=pd.DataFrame.drop(dados4,0,axis=1)
dados4=pd.DataFrame.drop(dados4,list(range(4,9)),axis=1)

eventos4=[]
jogada4=[]

for i in range(len(dados4)):
    if i%100==0:
        print(i)
    
    if i%11==0 and i>0:
        eventos4.append(jogada4)
        jogada4=[]

    jogada4.append(dados4[2][i])
    jogada4.append(dados4[3][i])
        
eventos4.append(jogada4)
    
jogadas_prontas1=[]
for i in range(min(len(eventos1),len(eventos2))):
    jogada=[]
    for j in range(len(eventos1[i])):
        jogada.append(eventos1[i][j])
    for j in range(len(eventos2[i])):
        jogada.append(eventos2[i][j])
        
    jogadas_prontas1.append(jogada)

jogadas_prontas2=[]
for i in range(min(len(eventos3),len(eventos4))):
    jogada=[]
    for j in range(len(eventos3[i])):
        jogada.append(eventos3[i][j])
    for j in range(len(eventos4[i])):
        jogada.append(eventos4[i][j])
        
    jogadas_prontas2.append(jogada)
    
teste1=pd.DataFrame(jogadas_prontas1)
teste1.describe()
    

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

