
// function analyze() {
//     const username = document.getElementById('username').value;
//     fetch(`/analyze?username=${username}`)
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();
//         })
//         .then(data => {
//             const chartsDiv = document.getElementById('charts');
//             chartsDiv.innerHTML = '';
//             if (data.charts) {
//                 data.charts.forEach(chart => {
//                     const img = document.createElement('img');
//                     img.src = chart;
//                     chartsDiv.appendChild(img);
//                 });
//             } else if (data.error) {
//                 chartsDiv.innerHTML = `<p>${data.error}</p>`;
//             } else {
//                 chartsDiv.innerHTML = '<p>User not found.</p>';
//             }
//         })
//         .catch(error => {
//             const chartsDiv = document.getElementById('charts');
//             chartsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
//         });
// }

function analyze() {
    const username = document.getElementById('username').value;
    fetch(`/analyze?username=${username}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const chartsDiv = document.getElementById('charts');
            //const tableDiv = document.getElementById('repo-table');
            
            // Clear previous content
            chartsDiv.innerHTML = '';
            //tableDiv.innerHTML = '';

            if (data.charts) {
                // Display charts
                data.charts.forEach(chart => {
                    const img = document.createElement('img');
                    img.src = chart;
                    chartsDiv.appendChild(img);
                });
            } else if (data.error) {
                chartsDiv.innerHTML = `<p>${data.error}</p>`;
            } else {
                chartsDiv.innerHTML = '<p>User not found.</p>';
            }
         })
        .catch(error => {
            const chartsDiv = document.getElementById('charts');
            //const tableDiv = document.getElementById('repo-table');
            chartsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
            //tableDiv.innerHTML = '';
        });
}
