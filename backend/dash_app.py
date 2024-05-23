import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
from models import Progress  # Import Progress model

def create_dash_app(flask_app):
    app = dash.Dash(server=flask_app, name="DashApp", url_base_pathname='/dash/')

    app.layout = html.Div([
        dcc.Graph(id='progress-graph'),
        dcc.Interval(id='interval-component', interval=60*1000, n_intervals=0)  # Update every minute
    ])

    @app.callback(Output('progress-graph', 'figure'),
                  [Input('interval-component', 'n_intervals')])
    def update_graph(n):
        # Fetch progress data from the database
        progress_entries = Progress.query.all()
        if not progress_entries:
            return {}

        data = [{
            'word': entry.vocabulary.word,
            'date_practiced': entry.date_practiced,
            'score': entry.score
        } for entry in progress_entries]

        df = pd.DataFrame(data)
        avg_scores = df.groupby('word')['score'].mean().reset_index()
        practice_counts = df.groupby('word')['score'].count().reset_index().rename(columns={'score': 'practice_count'})
        progress_df = pd.merge(avg_scores, practice_counts, on='word')

        fig, ax1 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='word', y='score', data=progress_df, ax=ax1)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        encoded_image = base64.b64encode(buf.read()).decode('utf-8')
        return {'data': [{'x': progress_df['word'], 'y': progress_df['score'], 'type': 'bar'}]}

    return app
