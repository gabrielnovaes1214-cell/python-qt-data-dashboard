from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from PyQt5 import uic
import Inter1
import Inter2
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


import os #manipular as pastas, definir o caminho
import shutil #mover literalmente, sem definir o nome do arquivo
import time
import glob #Encontrar o arquivo pela sua extensão
from selenium import webdriver #Fazer o controle no navegador
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



#DOWNLOADDDDDDDDD


# Obter o diretório base do usuário (ex: C:/Users/SeuUsuario)
diretorio_base = os.path.expanduser("~")

# Caminho da pasta de downloads e do projeto
caminho_downloads = os.path.join(diretorio_base, "Downloads")  # Caminho para Downloads

# Criar uma pasta automaticamente no Desktop para o projeto
caminho_projeto = os.path.join(diretorio_base, "Desktop", "PROJETO_FINAL")  # Caminho no Desktop
if not os.path.exists(caminho_projeto):
    os.makedirs(caminho_projeto)
    print(f"Pasta {caminho_projeto} criada.")


# Inicializa o navegador
def iniciar_navegador():
    try:
        driver = webdriver.Chrome(service=ChromeService())
        return driver
    except WebDriverException:
        print("Chrome não disponível. Tentando Firefox...")

    try:
        driver = webdriver.Firefox(service=FirefoxService())
        return driver
    except WebDriverException:
        print("Firefox não disponível. Tentando Edge...")

    try:
        driver = webdriver.Edge(service=EdgeService())
        return driver
    except WebDriverException:
        print("Nenhum navegador disponível. Instale o Chrome, Firefox ou Edge.")
        
        return None
    
navegador = iniciar_navegador()
if navegador:
    
    navegador.get('https://www.google.com')
else:
    print("Nenhum navegador foi iniciado.")

# Abre a página 
navegador.get('https://www.ibge.gov.br/estatisticas/sociais/populacao/22827-censo-demografico-2022.html?edicao=39980&t=resultados')

# Espera até que o primeiro botão esteja clicável e clica nele
botao_abrir = WebDriverWait(navegador, 5).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="tabela_1"]/button'))
)
botao_abrir.click()

time.sleep(5)


# Espera até que o botão de download esteja clicável e clica nele
botao_download = WebDriverWait(navegador, 5).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="downloadResultado"]/button[1]'))
)
botao_download.click()


# Aguarde um tempo para garantir que o download seja concluído
time.sleep(10)


# Procurar o arquivo mais recente com a extensão .xlsx na pasta de downloads
lista_arquivos = glob.glob(os.path.join(caminho_downloads, '*.xlsx'))
arquivo_baixado = max(lista_arquivos, key=os.path.getctime)  # Pega o arquivo mais recente

print(f"Arquivo mais recente encontrado: {arquivo_baixado}")


# Caminho para onde você deseja mover o arquivo
novo_caminho_arquivo = os.path.join(caminho_projeto, os.path.basename(arquivo_baixado))



# Mover o arquivo da pasta de downloads para a pasta do projeto
if os.path.exists(arquivo_baixado):
    shutil.move(arquivo_baixado, novo_caminho_arquivo)
    print(f"Arquivo movido para {novo_caminho_arquivo}")
else:
    print(f"Arquivo não encontrado.")
    
    
    
    
    
    
    
    
    
    
 #PLANILHAAAAAAAAAA MANIPULAÇÃO 
    

df = pd.read_excel(novo_caminho_arquivo, engine='openpyxl')

#apagar linhas inuteis
df = df.iloc[3:].reset_index(drop=True)

#Transpor
df = df.transpose()

#apagar coluna inutil q virou linha
df = df.drop(df.columns[[37]], axis=1)  

#nomes de colunas faltantes
df.iloc[0, 0] = "Gênero"
df.iloc[0, 1] = "Raça"
df.iloc[0, 2] = "Idade"
df.iloc[0, 3] = "Alfabetização"

#coluna0
texto_copiar1 = df.iloc[1, 0]  
df.iloc[2:181, 0] = texto_copiar1  

texto_copiar2 = df.iloc[181, 0]  
df.iloc[182:361, 0] = texto_copiar2  

texto_copiar3 = df.iloc[361, 0]  
df.iloc[362:541, 0] = texto_copiar3 


