import pandas as pd
from process_data import load_data, get_insights
from visualize import create_visualizations

# Carregar o arquivo JSON do histórico
history_file = 'history.json'

# Processar os dados
df = load_data(history_file)

# Obter insights
insights = get_insights(df)

# Exibir insights
for key, value in insights.items():
    print(f"{key}: {value}")

# Criar visualizações
create_visualizations(df)
