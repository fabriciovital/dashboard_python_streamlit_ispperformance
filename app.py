import streamlit as st
import pandas as pd
import psycopg2

# Função para estabelecer a conexão com o banco de dados PostgreSQL
def get_connection():
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="postgres",
        user="fabricio",
        password="kr8c4s%w"
    )
    return conn

# Função para buscar os dados do PostgreSQL
def fetch_data(query):
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Define a configuração da página no Streamlit
st.set_page_config(page_title="ISQ Performance", page_icon="🌍", layout="wide")

# Define o título da página
st.title('ISQ Performance')

# Função principal do Streamlit
def main():
    st.title("Análise de Atendimentos")

    # Consulta para buscar estados da tabela dim_cidade
    query_estados = "SELECT sk_cidade, UF FROM dim_cidade ORDER BY UF;"
    df_estados = fetch_data(query_estados)

    # Configura os filtros na barra lateral para estado
    estados = st.sidebar.multiselect(
        "Selecione Estado",
        options=df_estados["uf"].unique(),
        default=df_estados["uf"].unique(),
    )

    # Consulta para buscar cidades da tabela dim_cidade com base nos estados selecionados
    if estados:
        query_cidades = f"""
        SELECT DISTINCT Cidade 
        FROM dim_cidade 
        WHERE UF IN ({','.join([f"'{estado}'" for estado in estados])}) 
        ORDER BY Cidade;
        """
    else:
        query_cidades = """
        SELECT DISTINCT Cidade 
        FROM dim_cidade 
        ORDER BY Cidade;
        """
    df_cidades = fetch_data(query_cidades)

    # Configura os filtros na barra lateral para cidade
    cidades = st.sidebar.multiselect(
        "Selecione Cidade",
        options=df_cidades["cidade"].unique(),
        default=df_cidades["cidade"].unique(),
    )

    # Consulta para buscar filiais com base nas cidades selecionadas
    if cidades:
        query_filiais = """
        SELECT DISTINCT Filial 
        FROM dim_filial 
        WHERE cidade IN ({}) 
        ORDER BY Filial;
        """.format(",".join(["'{}'".format(cidade.replace("'", "''")) for cidade in cidades]))
    else:
        query_filiais = """
        SELECT DISTINCT Filial 
        FROM dim_filial 
        ORDER BY Filial;
        """
    df_filiais = fetch_data(query_filiais)

    # Configura os filtros na barra lateral para filial
    filiais = st.sidebar.multiselect(
        "Selecione Filial",
        options=df_filiais["filial"].unique(),
        default=df_filiais["filial"].unique(),
    )

    # Exibição dos dados filtrados
    st.write("Estados selecionados:", estados)
    st.write("Cidades selecionadas:", cidades)
    st.write("Filiais selecionadas:", filiais)

    # Aqui você pode adicionar consultas adicionais ou exibir gráficos/tabelas com base nas seleções feitas
    # ...

if __name__ == "__main__":
    main()
