// Variables
const UploadUrl = "https://image-editor-api.vercel.app/upload";
const ResizeUrl = "https://image-editor-api.vercel.app/resize";
const fileTrigger = document.getElementById('file-select-div');
const fileInput = document.getElementById('fileInput');
const mainDiv = document.getElementById('main-div');
const progressDiv = document.getElementById('progress-div');
const progressBar = document.getElementById('progress-bar');
const fileNameH4 = document.getElementById('file-name-h4');
const fileSizeH4 = document.getElementById('file-size-h4');
const fileProgressH4 = document.getElementById('file-progress-h4');
const resizeDiv = document.getElementById('resize-div');
const widthInput = document.getElementById('widthInput');
const heightInput = document.getElementById('heightInput');
let height = 0;
let width = 0;
let fileHash = "";
const resizeButtonDiv = document.getElementById('resize-button-div');

// Event Listeners
fileTrigger.addEventListener('click', () => {
    fileInput.click();
});
fileInput.addEventListener('change', handleFileSelection);
heightInput.addEventListener('input', handleLargeSize);
widthInput.addEventListener('input', handleLargeSize);
resizeButtonDiv.addEventListener('click', handleResize);



// Functions
function FileUploader(file) {
    mainDiv.style.display = "none";
    progressDiv.style.display = "block";
    fileNameH4.innerHTML = file.name;
    fileProgressH4.innerHTML = "Uploading 0 %";

    if (file.size < 1024) {
        fileSizeH4.innerHTML = (file.size / (1024)).toFixed(1) + " KB";
    } else {
        fileSizeH4.innerHTML = (file.size / (1024 * 1024)).toFixed(1) + " MB";
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("Connection", "keep-alive");
    const xhr = new XMLHttpRequest();
    xhr.open("POST", UploadUrl, true);
    xhr.send(formData);

    // Handle Progress
    xhr.upload.onprogress = (e) => {
        const percentComplete = Math.round((e.loaded / e.total) * 100);
        progressBar.style.width = percentComplete + "%";
        fileProgressH4.innerHTML = `Uploading ${percentComplete} %`;
    }


    // Handle Errors
    xhr.onerror = (e) => {
        console.log("Error! Upload failed. Can't connect to server.");
        console.log(e);
        mainDiv.style.display = "block";
        progressDiv.style.display = "none";
        alert("Error! Upload failed. Can't connect to server.");
        return;
    };

    // Handle Completion
    xhr.onreadystatechange = function () {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            const res = xhr.responseText.split(";");
            console.log(res);
            fileHash = res[0];
            width = Number(res[1]);
            height = Number(res[2]);
            progressBar.style.width = "100%";
            fileProgressH4.innerHTML = "Uploaded 100 %";

            // Handle Resize
            resizeDiv.style.display = "block";
            progressDiv.style.display = "none";

            console.log(fileHash);
            console.log(width);
            console.log(height);



            widthInput.max = width;
            widthInput.value = width;
            heightInput.max = height;
            heightInput.value = height;
        };
    }
};



function handleFileSelection() {
    try {
        const file = fileInput.files[0];
        if (file) {
            if (file.size > 15.1 * 1024 * 1024) {
                alert("File size must be less than 15MB");
                return;
            }
            FileUploader(file);
        } else {
            alert("Select a File to upload!");
            return;
        }
    } catch (err) {
        alert(err);
        return;
    }
}

function handleLargeSize(e) {
    if (widthInput.value > width) {
        widthInput.value = width;
    }
    if (heightInput.value > height) {
        heightInput.value = height;
    }
}

async function handleResize() {
    const url = ResizeUrl + `?file=${fileHash}&width=${widthInput.value}&height=${heightInput.value}`;
    console.log(url);
    const response = await fetch(url)
    const data = await response.text();
    console.log(data);
}