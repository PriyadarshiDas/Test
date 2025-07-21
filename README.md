<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>CyberDoc Analyzer 🤖</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="container">
    <div class="ai-header">
      <h1>🤖 CyberDoc Analyzer</h1>
      <p>Upload a document and let the AI agents scan it.</p>
    </div>

    <div class="upload-box glass">
      <div class="custom-file-upload">
        <label for="fileInput">
          <span>📂 Upload Document</span>
        </label>
        <input type="file" id="fileInput" accept=".pdf,.docx" />
        <div id="fileName">No file chosen</div>
      </div>

      <button class="neon-button" onclick="uploadFile()">Analyze</button>
      <p class="note">Only PDF or DOCX files are supported</p>
    </div>

    <div id="buffer" class="buffer hidden">
      <div class="loader"></div>
      <p class="loading-text">Analyzing document... AI agents online...</p>
    </div>

    <div id="result" class="result-box hidden glass">
      <h2>📄 AI Output</h2>
      <div id="resultText" class="output-console"></div>
    </div>
  </div>
  <script src="app.js"></script>
</body>
</html>


scr

const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");

fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) {
    fileName.textContent = fileInput.files[0].name;
  } else {
    fileName.textContent = "No file chosen";
  }
});

async function uploadFile() {
  const buffer = document.getElementById('buffer');
  const result = document.getElementById('result');
  const resultText = document.getElementById('resultText');

  const file = fileInput.files[0];
  if (!file) {
    alert("Please select a file.");
    return;
  }

  const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
  if (!allowedTypes.includes(file.type)) {
    alert("Only PDF and DOCX files are supported.");
    return;
  }

  result.classList.add("hidden");
  buffer.classList.remove("hidden");

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error("Server returned an error");
    }

    const data = await response.json();
    buffer.classList.add("hidden");
    resultText.textContent = JSON.stringify(data, null, 2);
    result.classList.remove("hidden");
  } catch (err) {
    buffer.classList.add("hidden");
    alert("Error analyzing document. Check backend or try again.");
  }
}



body {
  margin: 0;
  background: linear-gradient(135deg, #0c002b, #1a103d);
  color: #fff;
  font-family: 'Segoe UI', sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  overflow-x: hidden;
}

.container {
  width: 90%;
  max-width: 600px;
  text-align: center;
}

.ai-header h1 {
  font-size: 2.5em;
  background: linear-gradient(to right, #00f2fe, #4facfe);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 15px #00ffff99;
}

.ai-header p {
  color: #bbb;
  margin-bottom: 30px;
}

.glass {
  background: rgba(255, 255, 255, 0.05);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.3);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 30px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.custom-file-upload {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px dashed #0ff;
  border-radius: 15px;
  padding: 25px;
  margin-bottom: 20px;
  background: rgba(255, 255, 255, 0.03);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
  cursor: pointer;
  transition: 0.3s ease;
}

.custom-file-upload label {
  display: inline-block;
  color: #0ff;
  padding: 10px 20px;
  font-weight: bold;
  border: 2px solid #0ff;
  border-radius: 25px;
  transition: all 0.3s ease;
  box-shadow: 0 0 10px #0ff;
  cursor: pointer;
  margin-bottom: 10px;
  text-transform: uppercase;
}

.custom-file-upload label:hover {
  background-color: #0ff;
  color: black;
  box-shadow: 0 0 20px #00ffff, 0 0 40px #00ffff;
}

.custom-file-upload input[type="file"] {
  display: none;
}

#fileName {
  color: #ccc;
  font-size: 0.9rem;
  font-style: italic;
}

.neon-button {
  background: #0ff;
  border: none;
  color: black;
  font-weight: bold;
  padding: 15px 30px;
  font-size: 1rem;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 0 20px #0ff;
}

.neon-button:hover {
  background: #00ffff;
  box-shadow: 0 0 40px #00ffff, 0 0 80px #00ffff;
  transform: scale(1.05);
}

.note {
  font-size: 0.8rem;
  color: #999;
  margin-top: 10px;
}

.buffer {
  margin-top: 30px;
  padding: 20px;
}

.buffer .loader {
  width: 60px;
  height: 60px;
  border: 6px solid #00ffff;
  border-top: 6px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: auto;
}

.loading-text {
  margin-top: 15px;
  color: #00ffff;
  font-style: italic;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.result-box {
  margin-top: 30px;
  text-align: left;
  border: 1px solid rgba(0, 255, 255, 0.2);
  background: rgba(0, 255, 255, 0.02);
  max-height: 400px;
  overflow-y: auto;
  padding: 20px;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.result-box h2 {
  margin-top: 0;
  color: #0ff;
  text-shadow: 0 0 10px #0ff;
}

.output-console {
  white-space: pre-wrap;
  font-size: 0.9rem;
  line-height: 1.5;
  background: rgba(0, 0, 0, 0.3);
  padding: 15px;
  border-radius: 10px;
  color: #0ff;
  border: 1px solid rgba(0, 255, 255, 0.1);
  box-shadow: inset 0 0 10px rgba(0, 255, 255, 0.15);
}

.hidden {
  display: none;
}
