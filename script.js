// static/script.js
document.getElementById("fileForm").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent the form from submitting normally

    let formData = new FormData();
    formData.append("file", document.getElementById("file").files[0]);

    // Hide any previous errors and results
    document.getElementById('error').style.display = 'none';  // Hide any previous error messages
    document.getElementById('fileLink').style.display = 'none';  // Hide the previous file download link

    // Perform the file upload with Fetch API
    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.file_url) {
            // If the file was uploaded successfully
            document.getElementById("fileLink").style.display = "block";
            document.getElementById("downloadLink").href = data.file_url;
            document.getElementById("downloadLink").innerText = "Click to download the file";
        } else {
            // Show any error messages returned by the server
            document.getElementById("error").innerText = "Error: " + (data.error || "Unknown error");
            document.getElementById("error").style.display = "block";
        }
    })
    .catch(error => {
        // Handle network or other errors
        document.getElementById("error").innerText = "Upload failed: " + error.message;
        document.getElementById("error").style.display = "block";
    });
});
