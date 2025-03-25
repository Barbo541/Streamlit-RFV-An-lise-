# Imports
import pandas as pd
import streamlit as st
import numpy as np

from datetime import datetime
from PIL import Image
from io import BytesIO

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

@st.cache_data
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    return processed_data

def recencia_class(x, r, q_dict):
    if x <= q_dict[r][0.25]:
        return 'A'
    elif x <= q_dict[r][0.50]:
        return 'B'
    elif x <= q_dict[r][0.75]:
        return 'C'
    else:
        return 'D'

def freq_val_class(x, fv, q_dict):
    if x <= q_dict[fv][0.25]:
        return 'D'
    elif x <= q_dict[fv][0.50]:
        return 'C'
    elif x <= q_dict[fv][0.75]:
        return 'B'
    else:
        return 'A'

def main():
    st.set_page_config(
        page_title='Dashboard RFV',
        layout="wide",
        initial_sidebar_state='expanded'
    )

    st.title("📊 Análise de Clientes com Segmentação RFV")
    st.markdown("""
    A metodologia **RFV** (Recência, Frequência, Valor) é uma técnica essencial para entender o comportamento dos clientes.
    Ela permite classificar sua base em segmentos valiosos para tomada de decisão em marketing, retenção e fidelização.
    
    ---
    """)

    st.sidebar.header("📂 Upload de Dados")
    data_file_1 = st.sidebar.file_uploader("Escolha o arquivo de compras (.csv ou .xlsx)", type=['csv', 'xlsx'])

    if data_file_1 is not None:
        try:
            df_compras = pd.read_csv(
                data_file_1,
                infer_datetime_format=True,
                parse_dates=['DiaCompra'],
                encoding='latin1'
            )
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")
            return

        st.subheader("🧮 Cálculo dos Parâmetros RFV")

        dia_atual = df_compras['DiaCompra'].max()
        st.markdown(f"**Data de referência (mais recente na base):** `{dia_atual.date()}`")

        st.markdown("### 🔹 Recência (R) - Dias desde a última compra")
        df_recencia = df_compras.groupby(by='ID_cliente', as_index=False)['DiaCompra'].max()
        df_recencia.columns = ['ID_cliente', 'DiaUltimaCompra']
        df_recencia['Recencia'] = df_recencia['DiaUltimaCompra'].apply(lambda x: (dia_atual - x).days)
        st.dataframe(df_recencia.head(), use_container_width=True)
        df_recencia.drop('DiaUltimaCompra', axis=1, inplace=True)

        st.markdown("### 🔹 Frequência (F) - Total de compras no período")
        df_frequencia = df_compras.groupby('ID_cliente')['CodigoCompra'].count().reset_index()
        df_frequencia.columns = ['ID_cliente', 'Frequência']
        st.dataframe(df_frequencia.head(), use_container_width=True)

        st.markdown("### 🔹 Valor (V) - Total gasto por cliente")
        df_valor = df_compras.groupby('ID_cliente')['ValorTotal'].sum().reset_index()
        df_valor.columns = ['ID_cliente', 'Valor']
        st.dataframe(df_valor.head(), use_container_width=True)

        df_RF = df_recencia.merge(df_frequencia, on='ID_cliente')
        df_RFV = df_RF.merge(df_valor, on='ID_cliente').set_index('ID_cliente')

        st.markdown("### 📊 Tabela Consolidada RFV")
        st.dataframe(df_RFV.head(), use_container_width=True)

        st.markdown("### 📏 Cálculo dos Quartis para Classificação")
        quartis = df_RFV.quantile(q=[0.25, 0.5, 0.75])
        st.dataframe(quartis)

        df_RFV['R_quartil'] = df_RFV['Recencia'].apply(recencia_class, args=('Recencia', quartis))
        df_RFV['F_quartil'] = df_RFV['Frequência'].apply(freq_val_class, args=('Frequência', quartis))
        df_RFV['V_quartil'] = df_RFV['Valor'].apply(freq_val_class, args=('Valor', quartis))
        df_RFV['RFV_Score'] = df_RFV.R_quartil + df_RFV.F_quartil + df_RFV.V_quartil

        # criar coluna de ações antes do filtro
        dict_acoes = {
            'AAA': 'Top clientes! Fidelizar com recompensas.',
            'AAB': 'Alto potencial. Incentivar mais compras.',
            'ABB': 'Clientes recentes e frequentes.',
            'DDD': 'Inativos. Reengajar ou descartar.',
            'DAA': 'Clientes antigos e valiosos. Tentar recuperar.',
            'CAA': 'Clientes importantes mas ausentes.',
            'ABC': 'Clientes com potencial para crescer.',
            'CBB': 'Frequentes mas com baixo valor. Upselling?',
            'AAC': 'Compradores recentes mas baixo ticket.'
        }

        df_RFV['acoes de marketing/crm'] = df_RFV['RFV_Score'].map(dict_acoes).fillna("Analisar individualmente")

        st.markdown("### 🧩 Clientes Segmentados por Score RFV")
        selected_scores = st.multiselect(
            "Filtrar por RFV Score:",
            options=sorted(df_RFV['RFV_Score'].unique()),
            default=sorted(df_RFV['RFV_Score'].unique())
        )
        df_filtered = df_RFV[df_RFV['RFV_Score'].isin(selected_scores)]
        st.dataframe(df_filtered[['Recencia', 'Frequência', 'Valor', 'RFV_Score', 'acoes de marketing/crm']], use_container_width=True)

        st.markdown("### 📈 Distribuição dos Scores RFV")
        st.bar_chart(df_RFV['RFV_Score'].value_counts())

        st.markdown("### 🛠 Sugestões de Ações para os Segmentos")
        st.dataframe(
            df_filtered[['RFV_Score', 'acoes de marketing/crm']]
            .value_counts().reset_index(name='Qtd'),
            use_container_width=True
        )

        df_xlsx = to_excel(df_RFV)
        st.download_button(label='📥 Baixar Tabela RFV em Excel', data=df_xlsx, file_name='RFV_segmentado.xlsx')

        st.success("Análise concluída com sucesso! Veja acima os insights de segmentos.")

if __name__ == '__main__':
    main()