#coluna2 - fazer na mão é loucura
def preencher_intervalos(df, coluna, start, step, repete_intervalos):
    for i in range(repete_intervalos):
        texto_copiar = df.iloc[start + i * step, coluna]
        df.iloc[start + (i * step) + 1 : start + (i + 1) * step, coluna] = texto_copiar
preencher_intervalos(df, coluna=1, start=1, step=30, repete_intervalos=18) #coluna1
preencher_intervalos(df, coluna=2, start=1, step=3, repete_intervalos=180) #coluna2






# GRAFICOSSSS!!!!!!!!!!!!!!!!!!!!!


#PRIMEIRO GRAFICO

total_homens = df.iloc[181, 4]  
total_mulheres = df.iloc[361, 4]  

total_homens_alfabetizados = df.iloc[182, 4]  
total_mulheres_alfabetizadas = df.iloc[362, 4]  

porcentagem_homens_alfabetizados = (total_homens_alfabetizados / total_homens) * 100
porcentagem_mulheres_alfabetizadas = (total_mulheres_alfabetizadas / total_mulheres) * 100

#SEGUNDO GRÁFICO

homens_indigenas_alfabetizados = df.iloc[332, 4]  
mulheres_indigenas_alfabetizadas = df.iloc[512, 4] 


#Terceiro Grafico
total_brancos = df.iloc[31, 4]
alfabetizados_brancos = df.iloc[32, 4]

total_negros = df.iloc[61, 4]
alfabetizados_negros = df.iloc[62, 4]

total_orientais = df.iloc[91, 4]
alfabetizados_orientais = df.iloc[92, 4]

total_pardos = df.iloc[121, 4]
alfabetizados_pardos = df.iloc[122, 4]

total_indigenas = df.iloc[151, 4]
alfabetizados_indigenas = df.iloc[152, 4]

porcentagem_brancos_alfabetizados = (alfabetizados_brancos / total_brancos) * 100
porcentagem_negros_alfabetizados = (alfabetizados_negros / total_negros) * 100
porcentagem_orientais_alfabetizados = (alfabetizados_orientais / total_orientais) * 100
porcentagem_pardos_alfabetizados = (alfabetizados_pardos / total_pardos) * 100
porcentagem_indigenas_alfabetizados = (alfabetizados_indigenas / total_indigenas) * 100


#Quarto Grafico
indigenas_alfabetizados_norte = df.iloc[152, 5]  
indigenas_alfabetizados_nordeste = df.iloc[152, 6]   
indigenas_alfabetizados_sudeste = df.iloc[152, 7] 
indigenas_alfabetizados_sul = df.iloc[152, 8]  
indigenas_alfabetizados_centro_oeste = df.iloc[152, 9] 


    
#Quinto grafico
total_15_19 = df.iloc[4, 4]  
alfabetizados_15_19 = df.iloc[5, 4]

total_20_24 = df.iloc[7, 4]  
alfabetizados_20_24 = df.iloc[8, 4]

total_25_34 = df.iloc[10, 4]  
alfabetizados_25_34 = df.iloc[11, 4]

total_35_44 = df.iloc[13, 4]  
alfabetizados_35_44 = df.iloc[14, 4]

total_45_54 = df.iloc[16, 4]  
alfabetizados_45_54 = df.iloc[17, 4]

total_55_64 = df.iloc[19, 4]  
alfabetizados_55_64 = df.iloc[20, 4]

total_65_mais = df.iloc[22, 4]  
alfabetizados_65_mais = df.iloc[23, 4]

total_75_mais = df.iloc[25, 4]  
alfabetizados_75_mais = df.iloc[26, 4]

total_80_mais = df.iloc[28, 4]  
alfabetizados_80_mais = df.iloc[29, 4]

porcentagem_15_19 = (alfabetizados_15_19 / total_15_19) * 100
porcentagem_20_24 = (alfabetizados_20_24 / total_20_24) * 100
porcentagem_25_34 = (alfabetizados_25_34 / total_25_34) * 100
porcentagem_35_44 = (alfabetizados_35_44 / total_35_44) * 100
porcentagem_45_54 = (alfabetizados_45_54 / total_45_54) * 100
porcentagem_55_64 = (alfabetizados_55_64 / total_55_64) * 100
porcentagem_65_mais = (alfabetizados_65_mais / total_65_mais) * 100
porcentagem_75_mais = (alfabetizados_75_mais / total_75_mais) * 100
porcentagem_80_mais = (alfabetizados_80_mais / total_80_mais) * 100



