from collections import Counter
import os
import requests
import matplotlib.pyplot as plt

GITHUB_USERNAME = "andregoncallez"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_repos(username):
    repos = []
    page = 1
    headers = {}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'

    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}&type=all"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Erro: {response.status_code}, {response.text}")
            break
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def get_language_stats(repos):
    language_counter = Counter()
    for repo in repos:
        lang = repo.get("language")
        if lang:
            language_counter[lang] += 1
    return language_counter

def plot_language_stats(language_stats, output_file="top_langs.png"):
    labels = list(language_stats.keys())
    sizes = list(language_stats.values())
    total = sum(sizes)
    percentages = [(size / total) * 100 for size in sizes]
    colors = plt.cm.tab10.colors
    plt.figure(figsize=(10, 6))
    bars = plt.barh(labels, percentages, color=colors[:len(labels)])
    plt.xlabel('Porcentagem de Uso (%)')
    plt.title(f"Linguagens mais usadas por {GITHUB_USERNAME} (Incluindo Forks)")
    for bar, percent in zip(bars, percentages):
        plt.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2, f'{percent:.1f}%', va='center')
    plt.tight_layout()
    plt.savefig(output_file, dpi=200)
    plt.close()
    print(f"Gráfico salvo como {output_file}")

if __name__ == "__main__":
    repos = get_repos(GITHUB_USERNAME)
    language_stats = get_language_stats(repos)
    plot_language_stats(language_stats)