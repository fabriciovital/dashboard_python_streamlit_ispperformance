import streamlit as st
import pandas as pd
import altair as alt

# Define a configuração da página no Streamlit
st.set_page_config(page_title="ISP Performance - Decisões inteligentes, baseadas em dados confiáveis para o sucesso do seu provedor!", page_icon="📊", layout="wide")

# Load Style CSS
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Função principal do Streamlit
def main():
    if 'loggedin' not in st.session_state:
        st.session_state.loggedin = False

    if not st.session_state.loggedin:
        login()
    else:
        app_interface()

# Função para exibir a tela de login
def login():
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

    st.sidebar.title("Login")
    username = st.sidebar.text_input("Usuário")
    password = st.sidebar.text_input("Senha", type="password")
    if st.sidebar.button("Login"):
        if username == "admin" and password == "admin":
            st.session_state.loggedin = True
            st.session_state.username = username  # Armazena o nome do usuário na sessão
            st.experimental_rerun()  # Recarregar a página após login bem-sucedido
            main()  # Chamada da função principal novamente
        else:
            st.sidebar.error("Usuário ou senha incorretos.")

# Limpa a barra lateral sempre que a função login é chamada
    st.sidebar.empty()

# Função para exibir a interface da aplicação
def app_interface():
    st.header("ANALISE DE PERFORMANCE | INDICADORES & PROGRESSÃO ")

    # Exibe o nome do usuário logado acima do botão Sair
    st.sidebar.write(f"Bem-vindo, {st.session_state.username}!")
    
    # Botão Sair
    if st.sidebar.button("Sair"):
        st.session_state.loggedin = False
        st.session_state.expander_state = False        
        st.experimental_rerun()  # Recarregar a página após sair
        
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

    # Carregar os dados do arquivo CSV
    df_atendimentos = pd.read_csv('atendimentos.csv')

    # Verificar as colunas disponíveis no DataFrame
    colunas_disponiveis = df_atendimentos.columns.tolist()

    # Verificar se todas as colunas necessárias estão presentes
    if all(coluna in colunas_disponiveis for coluna in ['uf', 'cidade', 'filial']):

        # Configura os filtros na barra lateral para estado
        estados_selecionados = st.sidebar.multiselect(
            "Selecione Estado",
            options=df_atendimentos['uf'].unique(),
            default=None
        )

        # Configura os filtros na barra lateral para cidade
        cidades_selecionadas = st.sidebar.multiselect(
            "Selecione Cidade",
            options=df_atendimentos[df_atendimentos['uf'].isin(estados_selecionados)]['cidade'].unique(),
            default=None
        )

        # Configura os filtros na barra lateral para filial
        filiais_selecionadas = st.sidebar.multiselect(
            "Selecione Filial",
            options=df_atendimentos[df_atendimentos['cidade'].isin(cidades_selecionadas)]['filial'].unique(),
            default=None
        )

    # Filtrar o DataFrame baseado nos filtros selecionados
    if estados_selecionados:
        df_atendimentos = df_atendimentos[df_atendimentos['uf'].isin(estados_selecionados)]
    if cidades_selecionadas:
        df_atendimentos = df_atendimentos[df_atendimentos['cidade'].isin(cidades_selecionadas)]
    if filiais_selecionadas:
        df_atendimentos = df_atendimentos[df_atendimentos['filial'].isin(filiais_selecionadas)]

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