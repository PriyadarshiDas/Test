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
