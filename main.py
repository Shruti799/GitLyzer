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



def plot_and_save(data, title, xlabel, ylabel, filename, chart_type='line'):
    os.makedirs('static/images', exist_ok=True)
    plt.figure(figsize=(10, 5))
    
    if chart_type == 'pie':
        data.plot(kind='pie', autopct='%1.1f%%')
        plt.title(title, fontsize=20, fontweight='bold')
        plt.ylabel('')  # Hide the y-label for pie charts
    else:
        data.plot(kind=chart_type)
        plt.title(title, fontsize=20, fontweight='bold')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=35, ha='right')
    
    plt.savefig(os.path.join('static/images', f'{filename}.png'))
    plt.close()
    return f'/static/images/{filename}.png'




def generate_charts(username):
    user_data, repos_data = fetch_user_data(username)
    repos_df = process_repos_data(repos_data)
    
    charts = []

    # Languages used in repositories
    languages = repos_df['language'].value_counts()
    languages_chart = plot_and_save(languages, 'Languages Used', '', '', 'languages', 'pie')
    charts.append(languages_chart)

    # Number of stars per repository
    stars_chart = plot_and_save(repos_df.set_index('name')['stargazers_count'], 'Stars per Repository', 'Repository', 'Stars', 'stars')
    charts.append(stars_chart)
    
    # Number of forks per repository
    forks_chart = plot_and_save(repos_df.set_index('name')['forks_count'], 'Forks per Repository', 'Repository', 'Forks', 'forks')
    charts.append(forks_chart)
    
    # Number of open issues per repository
    issues_chart = plot_and_save(repos_df.set_index('name')['open_issues_count'], 'Open Issues per Repository', 'Repository', 'Open Issues', 'issues')
    charts.append(issues_chart)
    
    
    return charts


def generate_table(username):
    _, repos_data = fetch_user_data(username)
    repos_df = process_repos_data(repos_data)
    
    # Create HTML table
    table_html = '<table class="table table-bordered"><thead><tr><th>Repository Name</th><th>Commits</th><th>Forks</th><th>Stars</th></tr></thead><tbody>'
    
    for _, row in repos_df.iterrows():
        table_html += f'<tr><td>{row["name"]}</td><td>{row["commits_count"]}</td><td>{row["forks_count"]}</td><td>{row["stargazers_count"]}</td></tr>'
    
    table_html += '</tbody></table>'
    
    return table_html



@app.route('/')
def base():
    return render_template('base.html')

@app.route('/index.html')
def index_html():
    return render_template('index.html')


@app.route('/analyze', methods=['GET'])
def analyze():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Invalid username'}), 400
    try:
        charts = generate_charts(username)
        #table_html = generate_table(username)

        return jsonify({'charts': charts})
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error fetching data from GitHub: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    

if __name__ == "__main__":
    app.run(debug=True)

