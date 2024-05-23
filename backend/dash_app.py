import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from models import Progress  # Import your Progress model


def create_dash_app(flask_app):
    app = dash.Dash(server=flask_app, name="DashApp", url_base_pathname='/dash/')

    app.layout = html.Div([
        html.H2("User Progress Summary"),
        dcc.Graph(id='average-score-graph'),
        dcc.Graph(id='practice-count-graph'),
        dcc.Graph(id='overall-statistics-graph'),
        dcc.Interval(id='interval-component', interval=60 * 1000, n_intervals=0)  # Update every minute
    ])

    @app.callback(
        [
            Output('average-score-graph', 'figure'),
            Output('practice-count-graph', 'figure'),
            Output('overall-statistics-graph', 'figure')
        ],
        [Input('interval-component', 'n_intervals')]
    )
    def update_graphs(n):
        # Fetch progress data from the database
        progress_entries = Progress.query.all()
        if not progress_entries:
            return {}, {}, {}

        data = [{
            'word': entry.vocabulary.word,
            'date_practiced': entry.date_practiced.strftime('%Y-%m-%d %H:%M:%S'),
            'score': entry.score
        } for entry in progress_entries]

        df = pd.DataFrame(data)

        # Calculate overall statistics
        total_practices = len(df)
        average_score = df['score'].mean()
        max_score = df['score'].max()
        min_score = df['score'].min()
        std_dev = df['score'].std()

        # Calculate performance per word
        performance_per_word = df.groupby('word')['score'].agg(['mean', 'count']).reset_index()
        performance_per_word.rename(columns={'mean': 'average_score', 'count': 'practice_count'}, inplace=True)

        # Create average score plot
        fig1, ax1 = plt.subplots()
        sns.barplot(x='word', y='average_score', data=performance_per_word, ax=ax1)
        ax1.set_title('Average Score per Word')
        ax1.set_xlabel('Word')
        ax1.set_ylabel('Average Score')

        buf1 = BytesIO()
        plt.savefig(buf1, format='png')
        plt.close(fig1)
        buf1.seek(0)
        encoded_image1 = base64.b64encode(buf1.read()).decode('utf-8')

        # Create practice count plot
        fig2, ax2 = plt.subplots()
        sns.barplot(x='word', y='practice_count', data=performance_per_word, ax=ax2)
        ax2.set_title('Practice Count per Word')
        ax2.set_xlabel('Word')
        ax2.set_ylabel('Practice Count')

        buf2 = BytesIO()
        plt.savefig(buf2, format='png')
        plt.close(fig2)
        buf2.seek(0)
        encoded_image2 = base64.b64encode(buf2.read()).decode('utf-8')

        # Create overall statistics plot
        fig3, ax3 = plt.subplots()
        overall_stats = pd.DataFrame({
            'Statistic': ['Total Practices', 'Average Score', 'Max Score', 'Min Score', 'Std Dev'],
            'Value': [total_practices, average_score, max_score, min_score, std_dev]
        })
        sns.barplot(x='Statistic', y='Value', data=overall_stats, ax=ax3)
        ax3.set_title('Overall Statistics')
        ax3.set_xlabel('Statistic')
        ax3.set_ylabel('Value')

        buf3 = BytesIO()
        plt.savefig(buf3, format='png')
        plt.close(fig3)
        buf3.seek(0)
        encoded_image3 = base64.b64encode(buf3.read()).decode('utf-8')

        return {
            'data': [{'x': performance_per_word['word'], 'y': performance_per_word['average_score'], 'type': 'bar'}]
        }, {
            'data': [{'x': performance_per_word['word'], 'y': performance_per_word['practice_count'], 'type': 'bar'}]
        }, {
            'data': [{'x': overall_stats['Statistic'], 'y': overall_stats['Value'], 'type': 'bar'}]
        }

    return app
