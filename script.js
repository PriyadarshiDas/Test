async function uploadFile() {
  const fileInput = document.getElementById('fileInput');
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

  // Hide result and show buffer screen
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
      throw new Error("Server returned error");
    }

    const data = await response.json();

    buffer.classList.add("hidden");
    resultText.textContent = JSON.stringify(data, null, 2);
    result.classList.remove("hidden");
  } catch (err) {
    buffer.classList.add("hidden");
    alert("Error analyzing document. Please check the backend and try again.");
  }
}