#Sexto grafico
norte = df.iloc[8, 5]  
nordeste = df.iloc[8, 6] 
sudeste = df.iloc[8, 7]  
sul = df.iloc[8, 8]  
centro_oeste = df.iloc[8, 9]  

            
total = norte + nordeste + sudeste + sul + centro_oeste

        
porcentagensss = [(norte / total) * 100,(nordeste / total) * 100,(centro_oeste / total) * 100,(sudeste / total) * 100,(sul / total) * 100]

#Setimo grafico
norte_alfabetizados = df.iloc[2, 5]
norte_total = df.iloc[1, 5]
nordeste_alfabetizados = df.iloc[2, 6]
nordeste_total = df.iloc[1, 6]
sudeste_alfabetizados = df.iloc[2, 7]
sudeste_total = df.iloc[1, 7]
sul_alfabetizados = df.iloc[2, 8]
sul_total = df.iloc[1, 8]
centro_oeste_alfabetizados = df.iloc[2, 9]
centro_oeste_total = df.iloc[1, 9]

porcentagem_norte = (norte_alfabetizados / norte_total) * 100
porcentagem_nordeste = (nordeste_alfabetizados / nordeste_total) * 100
porcentagem_sudeste = (sudeste_alfabetizados / sudeste_total) * 100
porcentagem_sul = (sul_alfabetizados / sul_total) * 100
porcentagem_centro_oeste = (centro_oeste_alfabetizados / centro_oeste_total) * 100


#Oitavo grafico
total_nordeste = df.iloc[2, 6]
total_alagoas = df.iloc[1, 23]
total_bahia = df.iloc[1, 25]
total_ceara = df.iloc[1, 19]
total_maranhao = df.iloc[1, 17]
total_paraiba = df.iloc[1, 21]
total_pernambuco = df.iloc[2, 22]
total_piaui = df.iloc[1, 18]
total_rn = df.iloc[1, 20] 

total_sergipe = df.iloc[1, 24]
alfabet_alagoas = df.iloc[2, 23]
alfabet_bahia =  df.iloc[2, 25]
alfabet_ceara = df.iloc[2, 19]
alfabet_maranhao = df.iloc[2, 17]
alfabet_paraiba = df.iloc[2, 21]
alfabet_pernambuco = df.iloc[2, 22]
alfabet_piaui = df.iloc[2, 18]
alfabet_rn = df.iloc[2, 20]
alfabet_sergipe = df.iloc[2, 24]

porcentagem_alagoas = (alfabet_alagoas / total_alagoas) * 100
porcentagem_bahia = (alfabet_bahia / total_bahia) * 100
porcentagem_ceara = (alfabet_ceara / total_ceara) * 100
porcentagem_maranhao = (alfabet_maranhao / total_maranhao) * 100
porcentagem_paraiba = (alfabet_paraiba / total_paraiba) * 100
porcentagem_pernambuco = (alfabet_pernambuco / total_pernambuco) * 100
porcentagem_piaui = (alfabet_piaui / total_piaui) * 100
porcentagem_rn = (alfabet_rn / total_rn) * 100
porcentagem_sergipe = (alfabet_sergipe / total_sergipe) * 100

proporcao_alagoas = (alfabet_alagoas / total_nordeste) * porcentagem_alagoas
proporcao_bahia = (alfabet_bahia / total_nordeste) * porcentagem_bahia
proporcao_ceara = (alfabet_ceara / total_nordeste) * porcentagem_ceara
proporcao_maranhao = (alfabet_maranhao / total_nordeste) * porcentagem_maranhao
proporcao_paraiba = (alfabet_paraiba / total_nordeste) * porcentagem_paraiba
proporcao_pernambuco = (alfabet_pernambuco / total_nordeste) * porcentagem_pernambuco
proporcao_piaui = (alfabet_piaui / total_nordeste) * porcentagem_piaui
proporcao_rn = (alfabet_rn / total_nordeste) * porcentagem_rn
proporcao_sergipe = (alfabet_sergipe / total_nordeste) * porcentagem_sergipe
        



#Nono grafico
total_sul = df.iloc[2, 8]
total_parana = df.iloc[1,30]
total_sc = df.iloc[1,31]
total_rs = df.iloc[1,32]
alfabetizados_parana = df.iloc[2, 30]
alfabetizados_sc = df.iloc[2, 31]
alfabetizados_rs = df.iloc[2, 32]
porcentagem_parana = (alfabetizados_parana / total_parana) * 100
porcentagem_sc = (alfabetizados_sc / total_sc) * 100
porcentagem_rs = (alfabetizados_rs / total_rs) * 100

