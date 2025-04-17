chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url) {
        fetch('http://localhost:5000/classify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: tab.url })
        })
        .then(res => res.json())
        .then(data => {
            if (data.result === "Phishing") {
                chrome.notifications.create({
                    type: "basic",
                    iconUrl: "icon.png",
                    title: "⚠️ Phishing Alert",
                    message: `This site might be unsafe!\nReasons: ${data.reasons.join(", ")}`
                });
            } else {
                console.log("Safe site:", tab.url);
            }
        })
        .catch(error => {
    console.error("Fetch error:", error);
    chrome.notifications.create({
        type: "basic",
        iconUrl: "icon.png",
        title: "Phishing Detection - Error",
        message: `Could not connect to server: ${error.message}`
    });
});
    }
