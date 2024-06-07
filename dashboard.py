import psycopg2
import pandas as pd
import streamlit as st
import plotly.express as px

def get_connection():
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="postgres",
        user="fabricio"
        ,
        password="kr8c4s%w"

    )
    return conn

def fetch_data(query):
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

#if __name__ == "__main__":
 #   query = "SELECT * FROM FATO_ATENDIMENTO LIMIT 10"  # Substitua 'sua_tabela' pelo nome da sua tabela
  #  data = fetch_data(query)
   # print(data)


def main():
    st.title("Dashboard de Performance")

    # Query SQL para buscar os dados
    query = """
    SELECT * FROM sua_tabela
    """

    # Buscar os dados do PostgreSQL
    data = fetch_data(query)

    # Mostrar os dados no Streamlit
    st.write(data)

    # Criar um gráfico com Plotly
    fig = px.line(data, x='coluna_x', y='coluna_y', title='Gráfico de Exemplo')
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()