proporcao_RS = (alfabetizados_rs / total_sul) * porcentagem_rs
proporcao_SC = (alfabetizados_sc / total_sul) * porcentagem_sc
proporcao_PR = (alfabetizados_parana / total_sul) * porcentagem_parana


#Decimo Grafico
total_norte = df.iloc[2, 5]
total_acre = df.iloc[1, 11]
total_amapa = df.iloc[1, 15]
total_amazonas = df.iloc[1, 12]
total_para = df.iloc[1, 14]
total_rondonia = df.iloc[1, 10]
total_roraima = df.iloc[1, 13]
total_tocantins = df.iloc[1, 16]

alfabet_acre = df.iloc[2, 11]
alfabet_amapa = df.iloc[2, 15]
alfabet_amazonas = df.iloc[2, 12]
alfabet_para = df.iloc[2, 14]
alfabet_rondonia = df.iloc[2, 10]
alfabet_roraima = df.iloc[2, 13]
alfabet_tocantins = df.iloc[2, 16]

porcentagem_acre = (alfabet_acre / total_acre) * 100
porcentagem_amapa = (alfabet_amapa / total_amapa) * 100
porcentagem_amazonas = (alfabet_amazonas / total_amazonas) * 100
porcentagem_para = (alfabet_para / total_para) * 100
porcentagem_rondonia = (alfabet_rondonia / total_rondonia) * 100
porcentagem_roraima = (alfabet_roraima / total_roraima) * 100
porcentagem_tocantins = (alfabet_tocantins / total_tocantins) * 100

proporcao_acre = (total_acre / total_norte) * porcentagem_acre
proporcao_amapa = (total_amapa / total_norte) * porcentagem_amapa
proporcao_amazonas = (total_amazonas / total_norte) * porcentagem_amazonas
proporcao_para = (total_para / total_norte) * porcentagem_para
proporcao_rondonia = (total_rondonia / total_norte) * porcentagem_rondonia
proporcao_roraima = (total_roraima / total_norte) * porcentagem_roraima
proporcao_tocantins = (total_tocantins / total_norte) * porcentagem_tocantins




#PLOTS - CLASE


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        
        
#Plot Graf1
    def plot_gr1(self):
        labels = ['Homens Alfabetizados', 'Mulheres Alfabetizadas']
        sizes = [porcentagem_homens_alfabetizados, porcentagem_mulheres_alfabetizadas]
        colors = ['blue', 'pink']
        explode = (0.1, 0)  # Explodir a fatia dos homens alfabetizados
        
        # Criando o gráfico de pizza
        self.axes.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        self.axes.axis('equal')  # Equaliza o gráfico de pizza
        self.axes.set_title('Porcentagem de Homens e Mulheres Alfabetizados')

#Plot Graf2
    def plot_gr2(self):
        
        labels = ['Homens', 'Mulheres']
        values = [homens_indigenas_alfabetizados, mulheres_indigenas_alfabetizadas]
        colors = ['blue', 'pink']

        
        self.axes.bar(labels, values, color=colors)
        self.axes.set_title('Generos Indígenas Alfabetizados', pad = 20)
        self.axes.set_ylabel('Alfabetizados')
        for i, value in enumerate(values):
            self.axes.text(i, value + 0.5, str(value), ha='center', va='bottom')
        self.axes.set_yticks([0, 100000, 200000, 300000, 400000])
        self.axes.set_ylim(0, 400000)
        
        

#plot Graf3
    def plot_gr3(self):
        labels = ['Brancos', 'Negros', 'Orientais', 'Pardos', 'Indígenas']
        sizes = [ porcentagem_brancos_alfabetizados, porcentagem_negros_alfabetizados, porcentagem_orientais_alfabetizados, porcentagem_pardos_alfabetizados, porcentagem_indigenas_alfabetizados]
        colors = ['white', 'gray', 'green', 'red', 'yellow']
    
        
        self.axes.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        self.axes.axis('equal')
        self.axes.set_title('Porcentagem de Alfabetização por Raça')

