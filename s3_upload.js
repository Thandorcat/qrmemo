const BUCKET_NAME = 'target-bucket-test-123';
const URL = "https://ollyljxpaeurqum3u3qtahhgaa0tsegp.lambda-url.us-east-1.on.aws/";

const form = document.getElementById('upload-form');
const fileInput = document.getElementById('file-input');
const progress = document.getElementById('progress');
const showForm = document.getElementById('download-form');
const fileNameInput = document.getElementById('file-download');
const imgPreview = document.getElementById('imgPreview');

form.addEventListener('submit', (e) => {
    e.preventDefault();

    console.log("Function works!");

    const file = fileInput.files[0];
    if (!file) {
        alert('Please select a file to upload.');
        return;
    }

    // Step 1: Get the presigned URL
    axios
        .post(URL, {
            type: "PUT",
            fileName: file.name
        })
        .then((presignedResponse) => {
            const presignedUrl = presignedResponse.data; // Assuming the response contains the URL
            console.log(presignedUrl);

            // Step 2: Upload the file using the presigned URL
            axios
                .put(presignedUrl, file, {
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
                .then((response) => {
                    if (response.status === 200) {
                        alert('File uploaded successfully!');
                        fileNameInput.value = file.name
                    } else {
                        alert('File upload failed.');
                    }
                })
                .catch((error) => {
                    console.error('Error during file upload:', error);
                    alert('File upload failed.');
                });
        })
        .catch((error) => {
            console.error('Error while obtaining the presigned URL:', error);
            alert('File upload failed.');
        });
});

// showForm.addEventListener('submit', showHandler)

async function showHandler() {

    console.log("Show function works!");
    const filename = fileNameInput.value;
    console.log(filename);

    let responce = await axios.post(
        URL, {
            type: "GET",
            fileName: filename
        }
    );

    console.log(responce);
    let getURL = responce.data
    console.log(getURL);
    imgPreview.src = getURL
    alert('Finished!');
}