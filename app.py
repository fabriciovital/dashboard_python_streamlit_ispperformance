import streamlit as st
import pandas as pd
import psycopg2
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

# Função de login
def login(username, password):
    # Verifique as credenciais aqui no banco de dados
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT tipo_usuario, filial_usuario, senha_usuario FROM dim_usuario WHERE nome_usuario = %s;", (username,))
    result = cur.fetchone()
    conn.close()

    if result is not None:  # Verifica se o resultado não é None
        tipo_usuario, filial_usuario, senha_bd = result
        if password == senha_bd:  # Verifica se a senha fornecida corresponde à senha armazenada
            if tipo_usuario == "FILIAL":
                return tipo_usuario, filial_usuario
            else:
                return tipo_usuario, None  # Retorna None como filial para usuários do tipo ADMINISTRADOR

    # Se as credenciais não forem válidas, exibir mensagem de erro e impedir o acesso
    st.error("Credenciais inválidas. Por favor, tente novamente.")
    return None, None

# Define a configuração da página no Streamlit
st.set_page_config(page_title="ISP Performance - Decisões inteligentes, baseadas em dados confiáveis para o sucesso do seu provedor!", page_icon="📊", layout="wide")

# Load Style CSS
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Função principal do Streamlit
def main():
    # Verificar o login apenas se o usuário não estiver logado
    if "user_type" not in st.session_state:
        login_section()

    if "user_type" in st.session_state:
        app_interface()

# Função para exibir a seção de login
def login_section():
    st.markdown("""
            <style>
                .animation-container {
                    text-align: center;
                    margin-bottom: 20px;
                }

                .program-name {
                    font-size: 50px;
                    color: white; /* Cor do texto branca */
                    background: linear-gradient(to right, #007bff, #1e90ff); /* Degrade azul no fundo do título */
                    padding: 10px 20px;
                    border-radius: 10px;
                    display: inline-block;
                }

                .animation {
                    background: linear-gradient(to right, #ff9966, #ff5e62);
                    padding: 20px;
                    border-radius: 10px;
                    animation: fadeIn 5s ease-in-out forwards;
                    opacity: 0;
                }

                .animation p {
                    opacity: 0;
                    animation: fadeInText 2s ease-in-out forwards;
                    font-size: 30px; /* Alteração do tamanho da fonte das frases */
                    margin-bottom: 15px; /* Espaçamento entre as frases */
                    color: white; /* Mantida a cor original das frases */
                }

                .animation p:nth-child(1) {
                    animation-delay: 0.5s;
                }

                .animation p:nth-child(2) {
                    animation-delay: 3s;
                }

                .animation p:nth-child(3) {
                    animation-delay: 5.5s;
                }

                .animation p:nth-child(4) {
                    animation-delay: 8s;
                }

                .animation p:nth-child(5) {
                    animation-delay: 10.5s;
                }

                .animation p:nth-child(6) {
                    animation-delay: 13s;
                }

                @keyframes fadeIn {
                    0% { opacity: 0; }
                    100% { opacity: 1; }
                }

                @keyframes fadeInText {
                    0% { opacity: 0; }
                    100% { opacity: 1; }
                }
            </style>
            <div class='animation-container'>
                <div class='program-name'>ISP Performance</div>
                <div class='animation'>
                    <p>Decisões inteligentes, baseadas em dados confiáveis para o sucesso do seu provedor!</p>
                    <p>1º - Transforme seus dados em vantagem competitiva.</p>
                    <p>2º - Desbloqueie o potencial oculto dos seus dados.</p>
                    <p>3º - Inove com confiança, baseado em dados sólidos.</p>
                    <p>4º - Construa o futuro do seu negócio com inteligência.</p>                  
                </div>
            </div>
        """, unsafe_allow_html=True)
    username = st.sidebar.text_input("Usuário")
    password = st.sidebar.text_input("Senha", type="password")
    login_button = st.sidebar.button("Login", key="login_button")

    if login_button:
        user_type, user_filial = login(username, password)
        if user_type:
            st.session_state.user_type = user_type
            st.session_state.user_filial = user_filial
            st.session_state.username = username  # Armazenar o nome de usuário na sessão
            st.session_state.password = password  # Armazenar a senha na sessão
            st.experimental_rerun()  # Recarregar a página após login bem-sucedido

