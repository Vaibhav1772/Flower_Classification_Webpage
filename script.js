//JAVASCRIPT CODE FOR TAKING AND POSTING TO BACKEND
const fileUploadInput = document.getElementById('upload-input');
const fileUpload = document.getElementById('file-upload');
const imagePreview = document.getElementById('image-preview');
const uploadedImage = document.getElementById('uploaded-image');
const progressBarContainer = document.getElementById('progress-bar-container');
const progressBar = document.getElementById('progress-bar');
const progressText = document.getElementById('progress-text');
var uploadButton = document.getElementById('submit');
var fileInput = document.getElementById('upload-input');

var outputContainer = document.getElementById('output-container');
var outputLabel = document.getElementById('output-label');
var outputImage = document.getElementById('output-image');
const resultContainer = document.getElementById('result-container');

fileUploadInput.addEventListener('change', () => {
    const file = fileUploadInput.files[0];
    if (file) {
        fileUpload.style.display = 'none';
        imagePreview.style.display = 'block';

        progressBarContainer.style.display = 'block';

        let progress = 0;
        const interval = setInterval(() => {
            progress += 1;
            progressBar.style.width = `${progress}%`;
            progressText.innerText = `${progress}%`;
            uploadButton.disabled = true;
            if (progress >= 100) {
                clearInterval(interval);
                uploadButton.disabled = false;
            }
        }, 30);

        let opacity = 0;
        const imageInterval = setInterval(() => {
            opacity += 0.01;
            uploadedImage.style.opacity = opacity;
            if (opacity >= 1) {
                clearInterval(imageInterval);
            }
        }, 30);

        uploadedImage.src = URL.createObjectURL(file);

    }
});

uploadButton.addEventListener('click', function () {
    resultContainer.style.display = 'none';

    var formData = new FormData();
    formData.append('file', fileInput.files[0]);

    var reader = new FileReader();
    reader.onload = function (e) {
        document.getElementById('return-image').src = e.target.result;
    };
    reader.readAsDataURL(fileInput.files[0]);

    // Send the image file to the backend
    fetch('https://main--flowerclassifier.netlify.app/predict', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            // Display the result from the backend
            var detailsContainer = document.getElementById('output-container');
            overlay.style.display = 'block';
            detailsContainer.innerHTML = `
            <h2 style="text-transform: uppercase">${data.predicted_class}</h2>
            <p ><strong>Confidence:</strong> ${data.Confidence}<span>%</span></p>
            <p><strong>Scientific Name:</strong> ${data.details.scientific_name}</p>
            <p><strong>Description:</strong> ${data.details.description}</p>
            <p><strong>Habitat:</strong> ${data.details.habitat}</p>
            <p><strong>Symbolism:</strong> ${data.details.uses}</p>
        `;
            outputContainer.style.display = 'block';
            outputImage.src = data.result_image_url;
            outputLabel.textContent = data.result_label;
            // Call resetForm() after fetch request is completed
            resetForm();
        });
});


overlay.addEventListener('click', function () {
    overlay.style.display = 'none';
});


function resetForm() {
    // Reset the file input and uploaded image
    document.getElementById("upload-input").value = "";
    document.getElementById("uploaded-image").src = "";

    // Show the file upload form and hide the image preview
    document.getElementById("file-upload").style.display = "block";
    document.getElementById("image-preview").style.display = "none";

    // Reset the progress bar
    document.getElementById("progress-bar-container").style.display = "none";
    document.getElementById("progress-bar").style.width = "0%";
    document.getElementById("progress-text").innerText = "0%";

    // Clear any previous results
    document.getElementById("result-container").style.display = "none";
    document.getElementById("result-label").textContent = "";
    document.getElementById("result-image").src = "";
}

