chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'getJobDescription') {
      let jobDescriptionElement = document.querySelector('.jobs-description-content__text');
      
      if (jobDescriptionElement) {
        const jobDescription = jobDescriptionElement.innerText;
        console.log('Job Description:', jobDescription);
        sendResponse({jobDescription: jobDescription });
      } else {
        console.error('Job description element not found.');
        sendResponse({ jobDescription: '' });
      }
    }
  });
  