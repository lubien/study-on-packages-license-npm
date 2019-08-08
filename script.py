import os
import csv
import json
import pandas as pd 

#Name[0];Stars[1];Forks[2];Language[3];Description[4];URL[5];Domain[6];Growth Pattern[7]
#Abre o CSV e trata os dados, retirando os repositorios de javascript e adicionando os mesmos a uma lista
with open('Domains of 5,000 GitHub Repositories - Public - Domains.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    #salva todos os links do csv
    repositorios = [] 
    for row in readCSV:
        if(row[3] == "JavaScript"):
            #row[5] é a coluna que contem os links
            projeto = []
            projeto.append("["+row[0].split("/")[0]+"]"+row[0].split("/")[1])
            projeto.append(row[5])
            repositorios.append(projeto)

inicio = 51
fim = 61
#Cria o repositorio onde serão clonados os repositorios da lista
os.system("mkdir repositories")
#Usa a lista com os repositorios para rodar o git clone
for pizza in range(inicio, fim):
    print(repositorios[pizza])
    os.system("git clone " + repositorios[pizza][1] + " repositories/" + repositorios[pizza][0])
#Cria diretorio que salva o resumo de licencas de cada repositorio
os.system("mkdir summary-licenses")
#Entra no repositorio para rodar o checador de licensas
os.chdir("repositories")
#Loop para entrar em cada repositorio, testar a licensa e voltar para o diretorio "licensa"

for pizza in range(inicio, fim):
    os.chdir(repositorios[pizza][0])
    os.system("license-checker --json > ../../summary-licenses/license"+str(pizza)+".json")
    os.chdir("../")

os.chdir("../summary-licenses")
#Cria um dicionario para salvar o conteudo dos jsons
json_final = {}
#Loop para varer os json e salva no dicionario
for pizza in range(inicio, fim):
    with open('license'+str(pizza)+'.json') as f:
        data = json.load(f)
    #concatena os json no dicionario criado
    json_final.update(data)

#Salva o dicionario no JSON
with open('resume_repository.json', 'w') as json_file:
    json.dump(json_final, json_file,indent = 4, sort_keys=True)
#Abre o json resumo
data = pd.read_json('resume_repository.json')
#converte o json para o formato de csv
data.to_csv('resume_repository.csv')