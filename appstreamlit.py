#importação de bibliotecas necessárias
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime

PATH = 'https://raw.githubusercontent.com/jonhsel/Data-Science/master/dataset/MVIMPM_Tratado.csv'


#def main():
@st.cache(allow_output_mutation=True)
def loadData():
    dataframe = pd.read_csv(PATH)
    return dataframe
df = loadData()

#st.sidebar.image('LogomarcaNova.png', width=300)
st.sidebar.title('CAOP-CRIM / MPMA')
#st.title('Centro de Apoio Operacional Criminal')
st.title('MVI - GRANDE ILHA DE SÃO LUÍS')
st.subheader('Mortes Violentas Intencionais')


#st.dataframe(df.head(5))
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
                    xytext=(0, 10), textcoords='offset points', fontsize=20)
    # fig.autofmt_xdate()
    st.pyplot()

def Pxplot():
    k = df['Data'].dt.year.value_counts()
    Crime = pd.Series(k.index[:])
    Count = list(k[:])
    Crime_Count = pd.DataFrame(list(zip(Crime, Count)),columns=['Crime', 'Count'])
    fig = px.bar(Crime_Count, x='Crime', y='Count', color_continuous_scale='YlOrBr' ,color='Count', labels={'Crime': 'Ano', 'Count': 'Quantidade'})
    st.plotly_chart(fig)

graficoano = st.sidebar.checkbox('Quantitativos por ano')
if graficoano:
    tiposgrafico = st.radio('Modelos de gráficos', ('Estático', 'Interativo'))
    if tiposgrafico == 'Estático':
        plotanoSeaborn()
    if tiposgrafico == 'Interativo':
        Pxplot()


#     st.text('**Criar botao**')
#     botao = st.button('botao')
#     if botao:
#         st.markdown('Botão pressionado')
#
#     st.text('**Criar Checkbox')
#     check = st.checkbox('chequibox')
#     if check:
#         st.markdown('Registros do ano XXXX')
#
#
#     st.text('**Criar Radio**')
#     radio = st.radio('Escolha os anos',('nenhum','2017', '2018'))
#     if radio == '2017':
#         st.markdown('Colocar seleção df 2017')
#     if radio == '2018':
#         st.markdown('Colocar seleção 2018')
#
#     st.text('**selectbox**')
#     selectBox = st.selectbox('Selecione um ano', ('nenhum', '2017', '2018'))
#     if selectBox=='2017':
#         st.markdown('Gráficos e codigos')
#     if selectBox == '2018':
#         st.markdown('Graicos 2018')
# """

#if __name__ == '__main__':
#    main()


