document.getElementById('summarizeBtn').addEventListener('click', function() {
    const text = document.getElementById('textInput').value;
    if (!text.trim()) {
        alert('Please enter text to summarize.');
        return;
    }

    fetch('https://muhammadkhalid1.pythonanywhere.com/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'  // Set the header to indicate JSON data
        },
        body: JSON.stringify({ text: text })  // Send the text as JSON
    })
    .then(response => response.json())
    .then(data => {
        const outputDiv = document.getElementById('summaryOutput');
        const summaryText = document.getElementById('summaryText');
        summaryText.textContent = data.summary || 'No summary generated.';
        outputDiv.classList.remove('hidden');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while summarizing.');
    });
});

document.getElementById('clearBtn').addEventListener('click', function() {
    document.getElementById('textInput').value = '';
    const outputDiv = document.getElementById('summaryOutput');
    const summaryText = document.getElementById('summaryText');
    summaryText.textContent = '';
    outputDiv.classList.add('hidden');
});
