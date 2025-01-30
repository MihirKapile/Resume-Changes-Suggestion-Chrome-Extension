chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'getJobDescription') {
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, { action: 'getJobDescription' }, (response) => {
          if (response && response.jobDescription) {
            console.log('Job Description received:', response.jobDescription);
          } else {
            console.error('Failed to retrieve job description.');
          }
        });
      });
    }
  });
  
  chrome.action.onClicked.addListener((tab) => {
    console.log('Extension icon clicked');
  });
  