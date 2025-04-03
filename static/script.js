document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file-input');
    const fileNameDisplay = document.getElementById('file-name');
    const uploadForm = document.getElementById('upload-form');
    const loader = document.getElementById('loader');
    
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                fileNameDisplay.textContent = 'Selected: ' + this.files[0].name;
                fileNameDisplay.style.display = 'block';
            } else {
                fileNameDisplay.style.display = 'none';
            }
        });
    }
    
    if (uploadForm) {
        uploadForm.addEventListener('submit', function() {
            if (fileInput.files.length > 0) {
                loader.style.display = 'block';
            }
        });
    }
});

// Drag and drop functionality
function handleDragOver(evt) {
    evt.preventDefault();
    evt.stopPropagation();
    document.querySelector('.upload-area').classList.add('dragover');
}

function handleDragLeave(evt) {
    evt.preventDefault();
    evt.stopPropagation();
    document.querySelector('.upload-area').classList.remove('dragover');
}

function handleDrop(evt) {
    evt.preventDefault();
    evt.stopPropagation();
    document.querySelector('.upload-area').classList.remove('dragover');
    
    const dt = evt.dataTransfer;
    const files = dt.files;
    
    document.querySelector('#file-input').files = files;
    
    if (files.length > 0) {
        document.querySelector('#file-name').textContent = 'Selected: ' + files[0].name;
        document.querySelector('#file-name').style.display = 'block';
    }
}
