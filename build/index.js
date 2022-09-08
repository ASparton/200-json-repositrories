import repositoriesSearch from './repositories.json' assert {type: 'json'}

// Set title and total repositories
document.getElementById('title').innerText = `Repositories with "${repositoriesSearch.search_expression}" in name or description`;
document.getElementById('total-repositories').innerText = `${repositoriesSearch.total_repositories} repositories:`;

// Populate list with the repositories infos
const repositoriesContainer = document.getElementById('repositories-list');
for (let repository of repositoriesSearch.items) {
    // Repository container
    const repoTag = document.createElement('li');

    // Title and link
    let titleTag = document.createElement('a');
    titleTag.href = repository.link;
    titleTag.target = '_blank';
    titleTag.rel = 'noopener noreferrer';
    titleTag.innerHTML = `<h2>${repository.full_name}</h2>`;

    // Description
    let descriptionTag = document.createElement('h3');
    descriptionTag.innerText = repository.description;

    // Stars count
    let starsCountTag = document.createElement('p');
    starsCountTag.innerText = `Stargazers count: ${repository.stars_count}`;

    // Append to tree
    repoTag.appendChild(titleTag);
    repoTag.appendChild(descriptionTag);
    repoTag.appendChild(starsCountTag);
    repositoriesContainer.appendChild(repoTag);
}