import pandas as pd
from datetime import datetime

def load_data(file_path):
    """Carrega e processa o arquivo JSON do histórico do YouTube."""
    # Ler o arquivo JSON
    data = pd.read_json(file_path)

    # Filtrar apenas entradas relacionadas ao YouTube
    df = data[data['header'] == 'YouTube']

    # Transformar subtítulos (nome do canal) em uma string
    df['channel'] = df['subtitles'].apply(lambda x: x[0]['name'] if isinstance(x, list) and len(x) > 0 else None)

    # Converter o campo 'time' para datetime
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df['date'] = df['time'].dt.date
    df['month'] = df['time'].dt.month
    df['year'] = df['time'].dt.year

    # Filtrar apenas o ano atual (2024)
    df = df[df['year'] == 2024]

    # Selecionar as colunas relevantes
    return df[['title', 'channel', 'time', 'date', 'month', 'year']]

def get_insights(df):
    """Gera insights básicos do histórico (somente 2024)."""
    insights = {
        "Total de vídeos assistidos (2024)": len(df),
        "Mês mais ativo (2024)": df['month'].mode()[0],
        "Vídeo mais assistido (2024)": df['title'].mode()[0],
        "Canal mais assistido (2024)": df['channel'].mode()[0]
    }
    return insights

