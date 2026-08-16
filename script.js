// DOM Elements
const fileInput = document.getElementById('file-input');
const browseBtn = document.getElementById('browse-btn');
const dropZone = document.getElementById('drop-zone');
const resumeInput = document.getElementById('resume-input');
const generateBtn = document.getElementById('generate-btn');
const btnText = document.querySelector('.btn-text');
const loader = document.querySelector('.loader');
const errorMsg = document.getElementById('error-message');
const emptyState = document.querySelector('.empty-state');
const iframe = document.getElementById('portfolio-frame');
const statusBadge = document.querySelector('.status-badge');

// File Upload Handling
browseBtn.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', handleFileSelect);

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('drag-over');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    if (e.dataTransfer.files.length) {
        fileInput.files = e.dataTransfer.files;
        handleFileSelect();
    }
});

function handleFileSelect() {
    const file = fileInput.files[0];
    if (!file) return;
    
    if (file.name.endsWith('.txt')) {
        const reader = new FileReader();
        reader.onload = (e) => {
            resumeInput.value = e.target.result;
            validateInput();
        };
        reader.readAsText(file);
    } else {
        showError("Please upload a .txt file.");
    }
}

// Input Validation
resumeInput.addEventListener('input', validateInput);

function validateInput() {
    if (resumeInput.value.trim().length > 50) {
        generateBtn.disabled = false;
        statusBadge.textContent = "Ready to Sculpt";
        statusBadge.style.color = "var(--gold-primary)";
        statusBadge.style.borderColor = "var(--gold-primary)";
    } else {
        generateBtn.disabled = true;
        statusBadge.textContent = "Awaiting Data";
        statusBadge.style.color = "var(--text-muted)";
        statusBadge.style.borderColor = "var(--border-color)";
    }
}

// Generate Portfolio
generateBtn.addEventListener('click', async () => {
    const prompt = resumeInput.value.trim();
    if (!prompt) return;

    // UI Loading State
    generateBtn.disabled = true;
    btnText.hidden = true;
    loader.hidden = false;
    errorMsg.hidden = true;
    emptyState.querySelector('h3').textContent = "Sculpting Masterpiece...";
    emptyState.querySelector('p').textContent = "Please wait while our AI engine analyzes your data.";

    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "An error occurred during generation.");
        }

        // Success - Render the HTML in the iframe
        emptyState.hidden = true;
        iframe.hidden = false;
        
        // Write the returned HTML string into the iframe's document
        const iframeDoc = iframe.contentWindow.document;
        iframeDoc.open();
        iframeDoc.write(data.html);
        iframeDoc.close();

    } catch (error) {
        showError(error.message);
        emptyState.querySelector('h3').textContent = "Generation Failed";
        emptyState.querySelector('p').textContent = "An error occurred. Please try again.";
    } finally {
        generateBtn.disabled = false;
        btnText.hidden = false;
        loader.hidden = true;
    }
});

function showError(msg) {
    errorMsg.textContent = msg;
    errorMsg.hidden = false;
    setTimeout(() => {
        errorMsg.hidden = true;
    }, 5000);
}
