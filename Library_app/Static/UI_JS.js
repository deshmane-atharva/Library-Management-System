function showSection(section) {
    const content = document.getElementById('content');
    if (section === 'add_member') {
        content.innerHTML = `
            <h2>Add Member</h2>
            <form id="memberForm">
                <input type="text" id="name" placeholder="Name" required><br>
                <input type="email" id="email" placeholder="Email" required><br>
                <input type="text" id="mob" placeholder="Mobile" required><br>
                <button type="submit">Add</button>
            </form>
        `;
        document.getElementById('memberForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                mob: document.getElementById('mob').value
            };
            const response = await fetch('/api/add_member', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            alert(result.message || result.error);
        });
    } else if (section === 'add_book') {
        content.innerHTML = `
            <h2>Add Book</h2>
            <form id="bookForm">
                <input type="text" id="bookName" placeholder="Book Name" required><br>
                <input type="text" id="barcode" placeholder="Barcode (Scan or type)" required autofocus><br>
                <button type="submit">Add</button>
            </form>
        `;
        document.getElementById('bookForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                name: document.getElementById('bookName').value,
                barcode: document.getElementById('barcode').value
            };
            const response = await fetch('/api/add_book', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            alert(result.message || result.error);
        });
    } else if (section === 'book_transaction') {
        content.innerHTML = `
            <h2>Book Transaction</h2>
            <form id="transactionForm">
                <select id="action">
                    <option value="issue">Issue Book</option>
                    <option value="return">Return Book</option>
                </select><br>
                <input type="text" id="barcode" placeholder="Barcode (Scan or type)" required autofocus><br>
                <input type="number" id="memberId" placeholder="Member ID" required><br>
                <button type="submit">Submit</button>
            </form>
        `;
        document.getElementById('action').addEventListener('change', () => {
            const memberField = document.getElementById('memberId');
            memberField.style.display = document.getElementById('action').value === 'return' ? 'none' : 'block';
        });
        document.getElementById('transactionForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                action: document.getElementById('action').value,
                barcode: document.getElementById('barcode').value,
                member_id: document.getElementById('memberId').value
            };
            const response = await fetch('/api/book_transaction', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            alert(result.message || result.error);
        });
    } else if (section === 'history') {
        fetch('/api/history')
            .then(response => response.json())
            .then(data => {
                let html = '<h2>Transaction History</h2><table><tr><th>Book Name</th><th>Member Name</th><th>Issue Date</th><th>Return Date</th><th>Status</th></tr>';
                data.forEach(t => {
                    html += `<tr><td>${t.books.name}</td><td>${t.members.name}</td><td>${t.issue_date}</td><td>${t.return_date}</td><td>${t.status}</td></tr>`;
                });
                html += '</table>';
                content.innerHTML = html;
            });
    }
}

