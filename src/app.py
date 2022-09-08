from requests import get as get_request
from json import dump
from sys import argv

def get_repositories(search: str, nb_repo: int = 30) -> list[dict]:
    """Search for Github repositories with the given word inside the name or description,
       and returns the wanted numbers of results if found. If no repository is found, returns an empty list.

    Args:
        search (str): The expression to search for in the repository name or description.
        nb_repo (int): The number of repositories to return if found.

    Returns:
        list[dict]: A list containing from 0 to nb_repo repositories with the matching search expression.
    """
    
    if nb_repo <= 100:
        return get_request(f"https://api.github.com/search/repositories?q={search}&per_page={nb_repo}").json()['items']
    else:
        repositories = []
        for i in range(1, int(nb_repo / 100 + 1)):
            repositories += get_request(f"https://api.github.com/search/repositories?q={search}&per_page=100&page={i}").json()['items']
        if nb_repo % 100 != 0:
            repositories += get_request(f"https://api.github.com/search/repositories?q={search}&per_page={nb_repo % 100}&page={i+1}").json()['items']
        return repositories

def get_results_count(github_api_link: str) -> int:
    """Count the total number of results returned for the given github api link.

    Args:
        github_api_link (str): The github api link without page and per_page parameter.

    Returns:
        int: The total number of results
    """
    
    counter = 0
    page = 1
    nb_page_results = 100
    while nb_page_results == 100:
        nb_page_results = len(get_request(f"{github_api_link}?per_page=100&page={page}").json())
        counter += nb_page_results
        page += 1
    return counter

def get_last_comments(comments_api_link: str, last_page_number: int) -> list[str]:
    """Returns the last 5 comments body on the given github api comments page if there are.

    Args:
        comments_api_link (str): The github comments api link to get the 5 last comments from.
        last_page_number (int): The number of the last comments page of the repository

    Returns:
        list[str]: The body of the wanted number of last comments if there are.
    """

    last_comments = []
    all_comments = get_request(f"{comments_api_link}?per_page=100&page={last_page_number}").json()
    if (len(all_comments) < 5):
        for comment in all_comments:
            last_comments.append(comment['body'])
            
        if (last_page_number == 1):
            return last_comments
        else:
            return last_comments + get_last_comments(comments_api_link, last_page_number - 1)
    else:
        for i in range(len(all_comments) - 5, len(all_comments)):
            last_comments.append(all_comments[i]['body'])
        return last_comments

# Initialize parameters and repositories list
repositories = []
search_expression = 'json' if len(argv) == 1 else argv[1]
nb_repositories = 200 if len(argv) <= 2 else int(argv[2])

# Get all repositories information
print("Get repositories information...")
full_repositories = get_repositories(search_expression, nb_repositories)

for full_repo in full_repositories:
    contributors_count = get_results_count(full_repo['contributors_url'])
    comments_url = full_repo['comments_url'].split('{')[0]
    comments_count = get_results_count(comments_url)
    comments_last_page = int(comments_count / 100) if comments_count % 100 == 0 else int(comments_count / 100) + 1
    
    # Keep needed information
    repositories.append({
        'full_name': full_repo['full_name'],
        'description': full_repo['description'],
        'link': full_repo['html_url'],
        'stars_count': full_repo['stargazers_count'],
        'contributors_count': contributors_count,
        'comments_count': comments_count,
        'last_comments': get_last_comments(comments_url, comments_last_page)
    })

# Export the result in a json file
print("Export repositories information...")
with open('build/repositories.json', 'w') as output_file:    
    dump({
            'search_expression': search_expression,
            'total_repositories': nb_repositories,
            'items': repositories
        }, output_file)
    
print("Result located in the \"build\" directory.")