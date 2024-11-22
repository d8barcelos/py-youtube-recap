import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from process_data import load_data, get_insights
import calendar

st.set_page_config(
    page_title="YouTube History Viewer",
    page_icon="▶️",
    layout="wide"
)

# Função para criar gráfico de atividade mensal
def plot_monthly_activity(monthly_data):
    months = list(calendar.month_name)[1:]
    values = [monthly_data.get(i, 0) for i in range(1, 13)]
    
    fig = px.bar(
        x=months,
        y=values,
        title="Distribuição Mensal de Vídeos Assistidos",
        labels={'x': 'Mês', 'y': 'Número de Vídeos'}
    )
    return fig

# Função para criar gráfico de top canais
def plot_top_channels(channel_data):
    fig = px.bar(
        x=list(channel_data.values()),
        y=list(channel_data.keys()),
        orientation='h',
        title="Top Canais Mais Assistidos",
        labels={'x': 'Número de Vídeos', 'y': 'Canal'}
    )
    return fig

# Função para criar gráfico de atividade por hora
def plot_hourly_activity(hourly_data):
    hours = list(range(24))
    values = [hourly_data.get(hour, 0) for hour in hours]
    
    fig = px.line(
        x=hours,
        y=values,
        title="Atividade por Hora do Dia",
        labels={'x': 'Hora', 'y': 'Número de Vídeos'}
    )
    return fig

# Função para criar gráfico de atividade por dia da semana
def plot_weekday_activity(weekday_data):
    fig = px.bar(
        x=list(weekday_data.keys()),
        y=list(weekday_data.values()),
        title="Atividade por Dia da Semana",
        labels={'x': 'Dia da Semana', 'y': 'Número de Vídeos'}
    )
    return fig

# Função para criar gráfico de distribuição por plataforma
def plot_platform_distribution(platform_data):
    fig = px.pie(
        values=list(platform_data.values()),
        names=list(platform_data.keys()),
        title="Distribuição por Plataforma"
    )
    return fig

def main():
    st.title("📊 YouTube History Viewer")
    
    # Upload do arquivo
    uploaded_file = st.file_uploader("Escolha seu arquivo JSON do histórico do YouTube", type=['json'])
    
    if uploaded_file is not None:
        # Salvando o arquivo temporariamente
        with open("temp_history.json", "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Carregando os dados
        df = load_data("temp_history.json")
        
        # Seletor de ano
        years = sorted(df['year'].unique())
        selected_year = st.selectbox("Selecione o ano", years)
        
        # Obtendo insights
        insights = get_insights(df, selected_year)
        
        # Layout em colunas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total de Vídeos", insights["total_videos"])
        with col2:
            st.metric("Média Mensal", f"{insights['avg_videos_per_month']:.1f}")
        with col3:
            st.metric("Meses Ativos", len(insights["active_months"]))
        
        # Gráficos
        st.plotly_chart(plot_monthly_activity(insights["monthly_dist"]), use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_top_channels(insights["top_channels"]), use_container_width=True)
        with col2:
            st.plotly_chart(plot_platform_distribution(insights["platform_dist"]), use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_hourly_activity(insights["hourly_activity"]), use_container_width=True)
        with col2:
            st.plotly_chart(plot_weekday_activity(insights["weekday_activity"]), use_container_width=True)
        
        # Top vídeos em uma tabela expandível
        with st.expander("Ver Top Vídeos"):
            st.table(pd.DataFrame(list(insights["top_videos"].items()), 
                                columns=['Título', 'Visualizações']).reset_index(drop=True))

if __name__ == "__main__":
    main()