import matplotlib.pyplot as plt
import seaborn as sns

def create_visualizations(df):
    """Cria gráficos a partir dos dados processados (somente 2024)."""
    sns.set(style="whitegrid", palette="muted")

    # Gráfico de vídeos assistidos por mês
    videos_per_month = df['month'].value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=videos_per_month.index, y=videos_per_month.values, palette="coolwarm")
    plt.title('Vídeos Assistidos por Mês (2024)', fontsize=16)
    plt.xlabel('Mês', fontsize=12)
    plt.ylabel('Quantidade de Vídeos', fontsize=12)
    plt.xticks(ticks=range(12), labels=[
        'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
        'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'], rotation=45)
    plt.tight_layout()
    plt.savefig('videos_por_mes_2024.png')
    plt.show()

    # Top 10 canais mais assistidos
    top_channels = df['channel'].value_counts().head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_channels.values, y=top_channels.index, palette="viridis")
    plt.title('Top 10 Canais Mais Assistidos (2024)', fontsize=16)
    plt.xlabel('Quantidade de Vídeos', fontsize=12)
    plt.ylabel('Canal', fontsize=12)
    plt.tight_layout()
    plt.savefig('top_canais_2024.png')
    plt.show()
