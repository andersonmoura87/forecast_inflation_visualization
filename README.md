# Painel de Previsões Macroeconômicas do FMI

Este projeto implementa um painel interativo para visualização e análise das previsões macroeconômicas do FMI (World Economic Outlook), utilizando Streamlit e Plotly.

## 📊 Funcionalidades

- Visualização interativa de previsões e valores realizados
- Filtros por país, região, grupo de renda e período
- Gráficos de linha para evolução temporal
- Gráficos de barras para comparação entre países/regiões
- Gráfico de dispersão para comparação previsão vs. realizado
- Exportação de dados filtrados para CSV

## 🛠️ Requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/andersoncastro-moura/forecast_inflation
cd forecast_inflation
```

2. Crie e ative o ambiente virtual:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/MacOS
python -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

> Caso não tenha o Streamlit instalado globalmente, use:
> ```bash
> pip install streamlit
> ```

4. Configure o arquivo `.env`:
- Se não existir, crie um arquivo chamado `.env` na raiz do projeto
- Adicione a seguinte linha:
```
DATA_PATH="Cópia de WEO_MacroForecasts_Apr_2025.xlsx"
```

## 📈 Uso

1. Certifique-se de que o ambiente virtual está ativado
2. Execute o painel:
```bash
streamlit run dashboard_weo.py
```

3. Acesse o painel no navegador (geralmente em http://localhost:8501)

## 📁 Estrutura do Projeto

```
forecast_inflation/
├── .venv/                  # Ambiente virtual Python
├── .env                    # Variáveis de ambiente
├── .gitignore             # Arquivos ignorados pelo Git
├── README.md              # Este arquivo
├── requirements.txt       # Dependências do projeto
├── dashboard_weo.py       # Código principal do painel
└── Cópia de WEO_MacroForecasts_Apr_2025.xlsx  # Dataset do FMI (NÃO VAI PARA O GIT)
```

## 🔧 Dependências

As principais dependências do projeto estão listadas em `requirements.txt`:
- streamlit
- pandas
- plotly
- python-dotenv
- openpyxl

## ❓ FAQ (Dúvidas Frequentes)

**1. Erro: `DATA_PATH não encontrada no arquivo .env`**
- Certifique-se de que o arquivo `.env` existe na raiz do projeto e contém a linha:
  ```
  DATA_PATH="Cópia de WEO_MacroForecasts_Apr_2025.xlsx"
  ```
- O nome do arquivo deve ser exatamente `.env` (sem extensão adicional).

**2. Erro: Arquivo Excel não encontrado**
- Verifique se o arquivo Excel está no local correto e com o nome igual ao especificado no `.env`.
- Se estiver em uma subpasta, ajuste o caminho no `.env` (ex: `DATA_PATH="data/Cópia de WEO_MacroForecasts_Apr_2025.xlsx"`).

**3. O painel não abre no navegador**
- Verifique se o Streamlit está instalado e se o comando `streamlit run dashboard_weo.py` foi executado no diretório correto.

**4. O arquivo Excel não aparece no GitHub**
- Por padrão, o arquivo Excel está listado no `.gitignore` e não será versionado pelo Git.

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor, siga estas etapas:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Veja o arquivo `LICENSE` para mais detalhes.

## 📧 Desenvolvedores e Contato
Este projeto foi desenvolvido por:

Mateus Ramalho Ribeiro da Fonseca
LinkedIn: linkedin.com/in/mateus-rr-fonseca
Email: mateusramalho88@gmail.com
Anderson de Castro Moura
LinkedIn: linkedin.com/in/andersondecastromoura
Email: andersoncastromoura@gmail.com
Link do Projeto: github.com/andersoncastro-moura/forecast_inflation   