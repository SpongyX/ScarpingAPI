function scrapeData() {
    fetch('/scrape', {
        method: 'POST'
    })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error));
}
