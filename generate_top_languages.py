import requests
from collections import Counter
import os
import matplotlib.pyplot as plt

# -------- CONFIGURAÇÕES --------
GITHUB_USERNAME = "andregoncallez"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Opcional: export GITHUB_TOKEN=xxxxxxx

# -------- FUNÇÃO PARA BUSCAR REPOS --------
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

# -------- FUNÇÃO PARA CONTAR LINGUAGENS --------
def get_language_stats(repos):
    language_counter = Counter()

    for repo in repos:
        lang = repo.get("language")
        if lang:
            language_counter[lang] += 1

    return language_counter

# -------- FUNÇÃO PARA GERAR O GRÁFICO --------
def plot_language_stats(language_stats, output_file="top_langs.png"):
    labels = []
    sizes = []

    total = sum(language_stats.values())
    for language, count in language_stats.most_common():
        labels.append(f"{language} ({count})")
        sizes.append(count)

    if not sizes:
        print("Nenhuma linguagem detectada para plotar.")
        return

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct=lambda p: f'{p:.1f}%', startangle=140, textprops={'fontsize': 10})
    plt.title(f"Linguagens mais usadas por {GITHUB_USERNAME} (Incluindo Forks)", fontsize=14)
    plt.axis('equal')  # Para o gráfico ficar circular

    plt.tight_layout()
    plt.savefig(output_file, dpi=200)
    plt.close()
    print(f"Gráfico salvo como {output_file}")

# -------- MAIN --------
if __name__ == "__main__":
    repos = get_repos(GITHUB_USERNAME)
    print(f"Total de repositórios encontrados (incluindo forks): {len(repos)}\n")

    language_stats = get_language_stats(repos)

    print("Top Linguagens (incluindo forks):\n")
    for language, count in language_stats.most_common():
        print(f"{language}: {count} repositórios")

    plot_language_stats(language_stats)
