import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import altair as alt

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
def fetch_data(query, params=None):
    conn = get_connection()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

# Define a configuração da página no Streamlit
st.set_page_config(page_title="ISP Performance", page_icon="🌍", layout="wide")

st.header("ANALISE DE PERFORMANCE | INDICADORES & PROGRESSÃO ")

# Load Style CSS
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Antes de main()
if "expander_state" not in st.session_state:
    st.session_state.expander_state = False

# Função principal do Streamlit
def main():    

     # Botão Expandir/Recolher
    expandir_recolher = st.button("Expandir/Recolher")

# Verifica se o botão foi pressionado
    if expandir_recolher:
        # Alterna o estado do expander
        st.session_state.expander_state = not st.session_state.expander_state

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
        query_cidades = """
        SELECT DISTINCT Cidade 
        FROM dim_cidade 
        WHERE UF IN %s 
        ORDER BY Cidade;
        """
        params_cidades = (tuple(estados),)
    else:
        query_cidades = """
        SELECT DISTINCT Cidade 
        FROM dim_cidade 
        ORDER BY Cidade;
        """
        params_cidades = None
    df_cidades = fetch_data(query_cidades, params=params_cidades)

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
        WHERE cidade IN %s 
        ORDER BY Filial;
        """
        params_filiais = (tuple(cidades),)
    else:
        query_filiais = """
        SELECT DISTINCT Filial 
        FROM dim_filial 
        ORDER BY Filial;
        """
        params_filiais = None
    df_filiais = fetch_data(query_filiais, params=params_filiais)

    # Configura os filtros na barra lateral para filial
    filiais = st.sidebar.multiselect(
        "Selecione Filial",
        options=df_filiais["filial"].unique(),
        default=df_filiais["filial"].unique(),
    )

    # Converte os filtros selecionados para tipos nativos do Python
    estados = [str(estado) for estado in estados]
    cidades = [str(cidade) for cidade in cidades]
    filiais = [str(filial) for filial in filiais]

    # Construindo a consulta principal dinamicamente
    query_atendimentos = """
    SELECT 
        fa.id,
        dda.data_completa AS data_abertura,
        fa.hora_abertura,
        ddag.data_completa AS data_agendamento,
        fa.hora_agendamento,
        ddi.data_completa AS data_inicio,
        fa.hora_inicio,
        ddf.data_completa AS data_finalizacao,
        ddf.nr_ano AS nr_ano_finalizacao,
        ddf.nr_mes AS nr_mes_finalizacao,
        ddf.nm_mes AS nm_mes_finalizacao,
        ddf.nr_dia_mes AS nr_dia_mes_finalizacao,
        ddf.nm_dia_semana AS nm_dia_semana_finalizacao,
        ddf.nm_trimestre AS nm_trimestre_finalizacao,
        ddf.nr_ano_nr_mes AS nr_ano_nr_mes_finalizacao,
        fa.hora_finalizacao,
        fa.sla,
        fa.liberado,
        fa.mensagem,
        fa.impresso,
        dc.UF,
        dc.Cidade,
        df.Filial,
        dt.tipo_atendimento,
        ds.status,
        dcl.cliente,
        das.assunto,
        dse.setor,
        dco.colaborador,
        dp.prioridade
    FROM 
        fato_atendimento fa
        JOIN dim_cidade dc ON fa.sk_cidade = dc.sk_cidade
        JOIN dim_filial df ON fa.sk_filial = df.sk_filial
        JOIN dim_tipo_atendimento dt ON fa.sk_tipo_atendimento = dt.sk_tipo_atendimento
        JOIN dim_status ds ON fa.sk_status = ds.sk_status
        JOIN dim_cliente dcl ON fa.sk_cliente = dcl.sk_cliente
        JOIN dim_assunto das ON fa.sk_assunto = das.sk_assunto
        JOIN dim_setor dse ON fa.sk_setor = dse.sk_setor
        JOIN dim_colaborador dco ON fa.sk_colaborador = dco.sk_colaborador
        JOIN dim_prioridade dp ON fa.sk_prioridade = dp.sk_prioridade
        JOIN dim_tempo dda ON fa.sk_data_abertura = dda.sk_data
        JOIN dim_tempo ddag ON fa.sk_data_agendamento = ddag.sk_data
        JOIN dim_tempo ddi ON fa.sk_data_inicio = ddi.sk_data
        JOIN dim_tempo ddf ON fa.sk_data_finalizacao = ddf.sk_data
    """

    # Adicionando condições dinamicamente
    conditions = []
    params = []

    if estados:
        conditions.append("dc.UF IN %s")
        params.append(tuple(estados))

    if cidades:
        conditions.append("dc.Cidade IN %s")
        params.append(tuple(cidades))

    if filiais:
        conditions.append("df.Filial IN %s")
        params.append(tuple(filiais))

    # Adicionando a cláusula WHERE se houver condições
    if conditions:
        query_atendimentos += " WHERE " + " AND ".join(conditions)

    # Executando a consulta com os parâmetros
    df_atendimentos = fetch_data(query_atendimentos, params=params)
    
    # Exibir análises adicionais
    if not df_atendimentos.empty:
        
    # Adicionando uma área de expansão para as análises
        # Titulo da sub-pagina
        st.title("Análise de Atendimentos Finalizados")

        with st.expander("Volume de Atendimentos por Ano/Mês", expanded=st.session_state.expander_state):

            # TItulo do gráfico
            st.subheader("Volume de Atendimentos por Ano/Mês")
                
            # Agregar os dados para contar a quantidade de IDs por ano/mês
            volume_ano_mes_altair = df_atendimentos.groupby('nr_ano_nr_mes_finalizacao')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(volume_ano_mes_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('nr_ano_nr_mes_finalizacao:O', axis=alt.Axis(labelAngle=0, title='Ano/Mês'), title='Ano/Mês')  # Aqui desativamos o título do eixo x
            ).properties(
                width=1400,
                height=400
            )
            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        # Adicionando uma área de expansão
        with st.expander("Volume de Atendimentos por Estado", expanded=st.session_state.expander_state):

            # Titulo do gráfico        
            st.subheader("Volume de Atendimentos por Estado")
            # Agregar os dados para contar a quantidade de IDs por ano/mês
            volume_estado_altair = df_atendimentos.groupby('uf')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(volume_estado_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('uf:O', axis=alt.Axis(labelAngle=0, title='Estado'), title='Estado')  # Aqui desativamos o título do eixo x
            ).properties(
                width=1400,
                height=400
            )
            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        # Adicionando uma área de expansão
        with st.expander("Volume de Atendimentos por Cidade", expanded=st.session_state.expander_state):

            # Titulo do gráfico        
            st.subheader("Volume de Atendimentos por Cidade")

            # Agregar os dados para contar a quantidade de IDs por ano/mês
            volume_estado_altair = df_atendimentos.groupby('cidade')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(volume_estado_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('cidade:O', axis=alt.Axis(labelAngle=0, title='Cidade'), title='Cidade')  # Aqui desativamos o título do eixo x
            ).properties(
                width=1400,
                height=400
            )
            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        # Adicionando uma área de expansão
        with st.expander("Volume de Atendimentos por Filial", expanded=st.session_state.expander_state):

            # Titulo do gráfico        
            st.subheader("Volume de Atendimentos por Filial")

            # Agregar os dados para contar a quantidade de IDs por ano/mês
            volume_estado_altair = df_atendimentos.groupby('filial')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(volume_estado_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('filial:O', axis=alt.Axis(labelAngle=0, title='Filial'), title='Filial')  # Aqui desativamos o título do eixo x
            ).properties(
                width=1400,
                height=400
            )
            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        with st.expander("Volume de Atendimentos por Setor", expanded=st.session_state.expander_state):
            # Titulo do gráfico        
            st.subheader("Volume de Atendimentos por Setor")

            # Agregar os dados para contar a quantidade de IDs por ano/mês
            volume_estado_altair = df_atendimentos.groupby('setor')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(volume_estado_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('setor:O', axis=alt.Axis(title='Setor', labelAngle=0, labelFontSize=10), title='Setor')  # Adicionei um título para o eixo x e ajustei o ângulo e o tamanho da fonte dos rótulos
            ).properties(
                width=1400,  # Reduzi a largura do gráfico
                height=400
            )

            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        with st.expander("Volume de Atendimentos por Colaborador", expanded=st.session_state.expander_state):
            # Titulo do gráfico        
            st.subheader("Volume de Atendimentos por Colaborador")
            
            # Extrair o primeiro nome de cada colaborador
            df_atendimentos['primeiro_nome'] = df_atendimentos['colaborador'].apply(lambda x: x.split()[0])

            # Agregar os dados para contar a quantidade de IDs por ano/mês
            volume_estado_altair = df_atendimentos.groupby('primeiro_nome')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(volume_estado_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('primeiro_nome:O', axis=alt.Axis(title='Colaborador', labelAngle=0, labelFontSize=10), title='Colaborador')  # Adicionei um título para o eixo x e ajustei o ângulo e o tamanho da fonte dos rótulos
            ).properties(
                width=1400,  # Reduzi a largura do gráfico
                height=400
            )

            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        with st.expander("Volume de Atendimentos por Assunto", expanded=st.session_state.expander_state):
            # Titulo do gráfico        
            st.subheader("Volume de Atendimentos por Assunto")

            # Agregar os dados para contar a quantidade de IDs por ano/mês
            volume_estado_altair = df_atendimentos.groupby('assunto')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(volume_estado_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('assunto:O', axis=alt.Axis(title='Assunto', labelAngle=0, labelFontSize=10), title='Assunto')  # Adicionei um título para o eixo x e ajustei o ângulo e o tamanho da fonte dos rótulos
            ).properties(
                width=1400,  # Reduzi a largura do gráfico
                height=400
            )

            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        with st.expander("Volume de Atendimentos por Tipo Atendimento", expanded=st.session_state.expander_state):
            # Titulo do gráfico        
            st.subheader("Volume de Atendimentos por Tipo Atendimento")

            # Agregar os dados para contar a quantidade de IDs por ano/mês
            volume_estado_altair = df_atendimentos.groupby('tipo_atendimento')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(volume_estado_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('tipo_atendimento:O', axis=alt.Axis(title='Tipo Atendimento', labelAngle=0, labelFontSize=10), title='Tipo Atendimento')  # Adicionei um título para o eixo x e ajustei o ângulo e o tamanho da fonte dos rótulos
            ).properties(
                width=1400,  # Reduzi a largura do gráfico
                height=400
            )

            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        with st.expander("Volume de Atendimentos por Prioridade", expanded=st.session_state.expander_state):
            # Titulo do gráfico        
            st.subheader("Volume de Atendimentos por Prioridade")

            # Agregar os dados para contar a quantidade de IDs por ano/mês
            volume_estado_altair = df_atendimentos.groupby('prioridade')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(volume_estado_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('prioridade:O', axis=alt.Axis(title='Prioridade', labelAngle=0, labelFontSize=10), title='Prioridade')  # Adicionei um título para o eixo x e ajustei o ângulo e o tamanho da fonte dos rótulos
            ).properties(
                width=1400,  # Reduzi a largura do gráfico
                height=400
            )

            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)


            # Altera o estado do expander ao final da seção
            st.session_state.expander_state = st.session_state.expander_state

########################################################################################################################
        # Titulo da sub-pagina
        st.title("Análise de SLA")

        with st.expander("SLA de Atendimentos por Ano/Mês", expanded=st.session_state.expander_state):

            # TItulo do gráfico
            st.subheader("SLA de Atendimentos por Ano/Mês")
                
            # Agregar os dados para contar a quantidade de IDs por ano/mês
            sla_ano_mes_altair = df_atendimentos.groupby('nr_ano_nr_mes_finalizacao')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(sla_ano_mes_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('nr_ano_nr_mes_finalizacao:O', axis=alt.Axis(labelAngle=0, title='Ano/Mês'), title='Ano/Mês')  # Aqui desativamos o título do eixo x
            ).properties(
                width=1400,
                height=400
            )
            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        # Adicionando uma área de expansão
        with st.expander("SLA de Atendimentos por Estado", expanded=st.session_state.expander_state):

            # Titulo do gráfico        
            st.subheader("SLA de Atendimentos por Estado")
            # Agregar os dados para contar a quantidade de IDs por ano/mês
            sla_estado_altair = df_atendimentos.groupby('uf')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(sla_estado_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('uf:O', axis=alt.Axis(labelAngle=0, title='Estado'), title='Estado')  # Aqui desativamos o título do eixo x
            ).properties(
                width=1400,
                height=400
            )
            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        # Adicionando uma área de expansão
        with st.expander("SLA de Atendimentos por Cidade", expanded=st.session_state.expander_state):

            # Titulo do gráfico        
            st.subheader("SLA de Atendimentos por Cidade")

            # Agregar os dados para contar a quantidade de IDs por ano/mês
            sla_estado_altair = df_atendimentos.groupby('cidade')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(sla_estado_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('cidade:O', axis=alt.Axis(labelAngle=0, title='Cidade'), title='Cidade')  # Aqui desativamos o título do eixo x
            ).properties(
                width=1400,
                height=400
            )
            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        # Adicionando uma área de expansão
        with st.expander("SLA de Atendimentos por Filial", expanded=st.session_state.expander_state):

            # Titulo do gráfico        
            st.subheader("SLA de Atendimentos por Filial")

            # Agregar os dados para contar a quantidade de IDs por ano/mês
            sla_estado_altair = df_atendimentos.groupby('filial')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(sla_estado_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('filial:O', axis=alt.Axis(labelAngle=0, title='Filial'), title='Filial')  # Aqui desativamos o título do eixo x
            ).properties(
                width=1400,
                height=400
            )
            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        with st.expander("SLA de Atendimentos por Setor", expanded=st.session_state.expander_state):
            # Titulo do gráfico        
            st.subheader("SLA de Atendimentos por Setor")

            # Agregar os dados para contar a quantidade de IDs por ano/mês
            sla_estado_altair = df_atendimentos.groupby('setor')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(sla_estado_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('setor:O', axis=alt.Axis(title='Setor', labelAngle=0, labelFontSize=10), title='Setor')  # Adicionei um título para o eixo x e ajustei o ângulo e o tamanho da fonte dos rótulos
            ).properties(
                width=1400,  # Reduzi a largura do gráfico
                height=400
            )

            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        with st.expander("SLA de Atendimentos por Colaborador", expanded=st.session_state.expander_state):
            # Titulo do gráfico        
            st.subheader("SLA de Atendimentos por Colaborador")
            
            # Extrair o primeiro nome de cada colaborador
            df_atendimentos['primeiro_nome'] = df_atendimentos['colaborador'].apply(lambda x: x.split()[0])

            # Agregar os dados para contar a quantidade de IDs por ano/mês
            sla_estado_altair = df_atendimentos.groupby('primeiro_nome')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(sla_estado_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('primeiro_nome:O', axis=alt.Axis(title='Colaborador', labelAngle=0, labelFontSize=10), title='Colaborador')  # Adicionei um título para o eixo x e ajustei o ângulo e o tamanho da fonte dos rótulos
            ).properties(
                width=1400,  # Reduzi a largura do gráfico
                height=400
            )

            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        with st.expander("SLA de Atendimentos por Assunto", expanded=st.session_state.expander_state):
            # Titulo do gráfico        
            st.subheader("SLA de Atendimentos por Assunto")

            # Agregar os dados para contar a quantidade de IDs por ano/mês
            sla_estado_altair = df_atendimentos.groupby('assunto')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(sla_estado_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('assunto:O', axis=alt.Axis(title='Assunto', labelAngle=0, labelFontSize=10), title='Assunto')  # Adicionei um título para o eixo x e ajustei o ângulo e o tamanho da fonte dos rótulos
            ).properties(
                width=1400,  # Reduzi a largura do gráfico
                height=400
            )

            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        with st.expander("SLA de Atendimentos por Tipo Atendimento", expanded=st.session_state.expander_state):
            # Titulo do gráfico        
            st.subheader("SLA de Atendimentos por Tipo Atendimento")

            # Agregar os dados para contar a quantidade de IDs por ano/mês
            sla_estado_altair = df_atendimentos.groupby('tipo_atendimento')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(sla_estado_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('tipo_atendimento:O', axis=alt.Axis(title='Tipo Atendimento', labelAngle=0, labelFontSize=10), title='Tipo Atendimento')  # Adicionei um título para o eixo x e ajustei o ângulo e o tamanho da fonte dos rótulos
            ).properties(
                width=1400,  # Reduzi a largura do gráfico
                height=400
            )

            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        with st.expander("SLA de Atendimentos por Prioridade", expanded=st.session_state.expander_state):
            # Titulo do gráfico        
            st.subheader("SLA de Atendimentos por Prioridade")

            # Agregar os dados para contar a quantidade de IDs por ano/mês
            sla_estado_altair = df_atendimentos.groupby('prioridade')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(sla_estado_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('prioridade:O', axis=alt.Axis(title='Prioridade', labelAngle=0, labelFontSize=10), title='Prioridade')  # Adicionei um título para o eixo x e ajustei o ângulo e o tamanho da fonte dos rótulos
            ).properties(
                width=1400,  # Reduzi a largura do gráfico
                height=400
            )

            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)


            # Altera o estado do expander ao final da seção
            st.session_state.expander_state = st.session_state.expander_state



########################################################################################################################3
        # Titulo da sub-pagina
        st.title("Análise de Tempo Médio")

        with st.expander("Tempo Médio de Atendimento por Ano/Mês", expanded=st.session_state.expander_state):

            # TItulo do gráfico
            st.subheader("Tempo Médio de Atendimento por Ano/Mês")
                
            # Agregar os dados para contar a quantidade de IDs por ano/mês
            tempo_medio_ano_mes_altair = df_atendimentos.groupby('nr_ano_nr_mes_finalizacao')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(tempo_medio_ano_mes_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('nr_ano_nr_mes_finalizacao:O', axis=alt.Axis(labelAngle=0, title='Ano/Mês'), title='Ano/Mês')  # Aqui desativamos o título do eixo x
            ).properties(
                width=1400,
                height=400
            )
            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        # Adicionando uma área de expansão
        with st.expander("Tempo Médio de Atendimento por Estado", expanded=st.session_state.expander_state):

            # Titulo do gráfico        
            st.subheader("Tempo Médio de Atendimento por Estado")
            # Agregar os dados para contar a quantidade de IDs por ano/mês
            tempo_medio_ano_mes_altair = df_atendimentos.groupby('uf')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(tempo_medio_ano_mes_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('uf:O', axis=alt.Axis(labelAngle=0, title='Estado'), title='Estado')  # Aqui desativamos o título do eixo x
            ).properties(
                width=1400,
                height=400
            )
            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        # Adicionando uma área de expansão
        with st.expander("Tempo Médio de Atendimento por Cidade", expanded=st.session_state.expander_state):

            # Titulo do gráfico        
            st.subheader("Tempo Médio de Atendimento por Cidade")

            # Agregar os dados para contar a quantidade de IDs por ano/mês
            tempo_medio_ano_mes_altair = df_atendimentos.groupby('cidade')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(tempo_medio_ano_mes_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('cidade:O', axis=alt.Axis(labelAngle=0, title='Cidade'), title='Cidade')  # Aqui desativamos o título do eixo x
            ).properties(
                width=1400,
                height=400
            )
            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        # Adicionando uma área de expansão
        with st.expander("Tempo Médio de Atendimento por Filial", expanded=st.session_state.expander_state):

            # Titulo do gráfico        
            st.subheader("Tempo Médio de Atendimento por Filial")

            # Agregar os dados para contar a quantidade de IDs por ano/mês
            tempo_medio_ano_mes_altair = df_atendimentos.groupby('filial')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(tempo_medio_ano_mes_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('filial:O', axis=alt.Axis(labelAngle=0, title='Filial'), title='Filial')  # Aqui desativamos o título do eixo x
            ).properties(
                width=1400,
                height=400
            )
            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        with st.expander("Tempo Médio de Atendimento por Setor", expanded=st.session_state.expander_state):
            # Titulo do gráfico        
            st.subheader("Tempo Médio de Atendimento por Setor")

            # Agregar os dados para contar a quantidade de IDs por ano/mês
            tempo_medio_ano_mes_altair = df_atendimentos.groupby('setor')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(tempo_medio_ano_mes_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('setor:O', axis=alt.Axis(title='Setor', labelAngle=0, labelFontSize=10), title='Setor')  # Adicionei um título para o eixo x e ajustei o ângulo e o tamanho da fonte dos rótulos
            ).properties(
                width=1400,  # Reduzi a largura do gráfico
                height=400
            )

            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        with st.expander("Tempo Médio de Atendimento por Colaborador", expanded=st.session_state.expander_state):
            # Titulo do gráfico        
            st.subheader("Tempo Médio de Atendimento por Colaborador")
            
            # Extrair o primeiro nome de cada colaborador
            df_atendimentos['primeiro_nome'] = df_atendimentos['colaborador'].apply(lambda x: x.split()[0])

            # Agregar os dados para contar a quantidade de IDs por ano/mês
            tempo_medio_ano_mes_altair = df_atendimentos.groupby('primeiro_nome')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(tempo_medio_ano_mes_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('primeiro_nome:O', axis=alt.Axis(title='Colaborador', labelAngle=0, labelFontSize=10), title='Colaborador')  # Adicionei um título para o eixo x e ajustei o ângulo e o tamanho da fonte dos rótulos
            ).properties(
                width=1400,  # Reduzi a largura do gráfico
                height=400
            )

            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        with st.expander("Tempo Médio de Atendimento por Assunto", expanded=st.session_state.expander_state):
            # Titulo do gráfico        
            st.subheader("Tempo Médio de Atendimento por Assunto")

            # Agregar os dados para contar a quantidade de IDs por ano/mês
            tempo_medio_ano_mes_altair = df_atendimentos.groupby('assunto')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(tempo_medio_ano_mes_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('assunto:O', axis=alt.Axis(title='Assunto', labelAngle=0, labelFontSize=10), title='Assunto')  # Adicionei um título para o eixo x e ajustei o ângulo e o tamanho da fonte dos rótulos
            ).properties(
                width=1400,  # Reduzi a largura do gráfico
                height=400
            )

            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        with st.expander("Tempo Médio de Atendimento por Tipo Atendimento", expanded=st.session_state.expander_state):
            # Titulo do gráfico        
            st.subheader("Tempo Médio de Atendimento por Tipo Atendimento")

            # Agregar os dados para contar a quantidade de IDs por ano/mês
            tempo_medio_ano_mes_altair = df_atendimentos.groupby('tipo_atendimento')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(tempo_medio_ano_mes_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('tipo_atendimento:O', axis=alt.Axis(title='Tipo Atendimento', labelAngle=0, labelFontSize=10), title='Tipo Atendimento')  # Adicionei um título para o eixo x e ajustei o ângulo e o tamanho da fonte dos rótulos
            ).properties(
                width=1400,  # Reduzi a largura do gráfico
                height=400
            )

            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)

        with st.expander("Tempo Médio de Atendimento por Prioridade", expanded=st.session_state.expander_state):
            # Titulo do gráfico        
            st.subheader("Tempo Médio de Atendimento por Prioridade")

            # Agregar os dados para contar a quantidade de IDs por ano/mês
            tempo_medio_ano_mes_altair = df_atendimentos.groupby('prioridade')['id'].nunique().reset_index(name='Contagem')

            # Criar o gráfico usando Altair com barras horizontais
            chart = alt.Chart(tempo_medio_ano_mes_altair).mark_bar().encode(
                y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)),  # Aqui desativamos o título do eixo y
                x=alt.X('prioridade:O', axis=alt.Axis(title='Prioridade', labelAngle=0, labelFontSize=10), title='Prioridade')  # Adicionei um título para o eixo x e ajustei o ângulo e o tamanho da fonte dos rótulos
            ).properties(
                width=1400,  # Reduzi a largura do gráfico
                height=400
            )

            # Adiciona rótulos de valores no topo das barras com cor branca
            text = chart.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Deslocamento vertical
                color='white'  # Cor branca para o texto
            ).encode(
                text='Contagem:Q'
            )

            st.altair_chart(chart + text)


            # Altera o estado do expander ao final da seção
            st.session_state.expander_state = st.session_state.expander_state

if __name__ == "__main__":
    main()
