import pandas as pd
import json
from datetime import datetime

def load_data(file_path):
    """Carrega e processa o arquivo JSON do histórico do YouTube."""
    # Ler o arquivo JSON completo
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            raise ValueError("Erro ao ler o arquivo JSON. Verifique se o formato está correto.")

    # Converter para DataFrame
    df = pd.DataFrame(data)
    
    # Converter o campo 'time' para datetime
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df = df.dropna(subset=['time'])
    
    # Extrair informações temporais
    df['date'] = df['time'].dt.date
    df['month'] = df['time'].dt.month
    df['year'] = df['time'].dt.year
    df['hour'] = df['time'].dt.hour
    df['weekday'] = df['time'].dt.day_name()
    
    # Extrair informações do canal de forma segura
    def extract_channel(row):
        try:
            if isinstance(row['subtitles'], list) and len(row['subtitles']) > 0:
                return row['subtitles'][0]['name']
        except (KeyError, TypeError, IndexError):
            pass
        return 'Desconhecido'
    
    df['channel'] = df.apply(extract_channel, axis=1)
    
    # Identificar a origem (YouTube ou YouTube Music)
    def identify_source(title_url):
        try:
            if 'music.youtube.com' in str(title_url):
                return 'YouTube Music'
            return 'YouTube'
        except:
            return 'YouTube'
    
    df['platform'] = df['titleUrl'].apply(identify_source)
    
    return df[['title', 'channel', 'time', 'date', 'month', 'year', 'hour', 'weekday', 'platform']]

def get_insights(df, year=None):
    """Gera insights detalhados do histórico."""
    if year:
        df = df[df['year'] == year]
    
    if df.empty:
        return {"Erro": "Nenhum dado encontrado para o período especificado"}

    monthly_counts = df.groupby('month').size()
    top_channels = df['channel'].value_counts().head(10)
    top_videos = df['title'].value_counts().head(10)
    hourly_activity = df['hour'].value_counts().sort_index()
    weekday_activity = df['weekday'].value_counts()
    platform_dist = df['platform'].value_counts()

    return {
        "total_videos": len(df),
        "monthly_dist": monthly_counts.to_dict(),
        "top_channels": top_channels.to_dict(),
        "top_videos": top_videos.to_dict(),
        "hourly_activity": hourly_activity.to_dict(),
        "weekday_activity": weekday_activity.to_dict(),
        "platform_dist": platform_dist.to_dict(),
        "avg_videos_per_month": len(df) / df['month'].nunique(),
        "active_months": sorted(df['month'].unique().tolist())
    }