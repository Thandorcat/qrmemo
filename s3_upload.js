const backendURL = "https://r627yqhmtpvupwc5wvr73tmv6a0sfzyj.lambda-url.us-east-1.on.aws/";

const form = document.getElementById('upload-form');
const fileInput = document.getElementById('file-input');
const progress = document.getElementById('progress');
const showForm = document.getElementById('download-form');
const fileNameInput = document.getElementById('file-download');
const imgPreview = document.getElementById('imgPreview');

var uploadURL = "";

document.addEventListener('DOMContentLoaded', () => {
    checkPhotoExistence();
});

async function checkPhotoExistence() {
    try {

        // Get the current URL
        const currentUrl = window.location.href;
        // Create a URLSearchParams object from the current URL
        const urlParams = new URLSearchParams(new URL(currentUrl).search);
        // Get a specific parameter by name, for example, 'photoId'
        if (urlParams.toString() == '') {
            alert("No parameters provided!");
        }
        const provided_token = urlParams.get('tk');
        const provided_secret = urlParams.get('s');
        
        let response = await axios.post(
            backendURL, {
                token: provided_token,
                secret: provided_secret
            }
        );
        console.log(response);

        if (response.status != 200) {
            console.log("Failed request to backend!");
            alert(response.body);
            return;
        }
        console.log(response.data);
        const presignedUrl = response.data.url;

        if (response.data.existing_file) {
            // If the photo exists, display it
            console.log("File exists!");
            console.log(presignedUrl);
            imgPreview.src = presignedUrl;
            form.style.display = 'none';
        } else {
            // If the photo does not exist, show the upload form
            console.log("New upload!");
            console.log(presignedUrl);

            uploadURL = presignedUrl;

            imgPreview.style.display = 'none';
        }
    } catch (error) {
        console.error('Error checking photo existence:', error);
    }
}

async function uploadFile() {
    console.log("Upload URL is: " + uploadURL);
    let response = await axios.put(presignedUrl, file, {
        headers: {
            'Content-Type': 'application/octet-stream',
        },
        onUploadProgress: (progressEvent) => {
            const loaded = progressEvent.loaded;
            const total = progressEvent.total;
            const percent = (loaded / total) * 100;
            progress.value = percent;
            console.log(`Upload progress: ${percent}%`);
        },
    })
    if (response.status === 200) {
        alert('File uploaded successfully!');
    } else {
        alert('File upload failed.');
    }
}

form.addEventListener('submit', () => {
    uploadFile();
});