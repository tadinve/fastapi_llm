async function processText() {
    const inputText = document.getElementById('inputText').value;
  
    try {
      const response = await axios.post('/process', { text: inputText });
      document.getElementById('outputDuckDuckGo').value = response.data.duckduckgo_search;
      document.getElementById('outputUpperCase').value = response.data.upper_case;
      document.getElementById('outputLength').value = response.data.length;
    } catch (error) {
      console.error(error);
    }
  }
  
  