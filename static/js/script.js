function analyze() {
    const username = document.getElementById('username').value;
    fetch(`/analyze?username=${username}`)
        .then(response => response.json())
        .then(data => {
            const chartsDiv = document.getElementById('charts');
            chartsDiv.innerHTML = '';
            if (data.charts) {
                data.charts.forEach(chart => {
                    const img = document.createElement('img');
                    img.src = chart;
                    chartsDiv.appendChild(img);
                });
            } else {
                chartsDiv.innerHTML = '<p>User not found.</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
