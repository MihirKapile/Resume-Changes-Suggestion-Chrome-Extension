document.getElementById('analyze').addEventListener('click', () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.tabs.sendMessage(tabs[0].id, { action: 'getJobDescription' }, (response) => {
        fetch('http://127.0.0.1:8000/analyze', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ description: response.jobDescription })
        })
        .then(response => response.json())
        .then(data => {
          const formattedSuggestions = data.suggestions
                    .replace(/\n/g, ' ')
                    .replace(/\s+/g, ' ') 
                    .trim();
          formattedSuggestions1 = formattedSuggestions
                    .replace(/\*\*/g, '<br>')
                    .replace(/\*/g, '');
          document.getElementById('suggestions').innerHTML = JSON.stringify(formattedSuggestions1, null, 4);
        });
      });
    });
  });
const submitBtn = document.getElementById('submitBtn');
const fileInput = document.getElementById('fileInput');
const statusMessage = document.getElementById('statusMessage');

submitBtn.addEventListener('click', async function() {
  const file = fileInput.files[0];
  if (!file) {
      statusMessage.textContent = 'Please select a file.';
      return;
  }

  if (file.type !== 'application/pdf') {
      statusMessage.textContent = 'Only PDF files are allowed.';
      return;
  }

  const formData = new FormData();
  formData.append('resume', file);

  try {
      const response = await fetch('http://127.0.0.1:8000/upload', {  // Adjust the URL as needed
          method: 'POST',
          body: formData
      });

      if (response.ok) {
          statusMessage.textContent = 'File uploaded successfully!';
      } else {
          statusMessage.textContent = 'Error uploading file.';
      }
  } catch (error) {
      statusMessage.textContent = 'Error: ' + error.message;
  }
});

  
  