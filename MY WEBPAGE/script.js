//JAVASCRIPT CODE FOR TAKING AND POSTING TO BACKEND

var progressBar = document.getElementById('progress-bar');
var uploadButton = document.getElementById('submit');
var fileInput = document.getElementById('upload-input');
var resultContainer = document.getElementById('result-container');
var resultImage = document.getElementById('result-image');
var resultLabel = document.getElementById('result-label');
var overlay = document.getElementById('overlay');
var uploadedImage = document.getElementById('uploaded-image');
var outputContainer = document.getElementById('output-container');
var outputLabel = document.getElementById('output-label');
var outputImage = document.getElementById('output-image');
var previewImage = document.getElementById('preview-image');
uploadButton.addEventListener('click', function () {
    progressBar.style.width = '0%';
    resultContainer.style.display = 'none';

    var formData = new FormData();
    formData.append('file', fileInput.files[0]);


    var reader = new FileReader();
    reader.onload = function (e) {
        uploadedImage.src = e.target.result;
    };
    reader.readAsDataURL(fileInput.files[0]);


    // Send the image file to the backend
    fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            progressBar.style.width = '100%';

            // Display the result from the backend
            resultContainer.style.display = 'block';
            resultImage.src = data.result_image_url;
            resultLabel.textContent = data.result_label;
            var detailsContainer = document.getElementById('output-container');
            detailsContainer.innerHTML = '';


            // Display the overlay
            overlay.style.display = 'block';
            for (var key in data) {
                if (key !== 'result_image_url' && key !== 'result_label') {
                    var detail = document.createElement('p');
                    detail.textContent = key + ': ' + data[key];
                    detailsContainer.appendChild(detail);
                    detail.setAttribute('id', 'predict')

                }
            }
            outputContainer.style.display = 'block';
            outputImage.src = data.result_image_url;
            outputLabel.textContent = data.result_label;

        })

});
overlay.addEventListener('click', function () {
    overlay.style.display = 'none';
});
