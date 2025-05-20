import pandas as pd

def process_survey_results(path):
    df = pd.read_csv(path)
    # Mapear sentimiento a valor numérico
    df['sentiment_num'] = df['sentiment'].map({'Positivo': 1, 'Negativo': -1})
    grouped = df.groupby('route_id').agg({
        'satisfaction': 'mean',
        'wait_time_rating': 'mean',
        'sentiment_num': 'mean'
    }).reset_index()
    survey_stats = grouped.set_index('route_id').to_dict(orient='index')
    return survey_stats