# Função para exibir a interface da aplicação
def app_interface():
    user_type = st.session_state.user_type
    username = st.session_state.username
    password = st.session_state.password  # Recuperar a senha da sessão
    user_filial = st.session_state.user_filial

    # Lidar com o caso em que o usuário é do tipo ADMINISTRADOR
    if user_type == "ADMINISTRADOR":
        st.session_state.user_filial = None  # Definir user_filial como None para usuários do tipo ADMINISTRADOR
        
    # Adicionar nome de usuário à barra lateral
    st.sidebar.write(f"Bem-vindo, {username}!")

    # Adicionar botão de sair à barra lateral
    if st.sidebar.button("Sair"):
        st.session_state.clear()  # Limpar os dados da sessão
        st.experimental_rerun()  # Recarregar a página após sair

    st.header("ANALISE DE PERFORMANCE | INDICADORES & PROGRESSÃO ")
    
    # Botão Expandir/Recolher
    expandir_recolher = st.button("Expandir/Recolher")

    # Verificar e inicializar expander_state
    if "expander_state" not in st.session_state:
        st.session_state.expander_state = False

    expander_state = st.session_state.expander_state

    # Verifica se o botão foi pressionado
    if expandir_recolher:
        # Alterna o estado do expander
        st.session_state.expander_state = not expander_state

    if user_type != "FILIAL":
        # Consulta para buscar estados da tabela dim_cidade
        query_estados = "SELECT DISTINCT UF FROM dim_cidade ORDER BY UF"
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

        # Converte os filtros selecionados para tipos nativos do Python
        estados = [str(estado) for estado in estados]
        cidades = [str(cidade) for cidade in cidades]
        filiais = [str(filial) for filial in filiais]
    else:
        # Lógica de filtro para usuários do tipo FILIAL
        estados = []
        cidades = []
        filiais = [str(user_filial)]

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

    if user_type == "FILIAL":
            conditions.append("df.Filial = %s")
            params.append(user_filial)
    elif filiais:
            conditions.append("df.Filial IN %s")
            params.append(tuple(filiais))
        # Adicionando a cláusula WHERE se houver condições
    
    if conditions:
        query_atendimentos += " WHERE " + " AND ".join(conditions)

    # Executando a consulta com os parâmetros
    df_atendimentos = fetch_data(query_atendimentos, params=params)
    
    # Exibir análises adicionais
    if not df_atendimentos.empty:

        # Titulo da sub-pagina
        st.title("Análise de Atendimentos Finalizados")

    # Volume de Atendimentos por Ano/Mês
    with st.expander("Volume de Atendimentos por Ano/Mês", expanded=expander_state):

        # Título do gráfico
        st.subheader("Volume de Atendimentos por Ano/Mês")
            
        # Agregar os dados para contar a quantidade de IDs por ano/mês
        volume_ano_mes_altair = df_atendimentos.groupby('nr_ano_nr_mes_finalizacao')['id'].nunique().reset_index(name='Contagem')

        # Criar o gráfico usando Altair com barras horizontais
        chart = alt.Chart(volume_ano_mes_altair).mark_bar().encode(
            y=alt.Y('Contagem:Q', axis=alt.Axis(title="Volume de Atendimentos por Ano/Mês")),  # Aqui desativamos o título do eixo y
            x=alt.X('nr_ano_nr_mes_finalizacao:O', axis=alt.Axis(labelAngle=0, title='Ano/Mês'), title='Ano/Mês')  # Aqui desativamos o título do eixo x
        ).properties(
            width='container',
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

        st.altair_chart(chart + text, use_container_width=True)

    # Volume de Atendimentos por Estado
    with st.expander("Volume de Atendimentos por Estado", expanded=expander_state):

        # Titulo do gráfico
        st.subheader("Volume de Atendimentos por Estado")

        # Agregar os dados para contar a quantidade de IDs por estado
        volume_estado_altair = df_atendimentos.groupby('uf')['id'].nunique().reset_index(name='Contagem')

        # Criar o gráfico usando Altair com barras horizontais
        chart = alt.Chart(volume_estado_altair).mark_bar().encode(
            y=alt.Y('Contagem:Q', axis=alt.Axis(title="Volume de Atendimentos por Estado")),  # Desativar o título do eixo y
            x=alt.X('uf:O', axis=alt.Axis(labelAngle=0, title='Estado'), title='Estado')  # Desativar o título do eixo x
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )
        # Adicionar rótulos de valores no topo das barras com cor branca
        text = chart.mark_text(
            align='center',
            baseline='middle',
            dy=-10,  # Deslocamento vertical
            color='white'  # Cor branca para o texto
        ).encode(
            text='Contagem:Q'
        )

        st.altair_chart(chart + text, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

    # Volume de Atendimentos por Cidade
    with st.expander("Volume de Atendimentos por Cidade", expanded=expander_state):

        # Titulo do gráfico
        st.subheader("Volume de Atendimentos por Cidade")

        # Agregar os dados para contar a quantidade de IDs por cidade
        volume_estado_altair = df_atendimentos.groupby('cidade')['id'].nunique().reset_index(name='Contagem')

        # Criar o gráfico usando Altair com barras horizontais
        chart = alt.Chart(volume_estado_altair).mark_bar().encode(
            y=alt.Y('Contagem:Q', axis=alt.Axis(title="Volume de Atendimentos por Cidade")),  # Desativar o título do eixo y
            x=alt.X('cidade:O', axis=alt.Axis(labelAngle=0, title='Cidade'), title='Cidade')  # Desativar o título do eixo x
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )
        # Adicionar rótulos de valores no topo das barras com cor branca
        text = chart.mark_text(
            align='center',
            baseline='middle',
            dy=-10,  # Deslocamento vertical
            color='white'  # Cor branca para o texto
        ).encode(
            text='Contagem:Q'
        )

        st.altair_chart(chart + text, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

    # Volume de Atendimentos por Filial
    with st.expander("Volume de Atendimentos por Filial", expanded=expander_state):

        # Titulo do gráfico
        st.subheader("Volume de Atendimentos por Filial")

        # Agregar os dados para contar a quantidade de IDs por filial
        volume_estado_altair = df_atendimentos.groupby('filial')['id'].nunique().reset_index(name='Contagem')

        # Criar o gráfico usando Altair com barras horizontais
        chart = alt.Chart(volume_estado_altair).mark_bar().encode(
            y=alt.Y('Contagem:Q', axis=alt.Axis(title="Volume de Atendimentos por Filial")),  # Desativar o título do eixo y
            x=alt.X('filial:O', axis=alt.Axis(labelAngle=0, title='Filial'), title='Filial')  # Desativar o título do eixo x
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )
        # Adicionar rótulos de valores no topo das barras com cor branca
        text = chart.mark_text(
            align='center',
            baseline='middle',
            dy=-10,  # Deslocamento vertical
            color='white'  # Cor branca para o texto
        ).encode(
            text='Contagem:Q'
        )

        st.altair_chart(chart + text, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

    # Volume de Atendimentos por Setor
    with st.expander("Volume de Atendimentos por Setor", expanded=expander_state):

        # Titulo do gráfico
        st.subheader("Volume de Atendimentos por Setor")

        # Agregar os dados para contar a quantidade de IDs por setor
        volume_estado_altair = df_atendimentos.groupby('setor')['id'].nunique().reset_index(name='Contagem')

        # Criar o gráfico usando Altair com barras horizontais
        chart = alt.Chart(volume_estado_altair).mark_bar().encode(
            y=alt.Y('Contagem:Q', axis=alt.Axis(title="Volume de Atendimentos por Setor")),  # Desativar o título do eixo y
            x=alt.X('setor:O', axis=alt.Axis(title='Setor', labelAngle=0, labelFontSize=10), title='Setor')  # Adicionar um título para o eixo x e ajustar o ângulo e o tamanho da fonte dos rótulos
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )
        # Adicionar rótulos de valores no topo das barras com cor branca
        text = chart.mark_text(
            align='center',
            baseline='middle',
            dy=-10,  # Deslocamento vertical
            color='white'  # Cor branca para o texto
        ).encode(
            text='Contagem:Q'
        )

        st.altair_chart(chart + text, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

    # Volume de Atendimentos por Colaborador
    with st.expander("Volume de Atendimentos por Colaborador", expanded=expander_state):

        # Titulo do gráfico
        st.subheader("Volume de Atendimentos por Colaborador")

        # Extrair o primeiro nome de cada colaborador
        df_atendimentos['primeiro_nome'] = df_atendimentos['colaborador'].apply(lambda x: x.split()[0])

        # Agregar os dados para contar a quantidade de IDs por colaborador
        volume_estado_altair = df_atendimentos.groupby('primeiro_nome')['id'].nunique().reset_index(name='Contagem')

        # Criar o gráfico usando Altair com barras horizontais
        chart = alt.Chart(volume_estado_altair).mark_bar().encode(
            y=alt.Y('Contagem:Q', axis=alt.Axis(title="Volume de Atendimentos por Colaborador")),  # Desativar o título do eixo y
            x=alt.X('primeiro_nome:O', axis=alt.Axis(title='Colaborador', labelAngle=0, labelFontSize=10), title='Colaborador')  # Adicionar um título para o eixo x e ajustar o ângulo e o tamanho da fonte dos rótulos
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )
        # Adicionar rótulos de valores no topo das barras com cor branca
        text = chart.mark_text(
            align='center',
            baseline='middle',
            dy=-10,  # Deslocamento vertical
            color='white'  # Cor branca para o texto
        ).encode(
            text='Contagem:Q'
        )

        st.altair_chart(chart + text, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

    # Volume de Atendimentos por Assunto
    with st.expander("Volume de Atendimentos por Assunto", expanded=expander_state):

        # Titulo do gráfico
        st.subheader("Volume de Atendimentos por Assunto")

        # Agregar os dados para contar a quantidade de IDs por assunto
        volume_estado_altair = df_atendimentos.groupby('assunto')['id'].nunique().reset_index(name='Contagem')

        # Criar o gráfico usando Altair com barras horizontais
        chart = alt.Chart(volume_estado_altair).mark_bar().encode(
            y=alt.Y('Contagem:Q', axis=alt.Axis(title="Volume de Atendimentos por Assunto")),  # Desativar o título do eixo y
            x=alt.X('assunto:O', axis=alt.Axis(title='Assunto', labelAngle=0, labelFontSize=10), title='Assunto')  # Adicionar um título para o eixo x e ajustar o ângulo e o tamanho da fonte dos rótulos
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )
        # Adicionar rótulos de valores no topo das barras com cor branca
        text = chart.mark_text(
            align='center',
            baseline='middle',
            dy=-10,  # Deslocamento vertical
            color='white'  # Cor branca para o texto
        ).encode(
            text='Contagem:Q'
        )

        st.altair_chart(chart + text, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

    # Volume de Atendimentos por Tipo Atendimento
    with st.expander("Volume de Atendimentos por Tipo Atendimento", expanded=expander_state):

        # Titulo do gráfico
        st.subheader("Volume de Atendimentos por Tipo Atendimento")

        # Agregar os dados para contar a quantidade de IDs por tipo de atendimento
        volume_estado_altair = df_atendimentos.groupby('tipo_atendimento')['id'].nunique().reset_index(name='Contagem')

        # Criar o gráfico usando Altair com barras horizontais
        chart = alt.Chart(volume_estado_altair).mark_bar().encode(
            y=alt.Y('Contagem:Q', axis=alt.Axis(title="Volume de Atendimentos por Tipo Atendimento")),  # Desativar o título do eixo y
            x=alt.X('tipo_atendimento:O', axis=alt.Axis(title='Tipo Atendimento', labelAngle=0, labelFontSize=10), title='Tipo Atendimento')  # Adicionar um título para o eixo x e ajustar o ângulo e o tamanho da fonte dos rótulos
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )
        # Adicionar rótulos de valores no topo das barras com cor branca
        text = chart.mark_text(
            align='center',
            baseline='middle',
            dy=-10,  # Deslocamento vertical
            color='white'  # Cor branca para o texto
        ).encode(
            text='Contagem:Q'
        )

        st.altair_chart(chart + text, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

    # Volume de Atendimentos por Prioridade
    with st.expander("Volume de Atendimentos por Prioridade", expanded=expander_state):

        # Titulo do gráfico
        st.subheader("Volume de Atendimentos por Prioridade")

        # Agregar os dados para contar a quantidade de IDs por prioridade
        volume_estado_altair = df_atendimentos.groupby('prioridade')['id'].nunique().reset_index(name='Contagem')

        # Criar o gráfico usando Altair com barras horizontais
        chart = alt.Chart(volume_estado_altair).mark_bar().encode(
            y=alt.Y('Contagem:Q', axis=alt.Axis(title="Volume de Atendimentos por Prioridade")),  # Desativar o título do eixo y
            x=alt.X('prioridade:O', axis=alt.Axis(title='Prioridade', labelAngle=0, labelFontSize=10), title='Prioridade')  # Adicionar um título para o eixo x e ajustar o ângulo e o tamanho da fonte dos rótulos
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )
        # Adicionar rótulos de valores no topo das barras com cor branca
        text = chart.mark_text(
            align='center',
            baseline='middle',
            dy=-10,  # Deslocamento vertical
            color='white'  # Cor branca para o texto
        ).encode(
            text='Contagem:Q'
        )

        st.altair_chart(chart + text, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

        # Altera o estado do expander ao final da seção
        st.session_state.expander_state = st.session_state.expander_state

########################################################################################################################

    # Titulo da sub-pagina
    st.title("Análise de SLA dos Atendimentos")

    with st.expander("SLA de Atendimentos por Ano/Mês", expanded=expander_state):

        # Título do gráfico
        st.subheader("SLA de Atendimentos por Ano/Mês")

        # Calcular a média do percentual de SLA por Ano/Mês (ajustando o valor para percentual)
        sla_ano_mes_altair = df_atendimentos.groupby('nr_ano_nr_mes_finalizacao')['sla'].mean().reset_index(name='Média SLA (%)')
        sla_ano_mes_altair['Média SLA (%)'] = sla_ano_mes_altair['Média SLA (%)'] / 100

        # Criar o gráfico usando Altair com barras horizontais
        chart = alt.Chart(sla_ano_mes_altair).mark_bar().encode(
            y=alt.Y('Média SLA (%):Q', axis=alt.Axis(title="Análise de SLA dos Atendimentos", format='.2%')),  # Porcentagem no eixo y
            x=alt.X('nr_ano_nr_mes_finalizacao:O', axis=alt.Axis(labelAngle=0, title='Ano/Mês'), title='Ano/Mês')  # Título do eixo x
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )

        # Adicionar rótulos de valores no topo das barras com cor branca
        text = chart.mark_text(
            align='center',
            baseline='middle',
            dy=-10,  # Deslocamento vertical
            color='white'  # Cor branca para o texto
        ).encode(
            text=alt.Text('Média SLA (%):Q', format='.2%')
        )

        st.altair_chart(chart + text, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

    with st.expander("SLA de Atendimentos por Estado", expanded=expander_state):

        # Título do gráfico        
        st.subheader("SLA de Atendimentos por Estado")

        # Calcular a média do percentual de SLA por Estado
        sla_estado_altair = df_atendimentos.groupby('uf')['sla'].mean().reset_index(name='Média SLA (%)')
        sla_estado_altair['Média SLA (%)'] = sla_estado_altair['Média SLA (%)'] / 100

        # Criar o gráfico usando Altair com barras horizontais
        chart = alt.Chart(sla_estado_altair).mark_bar().encode(
            y=alt.Y('Média SLA (%):Q', axis=alt.Axis(title="SLA de Atendimentos por Estado", format='.2%')),  # Porcentagem no eixo y
            x=alt.X('uf:O', axis=alt.Axis(labelAngle=0, title='Estado'), title='Estado')  # Título do eixo x
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )

        # Adicionar rótulos de valores no topo das barras com cor branca
        text = chart.mark_text(
            align='center', baseline='middle', dy=-10, color='white'
        ).encode(text=alt.Text('Média SLA (%):Q', format='.2%'))

        st.altair_chart(chart + text, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

    with st.expander("SLA de Atendimentos por Cidade", expanded=expander_state):

        # Título do gráfico        
        st.subheader("SLA de Atendimentos por Cidade")

        # Calcular a média do percentual de SLA por Cidade
        sla_cidade_altair = df_atendimentos.groupby('cidade')['sla'].mean().reset_index(name='Média SLA (%)')
        sla_cidade_altair['Média SLA (%)'] = sla_cidade_altair['Média SLA (%)'] / 100

        # Criar o gráfico usando Altair com barras horizontais
        chart = alt.Chart(sla_cidade_altair).mark_bar().encode(
            y=alt.Y('Média SLA (%):Q', axis=alt.Axis(title="SLA de Atendimentos por Cidade", format='.2%')),  # Porcentagem no eixo y
            x=alt.X('cidade:O', axis=alt.Axis(labelAngle=0, title='Cidade'), title='Cidade')  # Título do eixo x
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )

        # Adicionar rótulos de valores no topo das barras com cor branca
        text = chart.mark_text(
            align='center', baseline='middle', dy=-10, color='white'
        ).encode(text=alt.Text('Média SLA (%):Q', format='.2%'))

        st.altair_chart(chart + text, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

    with st.expander("SLA de Atendimentos por Filial", expanded=expander_state):

        # Título do gráfico        
        st.subheader("SLA de Atendimentos por Filial")

        # Calcular a média do percentual de SLA por Filial
        sla_filial_altair = df_atendimentos.groupby('filial')['sla'].mean().reset_index(name='Média SLA (%)')
        sla_filial_altair['Média SLA (%)'] = sla_filial_altair['Média SLA (%)'] / 100

        # Criar o gráfico usando Altair com barras horizontais
        chart = alt.Chart(sla_filial_altair).mark_bar().encode(
            y=alt.Y('Média SLA (%):Q', axis=alt.Axis(title="SLA de Atendimentos por Filial", format='.2%')),  # Porcentagem no eixo y
            x=alt.X('filial:O', axis=alt.Axis(labelAngle=0, title='Filial'), title='Filial')  # Título do eixo x
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )

        # Adicionar rótulos de valores no topo das barras com cor branca
        text = chart.mark_text(
            align='center', baseline='middle', dy=-10, color='white'
        ).encode(text=alt.Text('Média SLA (%):Q', format='.2%'))

        st.altair_chart(chart + text, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

    with st.expander("SLA de Atendimentos por Setor", expanded=expander_state):

        # Título do gráfico        
        st.subheader("SLA de Atendimentos por Setor")

        # Calcular a média do percentual de SLA por Setor
        sla_setor_altair = df_atendimentos.groupby('setor')['sla'].mean().reset_index(name='Média SLA (%)')
        sla_setor_altair['Média SLA (%)'] = sla_setor_altair['Média SLA (%)'] / 100

        # Criar o gráfico usando Altair com barras horizontais
        chart = alt.Chart(sla_setor_altair).mark_bar().encode(
            y=alt.Y('Média SLA (%):Q', axis=alt.Axis(title="SLA de Atendimentos por Setor", format='.2%')),  # Porcentagem no eixo y
            x=alt.X('setor:O', axis=alt.Axis(labelAngle=0, title='Setor', labelFontSize=10), title='Setor')  # Título do eixo x
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )

        # Adicionar rótulos de valores no topo das barras com cor branca
        text = chart.mark_text(
            align='center', baseline='middle', dy=-10, color='white'
        ).encode(text=alt.Text('Média SLA (%):Q', format='.2%'))

        st.altair_chart(chart + text, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

    with st.expander("SLA de Atendimentos por Colaborador", expanded=expander_state):

        # Título do gráfico        
        st.subheader("SLA de Atendimentos por Colaborador")

        # Extrair o primeiro nome de cada colaborador
        df_atendimentos['primeiro_nome'] = df_atendimentos['colaborador'].apply(lambda x: x.split()[0])

        # Calcular a média do percentual de SLA por Colaborador
        sla_colaborador_altair = df_atendimentos.groupby('primeiro_nome')['sla'].mean().reset_index(name='Média SLA (%)')
        sla_colaborador_altair['Média SLA (%)'] = sla_colaborador_altair['Média SLA (%)'] / 100

        # Criar o gráfico usando Altair com barras horizontais
        chart = alt.Chart(sla_colaborador_altair).mark_bar().encode(
            y=alt.Y('Média SLA (%):Q', axis=alt.Axis(title="SLA de Atendimentos por Colaborador", format='.2%')),  # Porcentagem no eixo y
            x=alt.X('primeiro_nome:O', axis=alt.Axis(labelAngle=0, title='Colaborador', labelFontSize=10), title='Colaborador')  # Título do eixo x
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )

        # Adicionar rótulos de valores no topo das barras com cor branca
        text = chart.mark_text(
            align='center', baseline='middle', dy=-10, color='white'
        ).encode(text=alt.Text('Média SLA (%):Q', format='.2%'))

        st.altair_chart(chart + text, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

    with st.expander("SLA de Atendimentos por Assunto", expanded=expander_state):

        # Título do gráfico        
        st.subheader("SLA de Atendimentos por Assunto")

        # Calcular a média do percentual de SLA por Assunto
        sla_assunto_altair = df_atendimentos.groupby('assunto')['sla'].mean().reset_index(name='Média SLA (%)')
        sla_assunto_altair['Média SLA (%)'] = sla_assunto_altair['Média SLA (%)'] / 100

        # Criar o gráfico usando Altair com barras horizontais
        chart = alt.Chart(sla_assunto_altair).mark_bar().encode(
            y=alt.Y('Média SLA (%):Q', axis=alt.Axis(title="SLA de Atendimentos por Assunto", format='.2%')),  # Porcentagem no eixo y
            x=alt.X('assunto:O', axis=alt.Axis(labelAngle=0, title='Assunto', labelFontSize=10), title='Assunto')  # Título do eixo x
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )

        # Adicionar rótulos de valores no topo das barras com cor branca
        text = chart.mark_text(
            align='center', baseline='middle', dy=-10, color='white'
        ).encode(text=alt.Text('Média SLA (%):Q', format='.2%'))

        st.altair_chart(chart + text, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

    with st.expander("SLA de Atendimentos por Tipo Atendimento", expanded=expander_state):

        # Título do gráfico        
        st.subheader("SLA de Atendimentos por Tipo Atendimento")

        # Calcular a média do percentual de SLA por Tipo Atendimento
        sla_tipo_atendimento_altair = df_atendimentos.groupby('tipo_atendimento')['sla'].mean().reset_index(name='Média SLA (%)')
        sla_tipo_atendimento_altair['Média SLA (%)'] = sla_tipo_atendimento_altair['Média SLA (%)'] / 100

        # Criar o gráfico usando Altair com barras horizontais
        chart = alt.Chart(sla_tipo_atendimento_altair).mark_bar().encode(
            y=alt.Y('Média SLA (%):Q', axis=alt.Axis(title="SLA de Atendimentos por Tipo Atendimento", format='.2%')),  # Porcentagem no eixo y
            x=alt.X('tipo_atendimento:O', axis=alt.Axis(labelAngle=0, title='Tipo Atendimento', labelFontSize=10), title='Tipo Atendimento')  # Título do eixo x
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )

        # Adicionar rótulos de valores no topo das barras com cor branca
        text = chart.mark_text(
            align='center', baseline='middle', dy=-10, color='white'
        ).encode(text=alt.Text('Média SLA (%):Q', format='.2%'))

        st.altair_chart(chart + text, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

    with st.expander("SLA de Atendimentos por Prioridade", expanded=expander_state):

        # Título do gráfico        
        st.subheader("SLA de Atendimentos por Prioridade")

        # Calcular a média do percentual de SLA por Prioridade
        sla_prioridade_altair = df_atendimentos.groupby('prioridade')['sla'].mean().reset_index(name='Média SLA (%)')
        sla_prioridade_altair['Média SLA (%)'] = sla_prioridade_altair['Média SLA (%)'] / 100

        # Criar o gráfico usando Altair com barras horizontais
        chart = alt.Chart(sla_prioridade_altair).mark_bar().encode(
            y=alt.Y('Média SLA (%):Q', axis=alt.Axis(title="SLA de Atendimentos por Prioridade", format='.2%')),  # Porcentagem no eixo y
            x=alt.X('prioridade:O', axis=alt.Axis(labelAngle=0, title='Prioridade', labelFontSize=10), title='Prioridade')  # Título do eixo x
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )

        # Adicionar rótulos de valores no topo das barras com cor branca
        text = chart.mark_text(
            align='center', baseline='middle', dy=-10, color='white'
        ).encode(text=alt.Text('Média SLA (%):Q', format='.2%'))

        st.altair_chart(chart + text, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner


        # Altera o estado do expander ao final da seção
        st.session_state.expander_state = st.session_state.expander_state



########################################################################################################################

# Função para converter segundos em horas, minutos e segundos
        def segundos_para_hms(segundos):
            horas = segundos // 3600
            minutos = (segundos % 3600) // 60
            segundos = segundos % 60
            return f"{int(horas):02d}:{int(minutos):02d}:{int(segundos):02d}"

        # Calcular o tempo de atendimento em cada linha
        df_atendimentos['data_hora_abertura'] = pd.to_datetime(df_atendimentos['data_abertura'].astype(str) + ' ' + df_atendimentos['hora_abertura'].astype(str))
        df_atendimentos['data_hora_finalizacao'] = pd.to_datetime(df_atendimentos['data_finalizacao'].astype(str) + ' ' + df_atendimentos['hora_finalizacao'].astype(str))

        # Calcular a diferença entre as duas colunas em segundos
        df_atendimentos['tempo_atendimento'] = (df_atendimentos['data_hora_finalizacao'] - df_atendimentos['data_hora_abertura']).dt.total_seconds()

        # Converter os segundos em horas, minutos e segundos
        df_atendimentos['tempo_atendimento_hms'] = df_atendimentos['tempo_atendimento'].apply(segundos_para_hms)        

    # Título da sub-página
    st.title("Análise de Tempo Médio dos Atendimentos")

    # Adicionando uma área de expansão para o Tempo Médio de Atendimento por Ano/Mês
    with st.expander("Tempo Médio de Atendimento por Ano/Mês", expanded=expander_state):

        # Agregar os dados para calcular o tempo médio de atendimento por ano/mês
        tempo_medio_ano_mes = df_atendimentos.groupby('nr_ano_nr_mes_finalizacao')['tempo_atendimento'].mean().reset_index()
        tempo_medio_ano_mes['tempo_atendimento_hms'] = tempo_medio_ano_mes['tempo_atendimento'].apply(segundos_para_hms)
        tempo_medio_ano_mes['tempo_atendimento_horas'] = tempo_medio_ano_mes['tempo_atendimento'] / 3600  # Converter segundos para horas para a escala Y

        # Título do gráfico
        st.subheader("Tempo Médio de Atendimento por Ano/Mês")

        # Criar o gráfico usando Altair para mostrar o tempo médio de atendimento por ano/mês
        chart_tempo_medio = alt.Chart(tempo_medio_ano_mes).mark_bar().encode(
            y=alt.Y('tempo_atendimento_horas:Q', axis=alt.Axis(title='Tempo Médio de Atendimento (horas)')),  # Eixo y com tempo médio de atendimento em horas
            x=alt.X('nr_ano_nr_mes_finalizacao:O', axis=alt.Axis(labelAngle=0, title='Ano/Mês'), title='Ano/Mês'),  # Eixo x com Ano/Mês                
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )

        # Adicionar rótulos de valores no topo das barras com cor branca
        text_tempo_medio = chart_tempo_medio.mark_text(
            align='center',
            baseline='middle',
            dy=-10,  # Deslocamento vertical
            color='white'  # Cor branca para o texto
        ).encode(
            text='tempo_atendimento_hms:N'  # Mostrar o tempo médio de atendimento formatado
        )

        st.altair_chart(chart_tempo_medio + text_tempo_medio, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

  # Adicionando uma área de expansão para o Tempo Médio de Atendimento por Estado
    with st.expander("Tempo Médio de Atendimento por Estado", expanded=expander_state):

        # Agregar os dados para calcular o tempo médio de atendimento por Estado
        tempo_medio_ano_mes = df_atendimentos.groupby('uf')['tempo_atendimento'].mean().reset_index()
        tempo_medio_ano_mes['tempo_atendimento_hms'] = tempo_medio_ano_mes['tempo_atendimento'].apply(segundos_para_hms)
        tempo_medio_ano_mes['tempo_atendimento_horas'] = tempo_medio_ano_mes['tempo_atendimento'] / 3600  # Converter segundos para horas para a escala Y

        # Título do gráfico
        st.subheader("Tempo Médio de Atendimento por Estado")

        # Criar o gráfico usando Altair para mostrar o tempo médio de atendimento por Estado
        chart_tempo_medio = alt.Chart(tempo_medio_ano_mes).mark_bar().encode(
            y=alt.Y('tempo_atendimento_horas:Q', axis=alt.Axis(title='Tempo Médio de Atendimento (horas)')),  # Eixo y com tempo médio de atendimento em horas
            x=alt.X('uf:O', axis=alt.Axis(labelAngle=0, title='Estado'), title='Estado'),  # Eixo x com Ano/Mês                
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )

        # Adicionar rótulos de valores no topo das barras com cor branca
        text_tempo_medio = chart_tempo_medio.mark_text(
            align='center',
            baseline='middle',
            dy=-10,  # Deslocamento vertical
            color='white'  # Cor branca para o texto
        ).encode(
            text='tempo_atendimento_hms:N'  # Mostrar o tempo médio de atendimento formatado
        )

        st.altair_chart(chart_tempo_medio + text_tempo_medio, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

    # Adicionando uma área de expansão para o Tempo Médio de Atendimento por Cidade
    with st.expander("Tempo Médio de Atendimento por Cidade", expanded=expander_state):

        # Agregar os dados para calcular o tempo médio de atendimento por Cidade
        tempo_medio_ano_mes = df_atendimentos.groupby('cidade')['tempo_atendimento'].mean().reset_index()
        tempo_medio_ano_mes['tempo_atendimento_hms'] = tempo_medio_ano_mes['tempo_atendimento'].apply(segundos_para_hms)
        tempo_medio_ano_mes['tempo_atendimento_horas'] = tempo_medio_ano_mes['tempo_atendimento'] / 3600  # Converter segundos para horas para a escala Y

        # Título do gráfico
        st.subheader("Tempo Médio de Atendimento por Cidade")

        # Criar o gráfico usando Altair para mostrar o tempo médio de atendimento por Cidade
        chart_tempo_medio = alt.Chart(tempo_medio_ano_mes).mark_bar().encode(
            y=alt.Y('tempo_atendimento_horas:Q', axis=alt.Axis(title='Tempo Médio de Atendimento (horas)')),  # Eixo y com tempo médio de atendimento em horas
            x=alt.X('cidade:O', axis=alt.Axis(labelAngle=0, title='Cidade'), title='Cidade'),  # Eixo x com Ano/Mês                
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )

        # Adicionar rótulos de valores no topo das barras com cor branca
        text_tempo_medio = chart_tempo_medio.mark_text(
            align='center',
            baseline='middle',
            dy=-10,  # Deslocamento vertical
            color='white'  # Cor branca para o texto
        ).encode(
            text='tempo_atendimento_hms:N'  # Mostrar o tempo médio de atendimento formatado
        )

        st.altair_chart(chart_tempo_medio + text_tempo_medio, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

    # Adicionando uma área de expansão para o Tempo Médio de Atendimento por Filial
    with st.expander("Tempo Médio de Atendimento por Filial", expanded=expander_state):

        # Agregar os dados para calcular o tempo médio de atendimento por Filial
        tempo_medio_ano_mes = df_atendimentos.groupby('filial')['tempo_atendimento'].mean().reset_index()
        tempo_medio_ano_mes['tempo_atendimento_hms'] = tempo_medio_ano_mes['tempo_atendimento'].apply(segundos_para_hms)
        tempo_medio_ano_mes['tempo_atendimento_horas'] = tempo_medio_ano_mes['tempo_atendimento'] / 3600  # Converter segundos para horas para a escala Y

        # Título do gráfico
        st.subheader("Tempo Médio de Atendimento por Filial")

        # Criar o gráfico usando Altair para mostrar o tempo médio de atendimento por Filial
        chart_tempo_medio = alt.Chart(tempo_medio_ano_mes).mark_bar().encode(
            y=alt.Y('tempo_atendimento_horas:Q', axis=alt.Axis(title='Tempo Médio de Atendimento (horas)')),  # Eixo y com tempo médio de atendimento em horas
            x=alt.X('filial:O', axis=alt.Axis(labelAngle=0, title='Filial'), title='Filial'),  # Eixo x com Ano/Mês                
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )

        # Adicionar rótulos de valores no topo das barras com cor branca
        text_tempo_medio = chart_tempo_medio.mark_text(
            align='center',
            baseline='middle',
            dy=-10,  # Deslocamento vertical
            color='white'  # Cor branca para o texto
        ).encode(
            text='tempo_atendimento_hms:N'  # Mostrar o tempo médio de atendimento formatado
        )

        st.altair_chart(chart_tempo_medio + text_tempo_medio, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

    # Adicionando uma área de expansão para o Tempo Médio de Atendimento por Setor
    with st.expander("Tempo Médio de Atendimento por Setor", expanded=expander_state):

        # Agregar os dados para calcular o tempo médio de atendimento por Setor
        tempo_medio_ano_mes = df_atendimentos.groupby('setor')['tempo_atendimento'].mean().reset_index()
        tempo_medio_ano_mes['tempo_atendimento_hms'] = tempo_medio_ano_mes['tempo_atendimento'].apply(segundos_para_hms)
        tempo_medio_ano_mes['tempo_atendimento_horas'] = tempo_medio_ano_mes['tempo_atendimento'] / 3600  # Converter segundos para horas para a escala Y

        # Título do gráfico
        st.subheader("Tempo Médio de Atendimento por Setor")

        # Criar o gráfico usando Altair para mostrar o tempo médio de atendimento por Setor
        chart_tempo_medio = alt.Chart(tempo_medio_ano_mes).mark_bar().encode(
            y=alt.Y('tempo_atendimento_horas:Q', axis=alt.Axis(title='Tempo Médio de Atendimento (horas)')),  # Eixo y com tempo médio de atendimento em horas
            x=alt.X('setor:O', axis=alt.Axis(labelAngle=0, title='Setor'), title='Setor'),  # Eixo x com Ano/Mês                
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )

        # Adicionar rótulos de valores no topo das barras com cor branca
        text_tempo_medio = chart_tempo_medio.mark_text(
            align='center',
            baseline='middle',
            dy=-10,  # Deslocamento vertical
            color='white'  # Cor branca para o texto
        ).encode(
            text='tempo_atendimento_hms:N'  # Mostrar o tempo médio de atendimento formatado
        )

        st.altair_chart(chart_tempo_medio + text_tempo_medio, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

    # Adicionando uma área de expansão para o Tempo Médio de Atendimento por Colaborador
    with st.expander("Tempo Médio de Atendimento por Colaborador", expanded=expander_state):

        # Agregar os dados para calcular o tempo médio de atendimento por Colaborador
        tempo_medio_ano_mes = df_atendimentos.groupby('colaborador')['tempo_atendimento'].mean().reset_index()
        tempo_medio_ano_mes['tempo_atendimento_hms'] = tempo_medio_ano_mes['tempo_atendimento'].apply(segundos_para_hms)
        tempo_medio_ano_mes['tempo_atendimento_horas'] = tempo_medio_ano_mes['tempo_atendimento'] / 3600  # Converter segundos para horas para a escala Y

        # Título do gráfico
        st.subheader("Tempo Médio de Atendimento por Colaborador")

        # Criar o gráfico usando Altair para mostrar o tempo médio de atendimento por Colaborador
        chart_tempo_medio = alt.Chart(tempo_medio_ano_mes).mark_bar().encode(
            y=alt.Y('tempo_atendimento_horas:Q', axis=alt.Axis(title='Tempo Médio de Atendimento (horas)')),  # Eixo y com tempo médio de atendimento em horas
            x=alt.X('colaborador:O', axis=alt.Axis(labelAngle=0, title='Colaborador'), title='Colaborador'),  # Eixo x com Ano/Mês                
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )

        # Adicionar rótulos de valores no topo das barras com cor branca
        text_tempo_medio = chart_tempo_medio.mark_text(
            align='center',
            baseline='middle',
            dy=-10,  # Deslocamento vertical
            color='white'  # Cor branca para o texto
        ).encode(
            text='tempo_atendimento_hms:N'  # Mostrar o tempo médio de atendimento formatado
        )

        st.altair_chart(chart_tempo_medio + text_tempo_medio, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

    # Adicionando uma área de expansão para o Tempo Médio de Atendimento por Assunto
    with st.expander("Tempo Médio de Atendimento por Assunto", expanded=expander_state):

        # Agregar os dados para calcular o tempo médio de atendimento por Assunto
        tempo_medio_ano_mes = df_atendimentos.groupby('assunto')['tempo_atendimento'].mean().reset_index()
        tempo_medio_ano_mes['tempo_atendimento_hms'] = tempo_medio_ano_mes['tempo_atendimento'].apply(segundos_para_hms)
        tempo_medio_ano_mes['tempo_atendimento_horas'] = tempo_medio_ano_mes['tempo_atendimento'] / 3600  # Converter segundos para horas para a escala Y

        # Título do gráfico
        st.subheader("Tempo Médio de Atendimento por Assunto")

        # Criar o gráfico usando Altair para mostrar o tempo médio de atendimento por Assunto
        chart_tempo_medio = alt.Chart(tempo_medio_ano_mes).mark_bar().encode(
            y=alt.Y('tempo_atendimento_horas:Q', axis=alt.Axis(title='Tempo Médio de Atendimento (horas)')),  # Eixo y com tempo médio de atendimento em horas
            x=alt.X('assunto:O', axis=alt.Axis(labelAngle=0, title='Assunto'), title='Assunto'),  # Eixo x com Ano/Mês                
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )

        # Adicionar rótulos de valores no topo das barras com cor branca
        text_tempo_medio = chart_tempo_medio.mark_text(
            align='center',
            baseline='middle',
            dy=-10,  # Deslocamento vertical
            color='white'  # Cor branca para o texto
        ).encode(
            text='tempo_atendimento_hms:N'  # Mostrar o tempo médio de atendimento formatado
        )

        st.altair_chart(chart_tempo_medio + text_tempo_medio, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

    # Adicionando uma área de expansão para o Tempo Médio de Atendimento por Tipo Atendimento
    with st.expander("Tempo Médio de Atendimento por Tipo Atendimento", expanded=expander_state):

        # Agregar os dados para calcular o tempo médio de atendimento por Tipo Atendimento
        tempo_medio_ano_mes = df_atendimentos.groupby('tipo_atendimento')['tempo_atendimento'].mean().reset_index()
        tempo_medio_ano_mes['tempo_atendimento_hms'] = tempo_medio_ano_mes['tempo_atendimento'].apply(segundos_para_hms)
        tempo_medio_ano_mes['tempo_atendimento_horas'] = tempo_medio_ano_mes['tempo_atendimento'] / 3600  # Converter segundos para horas para a escala Y

        # Título do gráfico
        st.subheader("Tempo Médio de Atendimento por Tipo Atendimento")

        # Criar o gráfico usando Altair para mostrar o tempo médio de atendimento por Tipo Atendimento
        chart_tempo_medio = alt.Chart(tempo_medio_ano_mes).mark_bar().encode(
            y=alt.Y('tempo_atendimento_horas:Q', axis=alt.Axis(title='Tempo Médio de Atendimento (horas)')),  # Eixo y com tempo médio de atendimento em horas
            x=alt.X('tipo_atendimento:O', axis=alt.Axis(labelAngle=0, title='Tipo Atendimento'), title='Tipo Atendimento'),  # Eixo x com Ano/Mês                
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )

        # Adicionar rótulos de valores no topo das barras com cor branca
        text_tempo_medio = chart_tempo_medio.mark_text(
            align='center',
            baseline='middle',
            dy=-10,  # Deslocamento vertical
            color='white'  # Cor branca para o texto
        ).encode(
            text='tempo_atendimento_hms:N'  # Mostrar o tempo médio de atendimento formatado
        )

        st.altair_chart(chart_tempo_medio + text_tempo_medio, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner

# Adicionando uma área de expansão para o Tempo Médio de Atendimento por Prioridade
    with st.expander("Tempo Médio de Atendimento por Prioridade", expanded=expander_state):

        # Agregar os dados para calcular o tempo médio de atendimento por Prioridade
        tempo_medio_ano_mes = df_atendimentos.groupby('prioridade')['tempo_atendimento'].mean().reset_index()
        tempo_medio_ano_mes['tempo_atendimento_hms'] = tempo_medio_ano_mes['tempo_atendimento'].apply(segundos_para_hms)
        tempo_medio_ano_mes['tempo_atendimento_horas'] = tempo_medio_ano_mes['tempo_atendimento'] / 3600  # Converter segundos para horas para a escala Y

        # Título do gráfico
        st.subheader("Tempo Médio de Atendimento por Prioridade")

        # Criar o gráfico usando Altair para mostrar o tempo médio de atendimento por Prioridade
        chart_tempo_medio = alt.Chart(tempo_medio_ano_mes).mark_bar().encode(
            y=alt.Y('tempo_atendimento_horas:Q', axis=alt.Axis(title='Tempo Médio de Atendimento (horas)')),  # Eixo y com tempo médio de atendimento em horas
            x=alt.X('prioridade:O', axis=alt.Axis(labelAngle=0, title='Prioridade'), title='Prioridade'),  # Eixo x com Ano/Mês                
        ).properties(
            width='container',  # Ajustar a largura do gráfico
            height=400
        )

        # Adicionar rótulos de valores no topo das barras com cor branca
        text_tempo_medio = chart_tempo_medio.mark_text(
            align='center',
            baseline='middle',
            dy=-10,  # Deslocamento vertical
            color='white'  # Cor branca para o texto
        ).encode(
            text='tempo_atendimento_hms:N'  # Mostrar o tempo médio de atendimento formatado
        )

        st.altair_chart(chart_tempo_medio + text_tempo_medio, use_container_width=True)  # Ajustar a largura do gráfico para ocupar todo o contêiner
        
            
if __name__ == "__main__":
    main()