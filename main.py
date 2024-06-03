import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, jsonify
import requests
import pandas as pd
import os


app = Flask(__name__)
GITHUB_API_URL = "https://api.github.com"
USER_AGENT = "Mozilla/5.0"


def fetch_user_data(username):
    headers = {'User-Agent': USER_AGENT}
    user_data = requests.get(f"{GITHUB_API_URL}/users/{username}", headers=headers).json()
    repos_data = requests.get(f"{GITHUB_API_URL}/users/{username}/repos", headers=headers).json()
    return user_data, repos_data

def process_repos_data(repos_data):
    repos_df = pd.DataFrame(repos_data)
    repos_df['created_at'] = pd.to_datetime(repos_df['created_at'])
    repos_df['updated_at'] = pd.to_datetime(repos_df['updated_at'])
    return repos_df



def plot_and_save(data, title, xlabel, ylabel, filename):

    os.makedirs('static/images', exist_ok=True)
    plt.figure(figsize=(10, 5))
    data.plot(kind='bar')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=90)
    plt.savefig(os.path.join('static/images', f'{filename}.png'))
    plt.close()
    return f'/static/images/{filename}.png'



def generate_charts(username):
    user_data, repos_data = fetch_user_data(username)
    repos_df = process_repos_data(repos_data)
    
    charts = []
    # Number of stars per repository
    stars_chart = plot_and_save(repos_df.set_index('name')['stargazers_count'], 'Stars per Repository', 'Repository', 'Stars', 'stars')
    charts.append(stars_chart)
    
    # Number of forks per repository
    forks_chart = plot_and_save(repos_df.set_index('name')['forks_count'], 'Forks per Repository', 'Repository', 'Forks', 'forks')
    charts.append(forks_chart)
    
    # Number of open issues per repository
    issues_chart = plot_and_save(repos_df.set_index('name')['open_issues_count'], 'Open Issues per Repository', 'Repository', 'Open Issues', 'issues')
    charts.append(issues_chart)
    
    # Languages used in repositories
    languages = repos_df['language'].value_counts()
    languages_chart = plot_and_save(languages, 'Languages Used', 'Language', 'Count', 'languages')
    charts.append(languages_chart)
    
    return charts


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['GET'])
def analyze():
    username = request.args.get('username')
    if username:
        charts = generate_charts(username)
        return jsonify({'charts': charts})
    else:
        return jsonify({'error': 'Invalid username'}), 400

if __name__ == "__main__":
    app.run(debug=True)
