function searchPerfume() {
    const query = document.getElementById('searchBar').value;
    const limit = document.getElementById('limitInput').value || 5;  // Default to 5 if not specified

    fetch(`/search?q=${query}&limit=${limit}`)
        .then(response => response.json())
        .then(data => {
            const douglasResultsDiv = document.getElementById('douglas-results');
            const parfumBGResultsDiv = document.getElementById('parfum-bg-results');
            const comparisonResultDiv = document.getElementById('comparison-result');

            douglasResultsDiv.innerHTML = '<h2>Douglas</h2>';
            parfumBGResultsDiv.innerHTML = '<h2>Parfum BG</h2>';
            comparisonResultDiv.innerHTML = '';

            let douglasFirstPrice = null;
            let parfumBGFirstPrice = null;

            if (data.error) {
                douglasResultsDiv.innerHTML += `<p>${data.error}</p>`;
                parfumBGResultsDiv.innerHTML += `<p>${data.error}</p>`;
            } else {
                data.forEach(perfume => {
                    const itemDiv = document.createElement('div');
                    itemDiv.className = 'result-item';
                    itemDiv.innerHTML = `
                        <img src="${perfume.image}" alt="${perfume.perfume_name}" class="product-image">
                        <div class="product-info">
                            <p><strong>Име:</strong> ${perfume.perfume_name}</p>
                            <p><strong>Цена:</strong> ${perfume.perfume_price} лв.</p>
                            <a href="${perfume.perfume_link}" target="_blank">Виж продукта</a>
                        </div>
                    `;

                    if (perfume.source === 'Douglas') {
                        douglasResultsDiv.appendChild(itemDiv);
                        if (douglasFirstPrice === null) {
                            douglasFirstPrice = perfume.perfume_price;
                        }
                    } else if (perfume.source === 'Parfum BG') {
                        parfumBGResultsDiv.appendChild(itemDiv);
                        if (parfumBGFirstPrice === null) {
                            parfumBGFirstPrice = perfume.perfume_price;
                        }
                    }
                });

                if (douglasFirstPrice !== null && parfumBGFirstPrice !== null) {
                    if (douglasFirstPrice > parfumBGFirstPrice) {
                        comparisonResultDiv.innerHTML = `<p>Douglas: ${douglasFirstPrice} лв. е по-скъп от Parfum BG: ${parfumBGFirstPrice} лв.</p>`;
                    } else if (douglasFirstPrice < parfumBGFirstPrice) {
                        comparisonResultDiv.innerHTML = `<p>Parfum BG: ${parfumBGFirstPrice} лв. е по-скъп от Douglas: ${douglasFirstPrice} лв.</p>`;
                    } else {
                        comparisonResultDiv.innerHTML = `<p>И двата сайта имат една и съща цена: ${douglasFirstPrice} лв.</p>`;
                    }
                }
            }

            document.querySelector('.results-container').style.display = 'flex';
            document.getElementById('homeButton').style.display = 'block';
        })
        .catch(error => console.error('Грешка:', error));
}

function goHome() {
    document.getElementById('douglas-results').innerHTML = '<h2>Douglas</h2>';
    document.getElementById('parfum-bg-results').innerHTML = '<h2>Parfum BG</h2>';
    document.querySelector('.results-container').style.display = 'none';
    document.getElementById('homeButton').style.display = 'none';
}
