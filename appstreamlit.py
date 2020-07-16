#importação de bibliotecas necessárias
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from datetime import datetime

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")
PATH = 'https://raw.githubusercontent.com/jonhsel/Data-Science/master/dataset/MVIMPM_Tratado.csv'


#def main():
@st.cache(allow_output_mutation=True)



def loadData():
    dataframe = pd.read_csv(PATH)
    return dataframe
df = loadData()

def information_caop():
    st.markdown(
        '''
        O **Centro de Apoio Operacional Criminal**, instituído por meio da Resolução 02/97-CPMP, tendo esta norma sido alterada pela Resolução n.º 34/2016-CPMP, é um órgão auxiliar da atividade funcional do Ministério Público do Maranhão, que possui, dentre outros, o objetivo de melhorar o desempenho das funções institucionais dos órgãos de execução do Parquet Maranhense, promovendo-lhes a devida interação e intercâmbio, sendo-lhes - além disso - dadas orientações técnico jurídicas com a remessa de informações de mesma natureza e, além disso, tem por finalidade promover a articulação, harmonização, mediação de relações e a integração das ações voltadas à segurança pública e defesa social com atribuições em todo espaço territorial maranhense.
        
        ## **ÂMBITO INTERNO**
        
        1.1 - atuar na área da segurança  pública, prevenção e  redução dos  índices  de criminalidade, persecução penal, execução penal e controle externo da atividade policial, abrangendo a criminal, além de outras correlatas;

        1.2 - atuar por meio de ações coordenadas, para dar efetividade ao exercício da função constitucional do Ministério Público no controle externo da atividade policial, buscando uma maior integração entre Ministério Público e órgãos policiais;

        1.3 - estabelecer intercâmbio permanente entre os Órgãos do Sistema de Segurança Pública e Defesa Social e entidades não governamentais que atuam direta ou indiretamente em áreas afins, para obtenção de elementos técnicos especializados, necessários ao desempenho das funções ministeriais para consecução dos fins da Justiça Criminal;

        1.4 - colaborar com os órgãos do Estado, notadamente na área de segurança, na identificação dos principais problemas relativos à violência, tais como levantamento das áreas de maior incidência de criminalidade, assim como dos crimes mais frequentes, identificando, ainda, o perfil do criminoso e da vítima.
        
        ## **ÂMBITO EXTERNO**
                      
        2.1  - fornecer, de ofício ou por provocação, informações técnico-jurídicas aos órgãos de execução do Ministério Público; com vistas a manter a uniformidade do exercício funcional, observando os princípios da unidade, da indivisibilidade e da independência funcional;

        2.2 - expedir recomendações visando à melhoria dos serviços públicos e respeito aos interesses, direitos e bens, fixando prazo para adoção das providências cabíveis;

        2.3 - receber representações ou qualquer outro expediente, de natureza criminal,  transmitindo-os aos órgãos encarregados de apreciá-las, ou restituindo-os à origem, para o correto encaminhamento, se a competência para apreciar o fato não for da Justiça do Estado do Maranhão;

        2.4 - desenvolver estudos e pesquisas e sugerir a criação de grupos e comissões de trabalho;

        2.5 - coordenar a realização de cursos, palestras e outros eventos, visando à efetiva capacitação dos órgãos de execução;
        '''
    )

def information_mvi():
    st.markdown(
        '''
        A metodologia **MVI (Mortes Violentas Intencionais)** é a forma utilizada pelo Instituto de Pesquisas Econômicas Aplicada (**IPEA**) e pelo Fórum Brasileiro de Segurança Pública (**FSBP**) para a elaboração dos **“Atlas da Violência”**. Os MVI contemplam, como forma de mortalidade violenta, os homicídios dolosos, latrocínios (roubos seguidos de morte), lesões corporais seguida de morte, vitimização policial, mortes decorrentes de intervenção policial, lesões com morte posterior, mortes em estabelecimentos prisionais com indícios de crime e mortes a esclarecer com indícios de crime.
        '''
    )

st.sidebar.image('LogomarcaNova.png', width=300)
st.sidebar.title('CAOP-CRIM / MPMA')
#st.title('Centro de Apoio Operacional Criminal')
st.title('MVI - GRANDE ILHA DE SÃO LUÍS')
st.subheader('Mortes Violentas Intencionais')


#st.dataframe(df.head(5))
informacao = st.sidebar.checkbox('Informações')
if informacao:
    descricao = st.selectbox('Selecione para saber mais!', ('Site','CAOp-Crim', 'MVI'))
    if descricao == 'Site':
        st.markdown(
            '''
            
            [CAOp-Criminal](https://www.mpma.mp.br/index.php/centros-de-apoio/criminal2)
            
            '''
        )
    if descricao == 'CAOp-Crim':
        information_caop()
    if descricao == 'MVI':
        information_mvi()



tabela_registros = st.sidebar.checkbox('Tabela de registros')
if tabela_registros:
    slider = st.slider('Defina a quantidade de registros a serem mostrados', 1, 100)
    st.table(df.head(slider))
#st.write(df.info())

#transformar variavel em datetime
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
#ano = df['Data'].dt.year.value_counts()
#st.table(ano)

