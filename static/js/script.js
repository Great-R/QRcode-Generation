// Execute when page is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const qrForm = document.getElementById('qr-form');
    const contentInput = document.getElementById('content');
    const charCount = document.getElementById('char-count');
    const sizeSlider = document.getElementById('size');
    const sizeValue = document.getElementById('size-value');
    const qrImage = document.getElementById('qr-image');
    const qrContainer = document.getElementById('qr-container');
    const loadingSpinner = document.getElementById('loading-spinner');
    const downloadBtn = document.getElementById('download-btn');
    const shareBtn = document.getElementById('share-btn');
    const successAlert = document.getElementById('success-alert');
    const errorAlert = document.getElementById('error-alert');
    
    // Custom option elements
    const unitSizeSlider = document.getElementById('unit_size');
    const unitSizeValue = document.getElementById('unit-size-value');
    const marginSlider = document.getElementById('margin');
    const marginValue = document.getElementById('margin-value');
    const borderSizeSlider = document.getElementById('border_size');
    const borderSizeValue = document.getElementById('border-size-value');
    const frameCheckbox = document.getElementById('frame');
    const foregroundColorPicker = document.getElementById('foreground_color');
    const backgroundColorPicker = document.getElementById('background_color');
    
    // Current generated QR code URL
    let currentQrUrl = '';
    
    // QR code creation steps related variables
    let qrSteps = [];
    let currentStepIndex = 0;
    
    // Get modal elements
    const stepsModal = document.getElementById('steps-modal');
    const closeBtn = document.querySelector('.close');
    const prevStepBtn = document.getElementById('prev-step');
    const nextStepBtn = document.getElementById('next-step');
    const stepIndicator = document.getElementById('step-indicator');
    const stepImage = document.getElementById('step-image');
    const stepDescription = document.getElementById('step-description');
    const showStepsCheckbox = document.getElementById('show-steps');
    
    // Get GIF modal elements
    const gifModal = document.getElementById('gif-modal');
    let gifTimeoutId; // Used to store the ID of GIF auto-close timer
    
    let qrData = null; // Used to store generation results
    let generationComplete = false; // Flag indicating if generation is complete
    let currentFormData = null; // Used to store current form data
    
    // Update character count
    contentInput.addEventListener('input', function() {
        charCount.textContent = this.value.length;
    });
    
    // Update size display
    sizeSlider.addEventListener('input', function() {
        sizeValue.textContent = this.value;
        if (qrImage.src) {
            qrImage.style.width = this.value + 'px';
            qrImage.style.height = this.value + 'px';
        }
    });
    
    // Update unit size display
    unitSizeSlider.addEventListener('input', function() {
        unitSizeValue.textContent = this.value;
    });
    
    // Update margin display
    marginSlider.addEventListener('input', function() {
        marginValue.textContent = this.value;
    });
    
    // Update border width display
    borderSizeSlider.addEventListener('input', function() {
        borderSizeValue.textContent = this.value;
    });
    
    // Form submission handling
    qrForm.addEventListener('submit', function(e) {
        e.preventDefault();
        generateQRCode();
    });
    
    // Generate QR code
    function generateQRCode() {
        // Show loading animation
        qrImage.style.display = 'none';
        loadingSpinner.style.display = 'block';
        downloadBtn.style.display = 'none';
        shareBtn.style.display = 'none';
        hideAlerts();
        
        // Show GIF modal
        if (gifModal) {
            // Use class addition to show modal, triggering fade-in animation
            gifModal.classList.add('show');
            
            // Set timer to hide GIF modal after 5 seconds and show QR code (if generated)
            gifTimeoutId = setTimeout(() => {
                // Use class removal to hide modal, triggering fade-out animation
                gifModal.classList.remove('show');
                // If generation is complete and successful, show QR code
                if (generationComplete && qrData && qrData.success) {
                    displayQRCode(qrData, currentFormData);
                } else if (generationComplete && qrData && !qrData.success) {
                     // If generation failed, show error after timer ends
                     showErrorAlert(qrData.error || 'Error generating QR code, please try again.');
                } else if (generationComplete && !qrData) {
                     // If generation complete but no qrData (e.g. network error), show error
                     showErrorAlert('Network error, please check your connection and try again.');
                }
            }, 5000); // 5000 milliseconds = 5 seconds
        }
        
        // Get form data
        currentFormData = new FormData(qrForm);
        
        // Process checkbox values
        currentFormData.set('frame', frameCheckbox.checked);
        
        // Send request to backend
        fetch('/generate', {
            method: 'POST',
            body: currentFormData
        })
        .then(response => response.json())
        .then(data => {
            qrData = data; // Store generation result
            generationComplete = true; // Mark generation as complete
            
            // Hide loading animation (even if GIF modal is still showing)
            loadingSpinner.style.display = 'none';
            
            // If GIF modal is already hidden, show QR code directly
            if (gifModal && !gifModal.classList.contains('show')) {
                 if (qrData && qrData.success) {
                    displayQRCode(qrData, currentFormData);
                }
            } else if (!gifModal) { // If there's no GIF modal (fallback)
                if (qrData && qrData.success) {
                   displayQRCode(qrData, currentFormData);
               } else {
                   showErrorAlert(qrData.error || 'Error generating QR code, please try again.');
               }
            }
        })
        .catch(error => {
            generationComplete = true; // Mark generation as complete (even if failed)
            // Hide loading animation
            loadingSpinner.style.display = 'none';
            
            // If GIF modal is already hidden or doesn't exist, show error
            if ((gifModal && !gifModal.classList.contains('show')) || !gifModal) {
                 showErrorAlert('Network error, please check your connection and try again.');
                 console.error('Error:', error);
            }
        });
    }
    
    // New function to display QR code and related elements
    function displayQRCode(data, formData) {
        // Show generated QR code
        qrImage.src = data.image_base64;
        qrImage.style.width = sizeSlider.value + 'px';
        qrImage.style.height = sizeSlider.value + 'px';
        qrImage.style.display = 'block';
        qrImage.classList.add('fade-in');
        
        // Update version select box value
        const versionSelect = document.getElementById('version');
        versionSelect.value = data.version;
        
        // Save download URL
        currentQrUrl = data.image_url;
        
        // Show download and share buttons
        downloadBtn.href = data.image_url;
        downloadBtn.style.display = 'inline-block';
        shareBtn.style.display = 'inline-block';
        
        // Show success message
        showSuccessAlert();
        
        // If show steps is checked, get QR code creation steps
        if (showStepsCheckbox && showStepsCheckbox.checked) {
            // Pass formData to getQRSteps
            getQRSteps(
                formData.get('content'), 
                formData.get('ecl'),      
                formData.get('version')  
            );
        }
         // Show error message (if generation failed)
        if (!data.success) {
             showErrorAlert(data.error || 'Error generating QR code, please try again.');
        }
    }
    
    // Share button click event
    shareBtn.addEventListener('click', function() {
        // If browser supports Web Share API
        if (navigator.share) {
            navigator.share({
                title: 'My QR Code',
                text: 'Check out my generated QR code',
                url: window.location.origin + currentQrUrl
            })
            .catch(error => console.error('Share failed:', error));
        } else {
            // Copy link to clipboard
            const tempInput = document.createElement('input');
            document.body.appendChild(tempInput);
            tempInput.value = window.location.origin + currentQrUrl;
            tempInput.select();
            document.execCommand('copy');
            document.body.removeChild(tempInput);
            
            alert('Link copied to clipboard!');
        }
    });
    
    // Show success alert
    function showSuccessAlert() {
        successAlert.style.display = 'block';
        setTimeout(() => {
            successAlert.style.display = 'none';
        }, 3000);
    }
    
    // Show error alert
    function showErrorAlert(message) {
        errorAlert.textContent = message;
        errorAlert.style.display = 'block';
    }
    
    // Hide all alerts
    function hideAlerts() {
        successAlert.style.display = 'none';
        errorAlert.style.display = 'none';
    }
    
    // Close modal (add common close logic for all modals)
    document.querySelectorAll('.modal .close').forEach(btn => {
        btn.onclick = function() {
            // Use class removal to hide modal, triggering fade-out animation
            btn.closest('.modal').classList.remove('show');
            // If closing GIF modal, clear timer
            if (btn.closest('#gif-modal')) {
                 clearTimeout(gifTimeoutId);
            }
        }
    });
    
    // Close modal when clicking outside (add common external close logic for all modals)
    window.onclick = function(event) {
        // If clicking on steps modal background
        if (event.target == stepsModal && stepsModal.classList.contains('show')) {
            stepsModal.classList.remove('show');
        }
        // If clicking on GIF modal background
        if (event.target == gifModal && gifModal.classList.contains('show')) {
            gifModal.classList.remove('show');
            clearTimeout(gifTimeoutId); // Clear auto-close timer
            
            // If generation is complete and successful, show QR code immediately
            if (generationComplete && qrData && qrData.success) {
                 displayQRCode(qrData, currentFormData);
            } else if (generationComplete && qrData && !qrData.success) {
                 // If generation failed, show error after closing modal
                 showErrorAlert(qrData.error || 'Error generating QR code, please try again.');
            } else if (generationComplete && !qrData) {
                 // If generation complete but no qrData (e.g. network error), show error
                 showErrorAlert('Network error, please check your connection and try again.');
            }
        }
    }
    
    // Show specific step
    function showStep(index) {
        if (qrSteps.length === 0) return;
        
        // Ensure index is within valid range
        if (index < 0) index = 0;
        if (index >= qrSteps.length) index = qrSteps.length - 1;
        
        currentStepIndex = index;
        
        // Update step indicator
        stepIndicator.textContent = `Step ${index + 1}/${qrSteps.length}`;
        
        // Update step image and description
        stepImage.src = qrSteps[index].image;
        stepDescription.innerHTML = qrSteps[index].description;
        
        // Update navigation button states
        prevStepBtn.disabled = index === 0;
        nextStepBtn.disabled = index === qrSteps.length - 1;
    }
    
    // Bind navigation button events
    if (prevStepBtn) {
        prevStepBtn.onclick = function() {
            showStep(currentStepIndex - 1);
        }
    }
    
    if (nextStepBtn) {
        nextStepBtn.onclick = function() {
            showStep(currentStepIndex + 1);
        }
    }
    
    // Get QR code creation steps
    function getQRSteps(content, ecl, version) {
        // Show loading
        document.getElementById('loading-spinner').style.display = 'block';
        
        // Prepare form data
        const formData = new FormData();
        formData.append('content', content);
        formData.append('ecl', ecl);
        formData.append('version', version);
        
        // Send request
        fetch('/get_qr_steps', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('loading-spinner').style.display = 'none';
            
            if (data.success) {
                qrSteps = data.steps;
                
                // Show modal and display first step
                stepsModal.classList.add('show');
                showStep(0);
                
                // Add step name mapping for clearer step names
                const stepTitles = [
                    "Step 1: Add Finder Patterns and Separator",
                    "Step 2: Add Alignment Patterns, Timing Patterns and Dark Module",
                    "Step 3: Fill Data",
                    "Step 4: Apply Best Mask",
                    "Step 5: Add Format and Version Information"
                ];
                
                // Update step titles
                for (let i = 0; i < qrSteps.length && i < stepTitles.length; i++) {
                    const descriptionHTML = qrSteps[i].description;
                    // Preserve original description text, only update title part
                    const updatedHTML = descriptionHTML.replace(/<h3>.*?<\/h3>/, `<h3>${stepTitles[i]}</h3>`);
                    qrSteps[i].description = updatedHTML;
                }
                
                // Re-display current step
                showStep(currentStepIndex);
            } else {
                alert('Failed to get QR code creation steps: ' + data.error);
            }
        })
        .catch(error => {
            document.getElementById('loading-spinner').style.display = 'none';
            alert('Error while getting QR code creation steps: ' + error);
        });
    }
});