#plot Graf4
    def plot_gr4(self):
        estados = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro Oeste']
        valores = [ indigenas_alfabetizados_norte, indigenas_alfabetizados_nordeste, indigenas_alfabetizados_sudeste, indigenas_alfabetizados_sul, indigenas_alfabetizados_centro_oeste]
        
        self.axes.barh(estados, valores, color=['blue', 'yellow', 'red', 'purple', 'green'])
        self.axes.set_title('indigenas alfabetizados por estado')
        self.axes.set_xlabel('Número de Alfabetizados')
        self.axes.set_ylabel('Estados')  
        
        
#plot Graf5
    def plot_gr5(self):
        
        idades = ['15-19 anos', '20-24 anos', '25-34 anos', '35-44 anos', '45-54 anos', '55-64 anos', '65 anos ou mais', '75 anos ou mais', '80 anos ou mais']
        porcentagens = [porcentagem_15_19, porcentagem_20_24, porcentagem_25_34, porcentagem_35_44, porcentagem_45_54, porcentagem_55_64, porcentagem_65_mais, porcentagem_75_mais, porcentagem_80_mais]
        
        
        self.axes.barh(idades, porcentagens, color='lightblue')
        self.axes.set_title('Alfabetização por Idade no Brasil')
        self.axes.set_xlabel('Taxa de Alfabetização (%)')
        self.axes.set_ylabel('Faixa Etária')      
        
#plot Graf6
    def plot_gr6(self):
        regioes = ['Norte', 'Nordeste','Centro-Oeste', 'Sudeste', 'Sul' ]
        cores = ['lightgreen', 'lightcoral', 'lightskyblue', 'gold', 'violet']
       
        
        self.axes.pie(porcentagensss, labels=regioes, colors=cores, autopct='%1.1f%%', shadow=True, startangle=90)
        self.axes.axis('equal')  
        self.axes.set_title('Jovens (20-24 anos) Alfabetizados por Região')
        
