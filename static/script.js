async function checkURL() {
    const urlInput = document.getElementById('urlInput');
    const resultBox = document.getElementById('result');
    const url = urlInput.value.trim();

    if (!url) {
        resultBox.innerText = "Please enter a URL.";
        resultBox.classList.remove('hidden');
        resultBox.style.color = 'orange';
        return;
    }

    try {
        const response = await fetch('/classify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });

        const data = await response.json();

        let resultText = `Result: ${data.result}`;
        if (data.reasons && data.reasons.length > 0) {
            resultText += `\nReason(s):\n- ${data.reasons.join('\n- ')}`;
        }

        resultBox.innerText = resultText;
        resultBox.style.whiteSpace = 'pre-line'; // Keep line breaks
        resultBox.style.color = data.result === 'Phishing' ? 'red' : 'green';
        resultBox.classList.remove('hidden');

    } catch (error) {
        resultBox.innerText = "Error: Could not connect to the server.";
        resultBox.style.color = 'orange';
        resultBox.classList.remove('hidden');
    }
}

