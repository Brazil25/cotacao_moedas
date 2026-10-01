import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import requests
from tkinter.filedialog import askopenfilename
import pandas as pd
from datetime import datetime
import numpy as np

requisicao = requests.get("https://economia.awesomeapi.com.br/json/all")
dicionario_moedas = requisicao.json()
lista_moedas = list(dicionario_moedas.keys())


def pegar_cotacao():
    moeda = combobox_selecionar_moeda.get()
    data_cotacao = calendario_moeda.get()
    ano = data_cotacao[-4:]
    mes = data_cotacao[3:5]
    dia = data_cotacao[:2]
    link = f"https://economia.awesomeapi.com.br/json/daily/{moeda}-BRL/?start_date={ano+mes+dia}&end_date={ano+mes+dia}"
    requisicao_moeda = requests.get(link)
    cotacao = requisicao_moeda.json()
    valor_moeda = cotacao[0]["bid"]
    label_texto_cotacao["text"] = f"A cotação da {moeda} no dia {data_cotacao} foi de: R${valor_moeda}"


def selecionar_arquivo():
    caminho_arquivo = askopenfilename(title="Selecione o arquivo de moedas")
    var_caminho_arquivo.set(caminho_arquivo)
    if caminho_arquivo:
        label_arquivo_selecionado["text"] = f"Arquivo Selecionado: {caminho_arquivo}"


def atualizar_cotacoes():
    try:
        df = pd.read_excel(var_caminho_arquivo.get())
        moedas = df.iloc[:,0]
        data_inicial_str = calendario_data_inicial.get()
        data_final_str = calendario_data_final.get() 
        dt_inicial = datetime.strptime(data_inicial_str, "%d/%m/%Y")
        dt_final = datetime.strptime(data_final_str, "%d/%m/%Y")
        numero_dias = (dt_final - dt_inicial).days + 1
        start_date = dt_inicial.strftime("%Y%m%d")
        end_date = dt_final.strftime("%Y%m%d")
        for moeda in moedas:
            link = f"https://economia.awesomeapi.com.br/json/daily/{moeda}-BRL/{numero_dias}?start_date={start_date}&end_date={end_date}"
            requisicao_moeda = requests.get(link)
            cotacoes = requisicao_moeda.json()
            for cotacao in cotacoes:
                timestamp = int(cotacao["timestamp"])
                bid = float(cotacao["bid"])
                data = datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y") 
                if data not in df.columns:
                    df[data] = np.nan 
                df.loc[df.iloc[:,0] == moeda, data] = bid
        df.to_excel("Cotacoes.xlsx", index=False)
        label_atualizar_cotacoes["text"] = "Arquivo atualizado com sucesso!"
    except:
        label_atualizar_cotacoes["text"] = "Selecione um arquivo Excel no formato correto!"      

janela = tk.Tk()
janela.title("Ferramenta de Cotação de Moedas")


janela.columnconfigure(0, weight=1)
janela.columnconfigure(1, weight=1)
janela.columnconfigure(2, weight=1)

for i in range(11):
    janela.rowconfigure(i, weight=1)

#linha 0
label_cotacao_moeda = tk.Label(text="Cotação de uma Moeda Específica", borderwidth=2, relief="solid", bg="goldenrod", fg="black")
label_cotacao_moeda.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW", columnspan=3)

#linha 1
label_selecionar_moeda= tk.Label(text="Selecione a moeda:", anchor="e")
label_selecionar_moeda.grid(row=1, column=0, padx=10, pady=10, sticky="NSEW", columnspan=2)

combobox_selecionar_moeda = ttk.Combobox(values=lista_moedas)
combobox_selecionar_moeda.grid(row=1, column=2, padx=10, pady=10, sticky="NSEW")

#linha 2
label_selecionar_dia= tk.Label(text="Selecione o dia de que deseja pegar a cotação:", anchor="e")
label_selecionar_dia.grid(row=2, column=0, padx=10, pady=10, sticky="NSEW", columnspan=2)

calendario_moeda = DateEntry(year=2026, locale="pt_br")
calendario_moeda.grid(row=2, column=2, padx=10, pady=10, sticky="NSEW")

#linha 3
label_texto_cotacao = tk.Label(text="")
label_texto_cotacao.grid(row=3, column=0, padx=10, pady=10, sticky="NSEW", columnspan=2)

botao_pegar_cotacao = tk.Button(text="Pegar Cotação", command=pegar_cotacao, bg="gold", fg="black")
botao_pegar_cotacao.grid(row=3, column=2, padx=10, pady=10, sticky="NSEW")

#linha 4
label_cotacao_multiplas = tk.Label(text="Cotação de Múltiplas Moedas", borderwidth=2, relief="solid",  bg="goldenrod", fg="black")
label_cotacao_multiplas.grid(row=4, column=0, padx=10, pady=10, sticky="NSEW", columnspan=3)

#linha 5
label_selecionar_arquivo = tk.Label(text="Selecione o arquivo em Excel com as moedas na coluna A:")
label_selecionar_arquivo.grid(row=5, column=0, padx=10, pady=10, sticky="NSEW", columnspan=2)

var_caminho_arquivo = tk.StringVar()

botao_selecionar_arquivo = tk.Button(text="Clique para Selecionar", command=selecionar_arquivo, bg="green2", fg="black")
botao_selecionar_arquivo.grid(row=5, column=2, padx=10, pady=10, sticky="NSEW")

#linha 6
label_arquivo_selecionado = tk.Label(text="Nenhum Arquivo Selecionado", anchor="e")
label_arquivo_selecionado.grid(row=6, column=0, padx=10, pady=10, sticky="NSEW", columnspan=3)

#linha 7
label_data_inicial = tk.Label(text="Data Inicial:", anchor="e")
label_data_inicial.grid(row=7, column=0, padx=10, pady=10, sticky="NSEW")

calendario_data_inicial = DateEntry(year=2026, locale="pt_br")
calendario_data_inicial.grid(row=7, column=1, padx=10, pady=10, sticky="NSEW")

#linha 8
label_data_final = tk.Label(text="Data Final:", anchor="e")
label_data_final.grid(row=8, column=0, padx=10, pady=10, sticky="NSEW")

calendario_data_final = DateEntry(year=2026, locale="pt_br")
calendario_data_final.grid(row=8, column=1, padx=10, pady=10, sticky="NSEW")

#linha 9
botao_atualizar_cotacoes = tk.Button(text="Atualizar Cotações", command=atualizar_cotacoes, bg="gold", fg="black")
botao_atualizar_cotacoes.grid(row=9, column=0, padx=10, pady=10, sticky="NSEW")

label_atualizar_cotacoes = tk.Label(text="")
label_atualizar_cotacoes.grid(row=9, column=1, padx=10, pady=10, sticky="NSEW", columnspan=2)

#linha 10
botao_fechar = tk.Button(text="Fechar", command=janela.quit, bg="red", fg="black")
botao_fechar.grid(row=10, column=0, padx=10, pady=10, sticky="NSEW", columnspan=3)

#Abrir a janela
janela.mainloop()