#Plot Graf7
    def plot_gr7(self):
        labels = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']
        percentages = [porcentagem_norte, porcentagem_nordeste, porcentagem_sudeste, porcentagem_sul, porcentagem_centro_oeste]
        colors = ['lightblue', 'lightcoral', 'lightgreen', 'orange', 'purple']
        
        self.axes.pie(percentages, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        self.axes.axis('equal') 
        self.axes.set_title('Alfabetizados nas Regiões do Brasil')

#Plot Graf8
    def plot_gr8(self):
        labels = ['Sergipe', 'Bahia', 'Alagoas', 'Maranhão', 'Paraíba', 'Pernambuco', 'Piauí', 'Ceará', 'Rio Grande do Norte']
        porcen = [proporcao_sergipe, proporcao_bahia, proporcao_alagoas, proporcao_maranhao, proporcao_paraiba, proporcao_pernambuco, proporcao_piaui, proporcao_ceara, proporcao_rn]
        colors = ['lightblue', 'lightcoral', 'lightgreen', 'orange', 'purple', 'lightpink', 'gold', 'lightgray', 'cyan']
    
        self.axes.pie(porcen, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, pctdistance=0.7, labeldistance=1)
        self.axes.axis('equal')  
        self.axes.set_title('Alfabetizados por Estado no Nordeste')
        
#Plot Graf9
    def plot_gr9(self):
        labels = ['Rio Grande do Sul', 'Santa Catarina', 'Paraná']
        porcentagens__ = [proporcao_RS, proporcao_SC, proporcao_PR]
        colors = ['gold', 'skyblue', 'lightgreen']
        
        self.axes.pie(porcentagens__, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
        self.axes.axis('equal')  
        self.axes.set_title('Alfabetizados por Estado no Sul')
        
#Plot Graf10
    def plot_gr10(self):
        labels = ['Acre', 'Amapá', 'Amazonas', 'Tocantins', 'Rondônia', 'Roraima', 'Pará']
        pctg = [proporcao_acre, proporcao_amapa, proporcao_amazonas, proporcao_tocantins, proporcao_rondonia, proporcao_roraima, proporcao_para]
        colors = ['lightgreen', 'lightcoral', 'lightskyblue', 'gold', 'violet', 'orange', 'red']
        
        self.axes.pie(pctg, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, pctdistance=0.7, labeldistance=1)
        self.axes.axis('equal')  
        self.axes.set_title('Alfabetizados por Estado no Norte')




#convertendo para vizualização
df.to_csv(os.path.join(caminho_projeto, 'arquivo_convertido.csv'), sep=';', index=False, encoding='utf-8')

print(df.head())






#InterfaceEEEEEEEEEEEEE - CLASSE MAIN

class main():
    
    def __init__(self):
        self.Inter1_MainWindow = QtWidgets.QMainWindow()
        self.Inter1_ui = Inter1.Ui_MainWindow()
        self.Inter1_ui.setupUi(self.Inter1_MainWindow)

        self.Inter2_MainWindow = QtWidgets.QMainWindow()
        self.Inter2_ui = Inter2.Ui_MainWindow()
        self.Inter2_ui.setupUi(self.Inter2_MainWindow)
        
        
        # Definindo layouts para os graficos
        self.verticalLayout_2 = self.Inter2_ui.verticalLayout_2
        self.verticalLayout_3 = self.Inter2_ui.verticalLayout_3
        self.verticalLayout_4 = self.Inter2_ui.verticalLayout_4
        self.verticalLayout_5 = self.Inter2_ui.verticalLayout_5
        self.verticalLayout_6 = self.Inter2_ui.verticalLayout_6
        self.verticalLayout_7 = self.Inter2_ui.verticalLayout_7
        self.verticalLayout_8 = self.Inter2_ui.verticalLayout_8
        self.verticalLayout_9 = self.Inter2_ui.verticalLayout_9
        self.verticalLayout_10 = self.Inter2_ui.verticalLayout_10
        self.verticalLayout_11 = self.Inter2_ui.verticalLayout_11
        
        
        # Fazendo os canvas para os graficos(graficos "falsos")
        self.canvas1 = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.canvas2 = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.canvas3 = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.canvas4 = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.canvas5 = MplCanvas(self, width=5, height=4,   dpi=100)
        self.canvas5.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.canvas6 = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas6.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.canvas7 = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas7.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.canvas8 = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas8.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.canvas9 = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas9.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.canvas10 = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas10.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        
        #espaçamento
        spacer_before = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer_after = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        
        
        #Definindo os layouts verticais p os graficos
        self.verticalLayout_2.addItem(spacer_before)  # Espaço antes do gráfico
        self.verticalLayout_2.addWidget(self.canvas1, alignment=Qt.AlignCenter)  # Centralizando o canvas
        self.verticalLayout_2.addItem(spacer_after)  # Espaço depois do gráfico
        
        self.verticalLayout_3.addItem(spacer_before)
        self.verticalLayout_3.addWidget(self.canvas2, alignment=Qt.AlignCenter)      
        self.verticalLayout_3.addItem(spacer_after)
        
        self.verticalLayout_4.addWidget(self.canvas3,alignment=Qt.AlignCenter )
        
        self.verticalLayout_5.addWidget(self.canvas4, alignment=Qt.AlignCenter)
        
        self.verticalLayout_6.addWidget(self.canvas5, alignment=Qt.AlignCenter)
        
        self.verticalLayout_7.addWidget(self.canvas6, alignment=Qt.AlignCenter)
        
        self.verticalLayout_8.addWidget(self.canvas7, alignment=Qt.AlignCenter)
        
        self.verticalLayout_9.addWidget(self.canvas8, alignment=Qt.AlignCenter)
        
        self.verticalLayout_10.addWidget(self.canvas9, alignment=Qt.AlignCenter)
        
        self.verticalLayout_11.addWidget(self.canvas10, alignment=Qt.AlignCenter)
        

        # Botões para cada grafico
        self.Inter2_ui.g1.clicked.connect(self.plotar_graf1)
        self.Inter2_ui.g3.clicked.connect(self.plotar_graf2)
        self.Inter2_ui.c1.clicked.connect(self.plotar_graf3)
        self.Inter2_ui.c3.clicked.connect(self.plotar_graf4)
        self.Inter2_ui.i1.clicked.connect(self.plotar_graf5)
        self.Inter2_ui.i4.clicked.connect(self.plotar_graf6)
        self.Inter2_ui.r1.clicked.connect(self.plotar_graf7)
        self.Inter2_ui.r3.clicked.connect(self.plotar_graf8)
        self.Inter2_ui.t2.clicked.connect(self.plotar_graf9)
        self.Inter2_ui.t6.clicked.connect(self.plotar_graf10)
        
        # Botão inicio
        self.Inter1_ui.iniciar.clicked.connect(self.abrir)
        
        
        # Botões selecionadores
        self.Inter2_ui.genero.clicked.connect(self.mudar_para_pg)
        self.Inter2_ui.cor.clicked.connect(self.mudar_para_pc)
        self.Inter2_ui.idade.clicked.connect(self.mudar_para_pi)
        self.Inter2_ui.regiao.clicked.connect(self.mudar_para_pr)
        self.Inter2_ui.total.clicked.connect(self.mudar_para_pt)
        self.Inter2_ui.planilha.clicked.connect(self.mudar_para_pp)
        
        
#FUNCOESSSSSS      
        
#Abrir
    def abrir(self):
        if self.Inter1_ui.vamos.isChecked():
            self.Inter2_MainWindow.show()
            self.Inter1_MainWindow.hide()        
            

 # Funções dos graficos
    def plotar_graf1(self):
        self.canvas1.axes.clear()  # Limpar gráfico anterior
        self.canvas1.plot_gr1()   # Gerar novo gráfico de pizza
        self.canvas1.figure.tight_layout()
        self.canvas1.draw()  # Desenhar o gráfico no canvas
        
    def plotar_graf2(self):
        self.canvas2.axes.clear()  
        self.canvas2.plot_gr2()  
        self.canvas2.figure.tight_layout()
        self.canvas2.draw()  
        
    def plotar_graf3(self):
        self.canvas3.axes.clear()  
        self.canvas3.plot_gr3() 
        self.canvas3.figure.tight_layout()
        self.canvas3.draw() 
        
    def plotar_graf4(self):
        self.canvas4.axes.clear()  
        self.canvas4.plot_gr4()  
        self.canvas4.figure.tight_layout()
        self.canvas4.draw()
        
    def plotar_graf5(self):
        self.canvas5.axes.clear()  
        self.canvas5.plot_gr5()  
        self.canvas5.figure.tight_layout()
        self.canvas5.draw()  
    
    def plotar_graf6(self):
        self.canvas6.axes.clear()
        self.canvas6.plot_gr6()
        self.canvas6.figure.tight_layout()
        self.canvas6.draw()

    def plotar_graf7(self):
        self.canvas7.axes.clear()
        self.canvas7.plot_gr7()
        self.canvas7.figure.tight_layout()
        self.canvas7.draw()    
        
    def plotar_graf8(self):
        self.canvas8.axes.clear()
        self.canvas8.plot_gr8()
        self.canvas8.figure.tight_layout()
        self.canvas8.draw()
        
    def plotar_graf9(self):
        self.canvas9.axes.clear()
        self.canvas9.plot_gr9()
        self.canvas9.figure.tight_layout()
        self.canvas9.draw()    
        
    def plotar_graf10(self):
        self.canvas10.axes.clear()
        self.canvas10.plot_gr10()
        self.canvas10.figure.tight_layout()
        self.canvas10.draw()   
        
            
# Funções para mudar de página
    def mudar_para_pg(self):
        self.Inter2_ui.stackedWidget.setCurrentWidget(self.Inter2_ui.pg)
        
    def mudar_para_pc(self):
        self.Inter2_ui.stackedWidget.setCurrentWidget(self.Inter2_ui.pc)
        
    def mudar_para_pi(self):
        self.Inter2_ui.stackedWidget.setCurrentWidget(self.Inter2_ui.pi)
        
    def mudar_para_pr(self):
        self.Inter2_ui.stackedWidget.setCurrentWidget(self.Inter2_ui.pr)
        
    def mudar_para_pt(self):
        self.Inter2_ui.stackedWidget.setCurrentWidget(self.Inter2_ui.pt)
        
    def mudar_para_pp(self):
        self.Inter2_ui.stackedWidget.setCurrentWidget(self.Inter2_ui.pp)
        self.carregar_tabela_pp()  # Carregar tabela sempre que mudar para a página pp
        
        
#Carregar tabela      
    def carregar_tabela_pp(self):
        model = QStandardItemModel()  # Modelo que armazena os dados
        model.setHorizontalHeaderLabels([str(col) for col in df.columns])  # Definir cabeçalhos

        # Adicionar as linhas da planilha ao modelo
        for row in df.values:
            itens = [QStandardItem(str(item)) for item in row]  # Cada linha é um item
            model.appendRow(itens)

        # Conectar o modelo ao QTableView na página "pp"
        self.Inter2_ui.tabela_pp.setModel(model)
        self.Inter2_ui.tabela_pp.resizeColumnsToContents()           
    
        
               
            
            
            
        
        
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv) 
    MainWindow = QtWidgets
    c = main()
    c.Inter1_MainWindow.show()
    sys.exit(app.exec_())   


        