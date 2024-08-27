
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

            // if (data.table) {
            //     tableDiv.innerHTML = data.table;
            // } else if (data.error) {
            //     chartsDiv.innerHTML = `<p>${data.error}</p>`;
            // } else {
            //     chartsDiv.innerHTML = '<p>User not found.</p>';
            // }

        //     if (data.table) {
        //         // Create table
        //         const table = document.createElement('table');
        //         table.border = '1';

        //         // Create table header
        //         const thead = document.createElement('thead');
        //         const headerRow = document.createElement('tr');
        //         ['Repository Name', 'Commits', 'Forks', 'Stars'].forEach(header => {
        //             const th = document.createElement('th');
        //             th.textContent = header;
        //             headerRow.appendChild(th);
        //         });
        //         thead.appendChild(headerRow);
        //         table.appendChild(thead);

        //         // Create table body
        //         const tbody = document.createElement('tbody');
        //         data.table.forEach(repo => {
        //             const row = document.createElement('tr');
        //             [repo.name, repo.commits, repo.forks, repo.stars].forEach(cellData => {
        //                 const td = document.createElement('td');
        //                 td.textContent = cellData;
        //                 row.appendChild(td);
        //             });
        //             tbody.appendChild(row);
        //         });
        //         table.appendChild(tbody);

        //         tableDiv.appendChild(table);
        //     }
         })
        .catch(error => {
            const chartsDiv = document.getElementById('charts');
            //const tableDiv = document.getElementById('repo-table');
            chartsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
            //tableDiv.innerHTML = '';
        });
}
