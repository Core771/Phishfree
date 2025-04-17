chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'showPhishingResult') {
        alert('This website is classified as: ' + request.result);
    }
});
