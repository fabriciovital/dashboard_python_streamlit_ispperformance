# ISP Performance
ISP Performance é uma aplicação web desenvolvida com Streamlit, destinada à análise de dados de atendimento de ISPs (Internet Service Providers). O projeto permite que administradores e filiais consultem, filtrem e visualizem o desempenho de atendimentos realizados, com base em dados extraídos de um banco de dados PostgreSQL.

# Funcionalidades

- Autenticação de Usuário: Implementação de um sistema de login que diferencia entre usuários administradores e filiais.
- Visualização de Dados: A aplicação exibe visualizações interativas dos atendimentos, incluindo gráficos de volume por Ano/Mês, Estado, e Cidade utilizando a biblioteca Altair.
- Filtros Avançados: Permite filtrar os dados por períodos, estados, cidades e filiais, de acordo com o tipo de usuário autenticado.
- Animações e Interface Personalizada: Apresentação inicial com animações e estilo customizado para uma experiência de usuário aprimorada.

# Tecnologias Utilizadas
Python: Linguagem principal do projeto.
Streamlit: Framework utilizado para construir a interface da aplicação.
Pandas: Utilizado para manipulação e análise de dados.
Altair: Biblioteca de visualização de dados baseada em gráficos declarativos.
psycopg2: Biblioteca para conexão com o banco de dados PostgreSQL.
PostgreSQL: Banco de dados relacional utilizado para armazenar os dados de atendimento.
CSS: Utilizado para estilização da interface e animações.

# Como Executar o Projeto
1. Clone este repositório:
```sh
git clone https://github.com/seu_usuario/isp-performance.git
cd isp-performance
```
2. Instale as dependências:
```sh
pip install -r requirements.txt
```
3. Configure o Banco de Dados:
Certifique-se de que o PostgreSQL esteja instalado e configurado.
Atualize as credenciais de conexão no arquivo main.py na função get_connection.

4. Inicie a aplicação:
```sh
streamlit run main.py
```
5. Acesse a aplicação:
Acesse a aplicação através do navegador em http://localhost:8501.

# Estrutura do Projeto
```sh
.
├── main.py           # Arquivo principal da aplicação
├── style.css         # Arquivo de estilo CSS para customização da interface
├── requirements.txt  # Lista de dependências do projeto
└── README.md         # Este arquivo
```
# Considerações de Segurança
Certifique-se de não incluir credenciais sensíveis, como senhas, diretamente no código fonte. Utilize variáveis de ambiente ou outros métodos seguros para gerenciar essas informações.

# Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

# Licença
Este projeto está licenciado sob a MIT License.
