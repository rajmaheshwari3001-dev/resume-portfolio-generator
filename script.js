// Magnetic Hover Effects (Simplified without cursor tracking)
const magnetics = document.querySelectorAll('.magnetic');
magnetics.forEach(magnetic => {
    magnetic.addEventListener('mousemove', (e) => {
        const position = magnetic.getBoundingClientRect();
        const x = e.pageX - position.left - position.width / 2;
        const y = e.pageY - position.top - position.height / 2;
        
        magnetic.style.transform = `translate(${x * 0.3}px, ${y * 0.5}px)`;
    });

    magnetic.addEventListener('mouseleave', () => {
        magnetic.style.transform = 'translate(0px, 0px)';
    });
});

// --- Initial GSAP Animations ---
gsap.from(".navbar", { y: -50, opacity: 0, duration: 1, ease: "power3.out" });
gsap.from(".input-section", { x: -50, opacity: 0, duration: 1, delay: 0.2, ease: "power3.out" });
gsap.from(".preview-section", { x: 50, opacity: 0, duration: 1, delay: 0.4, ease: "power3.out" });

// --- App Logic ---
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
const downloadBtn = document.getElementById('download-btn');
const statusBadgeText = document.querySelector('.status-indicator').lastChild;
const pulseDot = document.querySelector('.dot');
const themeCards = document.querySelectorAll('.theme-card');
const swatches = document.querySelectorAll('.swatch');

let selectedThemeColor = '#6366F1'; // Default Indigo
let selectedTheme = 'standard'; // Default Theme
let generatedHtml = '';

// Theme Card Selection
themeCards.forEach(card => {
    card.addEventListener('click', () => {
        themeCards.forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        selectedTheme = card.getAttribute('data-theme');
    });
});

// Theme Color Selection
swatches.forEach(swatch => {
    swatch.addEventListener('click', () => {
        swatches.forEach(s => s.classList.remove('active'));
        swatch.classList.add('active');
        selectedThemeColor = swatch.getAttribute('data-color');
    });
});

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
        showError("Please provide a .txt file.");
    }
}

// Input Validation
resumeInput.addEventListener('input', validateInput);

function validateInput() {
    const text = resumeInput.value.trim();
    
    if (text.length > 0) {
        generateBtn.disabled = false;
        statusBadgeText.textContent = " Ready to Generate";
        pulseDot.classList.add('active');
        
        // GSAP pulse
        gsap.to(generateBtn, {
            scale: 1.02, duration: 0.3, yoyo: true, repeat: 1
        });
    } else {
        generateBtn.disabled = true;
        statusBadgeText.textContent = ` Awaiting Input`;
        pulseDot.classList.remove('active');
    }
}

// Generate Portfolio
generateBtn.addEventListener('click', async () => {
    const prompt = resumeInput.value.trim();
    
    if (!prompt) {
        showError("Please provide some resume text.");
        return;
    }

    // UI Loading State
    generateBtn.disabled = true;
    btnText.hidden = true;
    loader.hidden = false;
    errorMsg.hidden = true;
    emptyState.hidden = false;
    
    emptyState.querySelector('h3').textContent = "Generating...";
    emptyState.querySelector('p').textContent = "Building your portfolio.";
    iframe.hidden = true;
    downloadBtn.hidden = true;
    pulseDot.style.animationDuration = "0.5s";

    const templateStyle = selectedTheme;

    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                prompt,
                template: templateStyle,
                theme_color: selectedThemeColor
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Generation failed.");
        }

        generatedHtml = data.html;

        // Success Animation
        gsap.to(emptyState, { opacity: 0, duration: 0.2, onComplete: () => {
            emptyState.hidden = true;
            iframe.hidden = false;
            downloadBtn.hidden = false;
            
            // Write HTML
            const iframeDoc = iframe.contentWindow.document;
            iframeDoc.open();
            iframeDoc.write(generatedHtml);
            iframeDoc.close();
            
            gsap.from(iframe, { opacity: 0, y: 10, duration: 0.4 });
            gsap.from(downloadBtn, { opacity: 0, scale: 0.9, duration: 0.3 });
        }});

    } catch (error) {
        showError(error.message);
        emptyState.hidden = false;
        emptyState.querySelector('h3').textContent = "Generation Error";
        emptyState.querySelector('p').textContent = "Please verify your input.";
        iframe.hidden = true;
    } finally {
        generateBtn.disabled = false;
        btnText.hidden = false;
        loader.hidden = true;
        pulseDot.style.animationDuration = "2s";
    }
});

// Download Logic
downloadBtn.addEventListener('click', () => {
    if (!generatedHtml) return;
    
    // Magnetic click effect
    gsap.to(downloadBtn, { scale: 0.9, duration: 0.1, yoyo: true, repeat: 1 });

    const blob = new Blob([generatedHtml], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = 'portfolio.html';
    document.body.appendChild(a);
    a.click();
    
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
});

function showError(msg) {
    errorMsg.textContent = msg;
    errorMsg.hidden = false;
    gsap.from(errorMsg, { opacity: 0, y: 10, duration: 0.3 });
    setTimeout(() => {
        gsap.to(errorMsg, { opacity: 0, duration: 0.3, onComplete: () => errorMsg.hidden = true });
    }, 5000);
}