def plotanoSeaborn():
    x = df['Data'].dt.year
    sns.set(style='white')
    fig, ax = plt.subplots(figsize=(16, 9))
    sns.countplot(x, palette='YlOrBr_r', ax=ax)
    ax.set_title('Ocorrências de MVI por TODOS OS ANOS', fontsize=20)
    ax.set_xlabel('Ano', fontsize=20)
    ax.set_ylabel('Quantidade', fontsize=20)
    for p in ax.patches:
        ax.annotate(p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),
                    xytext=(0, 5), textcoords='offset points', fontsize=20)
    # fig.autofmt_xdate()
    st.pyplot()

ymaximo_g01 = df.groupby(['Município'])['ID'].count().max()
ymaximo_g02 = df.groupby(['CAUSA DA MORTE'])['ID'].count().max()

def plot_city():
    # ANO
    sns.set(style="white")
    # sns.palplot(sns.dark_palette("purple"))

    fig, ax1 = plt.subplots( figsize=(10, 6))

    sns.countplot(df['Município'], palette='Blues_r', ax=ax1)
    # https://seaborn.pydata.org/tutorial/color_palettes.html
    ax1.set_title('Quantitativos de 2017 a 2020')
    ax1.set_xlabel('Município')
    ax1.set_ylabel('Quantidade')
    # instrução para que o rótulo não sobreponha a grade que circunda o gráfico
    ax1.set_ylim(0, ymaximo_g01 + 100)

    # GRÁFICO 01
    # laço para inclusão dos rótulos
    for p in ax1.patches:
        # Não tulizaremos valores decimais nos rótulos
        # ax1.annotate("%.2f" % p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),
        ax1.annotate(p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', fontsize=13, color='black', xytext=(0, 10),
                     textcoords='offset points')
    # To make space for the annotations
    #fig.show()
    # fig.autofmt_xdate()
    #fig.tight_layout()
    st.pyplot()

def plot_causa():
    sns.set(style="white")
    # sns.palplot(sns.dark_palette("purple"))

    fig, ax2 = plt.subplots( figsize=(10, 6))

    # To make space for the annotations

    # GRÁFICO 02
    sns.countplot(df['CAUSA DA MORTE'], palette='Blues_d', ax=ax2)
    ax2.set_title('Quantitativos de 2017 a 2020')
    ax2.set_xlabel('Causa da morte')
    ax2.set_ylabel('Quantidade')
    # instrução para que o rótulo não sobreponha a grade que circunda o gráfico
    ax2.set_ylim(0, ymaximo_g02 + 100)

    # laço para inclusão dos rótulos
    for p in ax2.patches:
        # Não tulizaremos valores decimais nos rótulos
        # ax1.annotate("%.2f" % p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),
        ax2.annotate(p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', fontsize=13, color='black', xytext=(0, 10),
                     textcoords='offset points')

    # fig.show()
    # fig.autofmt_xdate()
    # fig.tight_layout()
    st.pyplot()


def Pxplot():
    k = df['Data'].dt.year.value_counts()
    Crime = pd.Series(k.index[:])
    Count = list(k[:])
    Crime_Count = pd.DataFrame(list(zip(Crime, Count)),columns=['Crime', 'Count'])
    fig = px.bar(Crime_Count, x='Crime', y='Count', color_continuous_scale='YlOrBr' ,color='Count', labels={'Crime': 'Ano', 'Count': 'Quantidade'})
    st.plotly_chart(fig)

grafico_city = st.sidebar.checkbox('Gŕafico de Município e Causa')
if grafico_city:
    graficos2 = st.radio('Modelos de gráficos', ('Município', 'Causa da morte'))
    if graficos2 == 'Município':
        plot_city()
    if graficos2 == 'Causa da morte':
        plot_causa()

graficoano = st.sidebar.checkbox('Quantitativos por ano')
if graficoano:
    tiposgrafico = st.radio('Modelos de gráficos', ('Estático', 'Interativo'))
    if tiposgrafico == 'Estático':
        plotanoSeaborn()
    if tiposgrafico == 'Interativo':
        Pxplot()


def wordcloud():
    # criar uma cópia do DataFrame original
    df_wordcloud = pd.read_csv("https://raw.githubusercontent.com/jonhsel/Data-Science/master/dataset/MVIMPMA_VIT.csv")

    # seleção das colunas
    df_wordcloud = df_wordcloud[['Vítima', 'Sexo', 'CAUSA DA MORTE', 'Local', 'Município', 'Classificação']]
    #df_wordcloud = df_wordcloud[['Vítima', 'Sexo', 'Local', 'Município']]

    df_wordcloud.fillna('UNKNOWN', axis=1, inplace=True)

    #rotina para transformar o dataset em um unico arquivo
    lista = []
    for i in df_wordcloud.columns:
        text = " ".join(s for s in df_wordcloud[i])
        lista.append(text)

    texto2 = str(lista)

    #setando a máscara
    grandeilha_mask = np.array(Image.open("ilhaBlack.png"))

    # Definir as stopwords
    stopwords = set(STOPWORDS)
    stopwords.update(['de', 'UNKNOWN', 'dos', 'da'])

    # Criar a nuvem de palavras
    wordcloudW = WordCloud(stopwords=stopwords,
                          background_color='black',
                          width=2000, height=2000, max_words=2000,
                          mask=grandeilha_mask, max_font_size=200, colormap='Reds'
                          ).generate(texto2)

    # criar a imagem
    fig, ax = plt.subplots(figsize=(16, 16))
    ax.imshow(wordcloudW, interpolation='bilinear')
    ax.set_axis_off()

    st.pyplot()


nuvemPalavras = st.sidebar.checkbox('WordCloud')
if nuvemPalavras:
    wordcloud()
#if __name__ == '__main__':
#    main()


