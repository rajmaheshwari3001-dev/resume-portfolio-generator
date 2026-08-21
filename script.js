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
const validationModal = document.getElementById('validation-modal');
const cancelGenerateBtn = document.getElementById('cancel-generate-btn');
const proceedGenerateBtn = document.getElementById('proceed-generate-btn');
const validationMsg = document.getElementById('validation-msg');

let selectedThemeColor = '#3b82f6'; // Default Blue
let selectedTheme = 'standard'; // Default Theme
let generatedHtml = '';

// Theme Card Selection
themeCards.forEach(card => {
    card.addEventListener('click', () => {
        themeCards.forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        selectedTheme = card.getAttribute('data-theme');
        
        // INSTANTLY update theme without calling API if iframe is loaded
        if (iframe && !iframe.hidden && generatedHtml) {
            iframe.contentWindow.document.body.className = 'template-' + selectedTheme;
        }
    });
});

// Theme Color Selection
swatches.forEach(swatch => {
    swatch.addEventListener('click', () => {
        swatches.forEach(s => s.classList.remove('active'));
        swatch.classList.add('active');
        selectedThemeColor = swatch.getAttribute('data-color');
        
        // INSTANTLY update color without calling API
        if (iframe && !iframe.hidden && generatedHtml) {
            const hex = selectedThemeColor.replace('#', '');
            const r = parseInt(hex.substring(0,2), 16);
            const g = parseInt(hex.substring(2,4), 16);
            const b = parseInt(hex.substring(4,6), 16);
            const root = iframe.contentWindow.document.documentElement;
            root.style.setProperty('--accent-color', selectedThemeColor, 'important');
            root.style.setProperty('--accent', selectedThemeColor, 'important');
            root.style.setProperty('--accent-color-rgb', \, \, \, 'important');
        }
    });
});

// File Upload Handling
dropZone.addEventListener('click', () => fileInput.click());
browseBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    fileInput.click();
});

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        handleFileSelect(fileInput.files[0]);
    }
});

dropZone.addEventListener('dragenter', (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove('drag-over');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove('drag-over');
    if (e.dataTransfer && e.dataTransfer.files.length > 0) {
        handleFileSelect(e.dataTransfer.files[0]);
    }
});

function handleFileSelect(file) {
    if (!file) return;
    
    if (file.name.toLowerCase().endsWith('.txt')) {
        const reader = new FileReader();
        reader.onload = (e) => {
            resumeInput.value = e.target.result;
            validateInput();
            
            // Upload success flash
            gsap.fromTo(resumeInput, 
                { backgroundColor: 'rgba(16, 185, 129, 0.2)' },
                { backgroundColor: 'transparent', duration: 1 }
            );
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
    const words = text.split(/\s+/).filter(w => w.length > 0);

    if (words.length >= 10) {
        generateBtn.disabled = false;
        btnText.textContent = "Generate Portfolio";
        statusBadgeText.textContent = " Ready to Generate";
        pulseDot.classList.add('active');
        pulseDot.style.backgroundColor = '#10b981'; // Green
        
        // GSAP pulse
        gsap.to(generateBtn, {
            scale: 1.02, duration: 0.3, yoyo: true, repeat: 1
        });
    } else if (words.length > 0) {
        generateBtn.disabled = false; // Actually keep it disabled until 10 words, or let the modal handle it
        btnText.textContent = "Needs More Detail";
        statusBadgeText.textContent = " Needs More Detail";
        pulseDot.classList.add('active');
        pulseDot.style.backgroundColor = '#f59e0b'; // Amber/Warning
    } else {
        generateBtn.disabled = true;
        btnText.textContent = "Paste Resume to Start";
        statusBadgeText.textContent = ` Awaiting Input`;
        pulseDot.classList.remove('active');
        pulseDot.style.backgroundColor = '';
    }
}

// Generate Portfolio Logic
generateBtn.addEventListener('click', async () => {
    const text = resumeInput.value.trim();
    
    if (!text) {
        showError("Please provide some resume text.");
        return;
    }

    const words = text.split(/\s+/).filter(w => w.length > 0);
    const lowerText = text.toLowerCase();
    
    // Strict Validation Intercept
    let isValid = true;
    let errorMsg = "";

    const hasSkills = lowerText.includes('skill');
    const hasNameOrContact = text.includes('@') || /[0-9]{7,}/.test(text) || lowerText.includes('name');

    if (words.length < 10) {
        isValid = false;
        errorMsg = "Your input is too short. Please provide at least 10 words.";
    } else if (!hasSkills || !hasNameOrContact) {
        isValid = false;
        errorMsg = "Strict Validation Failed: Your resume MUST contain a 'Skills' section and basic contact information (Email/Phone) or 'Name' before generating.";
    } else if (
        !lowerText.includes('experience') && 
        !lowerText.includes('education') && 
        !lowerText.includes('work') &&
        !lowerText.includes('degree') &&
        !lowerText.includes('project')
    ) {
        isValid = false;
        errorMsg = "Your text does not look like a complete resume. It must contain experience, education, or projects to generate a valid portfolio without hallucinating.";
    }

    if (!isValid) {
        validationMsg.textContent = errorMsg;
        if (!hasSkills || !hasNameOrContact) {
            proceedGenerateBtn.style.display = 'none'; // Mandatory fields missing
        } else {
            proceedGenerateBtn.style.display = 'inline-block';
        }
        validationModal.hidden = false;
        return; // Hard block, do not generate
    }
    
    doGenerate();
});

cancelGenerateBtn.addEventListener('click', () => {
    validationModal.hidden = true;
});

proceedGenerateBtn.addEventListener('click', () => {
    validationModal.hidden = true;
    doGenerate();
});

// Handles the core API request and updates the UI state during generation
async function doGenerate() {
    const prompt = resumeInput.value.trim();

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
            
            // Auto-scroll on mobile
            if (window.innerWidth < 1024) {
                document.getElementById('preview-section').scrollIntoView({ behavior: 'smooth' });
            }
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
}

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
