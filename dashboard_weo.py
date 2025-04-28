import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Painel de Previsões Macroeconômicas do FMI",
    page_icon="📊",
    layout="wide"
)

# Cache the data loading function
@st.cache_data
def load_data():
    """Load and preprocess the WEO dataset."""
    try:
        data_path = os.getenv("DATA_PATH")
        if not data_path:
            st.error("DATA_PATH não encontrada no arquivo .env")
            return None
        
        df = pd.read_excel(data_path)
        
        # Basic data validation
        required_columns = [
            'Country', 'CCode', 'weo_year', 'exercise', 'year', 'Region',
            'incomegroup', 'Fngdp_rpc', 'pcpi_pch', 'bca_gdp',
            'Rngdp_rpc', 'Rpcpi_pch', 'Rbca_gdp'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Colunas faltantes no dataset: {missing_columns}")
            return None
            
        # Convert year to integer
        df['year'] = df['year'].astype(int)
        
        # Handle extreme values (e.g., Zimbabwe's hyperinflation)
        for col in ['pcpi_pch', 'Rpcpi_pch']:
            df[col] = df[col].clip(-100, 100)  # Cap inflation at ±100%
            
        return df
    
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}")
        return None

def create_line_plot(df, countries, variable, title):
    """Create an interactive line plot."""
    fig = px.line(
        df[df['Country'].isin(countries)],
        x='year',
        y=variable,
        color='Country',
        title=title,
        labels={
            'year': 'Ano',
            variable: 'Valor (%)',
            'Country': 'País/Agregado'
        }
    )
    fig.update_layout(
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig

def create_bar_plot(df, variable, year, group_by='Country'):
    """Create a bar plot comparing values across countries/regions."""
    df_filtered = df[df['year'] == year]
    df_grouped = df_filtered.groupby(group_by)[variable].mean().reset_index()
    
    fig = px.bar(
        df_grouped,
        x=group_by,
        y=variable,
        title=f'Média de {variable} por {group_by} em {year}',
        labels={
            group_by: group_by,
            variable: 'Valor (%)'
        }
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False
    )
    return fig

def create_scatter_plot(df, variable, year):
    """Create a scatter plot comparing forecast vs actual values."""
    forecast_col = variable
    actual_col = 'R' + variable[1:] if variable.startswith('F') else variable
    
    df_filtered = df[df['year'] == year]
    
    fig = px.scatter(
        df_filtered,
        x=forecast_col,
        y=actual_col,
        color='Country',
        title=f'Previsão vs. Realizado - {variable} em {year}',
        labels={
            forecast_col: 'Previsão (%)',
            actual_col: 'Realizado (%)',
            'Country': 'País/Agregado'
        }
    )
    
    # Add 45-degree line
    max_val = max(df_filtered[[forecast_col, actual_col]].max())
    fig.add_trace(
        go.Scatter(
            x=[0, max_val],  
            y=[0, max_val],
            mode='lines',
            line=dict(dash='dash', color='gray'),
            name='Linha de 45°'
        )
    )
    
    return fig

def main():
    # Load data
    df = load_data()
    if df is None:
        st.stop()
    
    # Sidebar filters
    st.sidebar.title("Filtros")
    
    # Country selection (multiselect, removendo nulos)
    country_options = sorted([x for x in df['Country'].unique().tolist() if pd.notnull(x)])
    countries = st.sidebar.multiselect(
        "Selecione países/agregados",
        options=country_options,
        default=['Brazil', 'United States', 'World'] if set(['Brazil', 'United States', 'World']).issubset(set(country_options)) else country_options[:1]
    )
    
    if not countries:
        st.warning("Selecione ao menos um país/agregado na barra lateral para visualizar os dados.")
        st.stop()
    
    # Year range selection
    min_year, max_year = int(df['year'].min()), int(df['year'].max())
    year_range = st.sidebar.slider(
        "Selecione o intervalo de anos",
        min_year,
        max_year,
        (min_year, max_year)
    )
    
    # Region selection (removendo nulos)
    region_options = ['Todas'] + sorted([x for x in df['Region'].unique().tolist() if pd.notnull(x)])
    selected_region = st.sidebar.selectbox(
        "Selecione a região",
        options=region_options
    )
    
    # Income group selection (removendo nulos)
    income_groups = ['Todos'] + sorted([x for x in df['incomegroup'].unique().tolist() if pd.notnull(x)])
    selected_income = st.sidebar.selectbox(
        "Selecione o grupo de renda",
        options=income_groups
    )
    
    # Variable type selection
    variable_type = st.sidebar.radio(
        "Selecione o tipo de variável",
        options=['Previsões', 'Valores Realizados']
    )
    
    # Variable selection
    if variable_type == 'Previsões':
        variables = {
            'Crescimento do PIB': 'Fngdp_rpc',
            'Inflação': 'pcpi_pch',
            'Balanço de Conta Corrente': 'bca_gdp'
        }
    else:
        variables = {
            'Crescimento do PIB': 'Rngdp_rpc',
            'Inflação': 'Rpcpi_pch',
            'Balanço de Conta Corrente': 'Rbca_gdp'
        }
    
    selected_variable = st.sidebar.selectbox(
        "Selecione a variável",
        options=list(variables.keys())
    )
    
    # Apply filters
    filtered_df = df[
        (df['Country'].isin(countries)) &
        (df['year'].between(year_range[0], year_range[1]))
    ]
    
    if selected_region != 'Todas':
        filtered_df = filtered_df[filtered_df['Region'] == selected_region]
    
    if selected_income != 'Todos':
        filtered_df = filtered_df[filtered_df['incomegroup'] == selected_income]
    
    # Main content
    st.title("Painel de Previsões Macroeconômicas do FMI")
    
    st.markdown("""
    Este painel interativo permite explorar as previsões macroeconômicas do FMI (World Economic Outlook) 
    desde 1990 para diversos países, regiões e agregados econômicos. Os dados incluem previsões e valores 
    realizados para crescimento do PIB, inflação e balanço de conta corrente.
    """)
    
    # Line plot
    st.subheader("Evolução Temporal")
    fig_line = create_line_plot(
        filtered_df,
        countries,
        variables[selected_variable],
        f"Evolução de {selected_variable} ao longo do tempo"
    )
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Bar plot
    st.subheader("Comparação entre Países/Regiões")
    selected_year = st.selectbox(
        "Selecione o ano para comparação",
        options=sorted(filtered_df['year'].unique())
    )
    
    group_by = st.radio(
        "Agrupar por",
        options=['Country', 'Region'],
        format_func=lambda x: 'País' if x == 'Country' else 'Região'
    )
    
    fig_bar = create_bar_plot(
        filtered_df,
        variables[selected_variable],
        selected_year,
        group_by
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Scatter plot (optional)
    st.subheader("Comparação Previsão vs. Realizado")
    show_scatter = st.checkbox("Mostrar gráfico de dispersão")
    
    if show_scatter:
        if variable_type != 'Previsões':
            st.info("O gráfico de dispersão só está disponível para variáveis de previsão.")
        else:
            fig_scatter = create_scatter_plot(
                filtered_df,
                variables[selected_variable],
                selected_year
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Data table
    st.subheader("Dados Filtrados")
    st.dataframe(
        filtered_df[[
            'Country', 'year', 'Region', 'incomegroup',
            variables[selected_variable]
        ]].sort_values(['Country', 'year']),
        use_container_width=True
    )
    
    # Export button (sempre visível, só habilitado se houver dados)
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Baixar CSV",
        data=csv,
        file_name="weo_filtered_data.csv",
        mime="text/csv",
        disabled=filtered_df.empty
    )


# Rodapé com créditos, GitHub e LinkedIn
st.markdown("""
<div style="text-align: center; padding: 20px 0; font-size: 14px; color: #555;">
    Desenvolvido por Mateus Fonseca e Anderson de Castro Moura<br><br>
    <a href="https://github.com/andersonmoura87/forecast_inflation_visualization" 
       target="_blank" 
       style="color: #0366d6; text-decoration: none; margin: 0 15px;"
       onmouseover="this.style.textDecoration='underline';"
       onmouseout="this.style.textDecoration='none';"
       aria-label="Repositório do projeto no GitHub">
        <svg style="vertical-align: middle; margin-right: 5px;" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
            <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
        </svg>
        Repositório no GitHub
    </a><br><br>
    <a href="https://www.linkedin.com/in/mateus-rr-fonseca/" 
       target="_blank" 
       style="color: #0366d6; text-decoration: none; margin: 0 15px;"
       onmouseover="this.style.textDecoration='underline';"
       onmouseout="this.style.textDecoration='none';"
       aria-label="Perfil do LinkedIn de Mateus Fonseca">
        <svg style="vertical-align: middle; margin-right: 5px;" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
            <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>
        </svg>
        Mateus Fonseca
    </a>
    <a href="https://www.linkedin.com/in/andersondecastromoura/" 
       target="_blank" 
       style="color: #0366d6; text-decoration: none; margin: 0 15px;"
       onmouseover="this.style.textDecoration='underline';"
       onmouseout="this.style.textDecoration='none';"
       aria-label="Perfil do LinkedIn de Anderson de Castro Moura">
        <svg style="vertical-align: middle; margin-right: 5px;" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
            <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>
        </svg>
        Anderson de Castro Moura
    </a>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main() 