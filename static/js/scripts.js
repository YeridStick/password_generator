document.addEventListener('DOMContentLoaded', function() {
    const passwordOutput = document.getElementById('password-output');
    const copyButton = document.getElementById('copy-button');
    const generateButton = document.getElementById('generate-button');
    const passwordLength = document.getElementById('password-length');
    const decreaseLength = document.getElementById('decrease-length');
    const increaseLength = document.getElementById('increase-length');
    
    const toggleCustomizeButton = document.getElementById('toggle-customize');
    const customizePanel = document.getElementById('customize-panel');
    const minLengthInput = document.getElementById('min-length');
    const minLengthDisplay = document.getElementById('min-length-display');
    const specialCharsInput = document.getElementById('special-chars');
    
    const reqLengthToggle = document.getElementById('req-length-toggle');
    const reqUppercaseToggle = document.getElementById('req-uppercase-toggle');
    const reqLowercaseToggle = document.getElementById('req-lowercase-toggle');
    const reqDigitToggle = document.getElementById('req-digit-toggle');
    const reqSpecialToggle = document.getElementById('req-special-toggle');
    const reqNoRepeatsToggle = document.getElementById('req-no-repeats-toggle');
    
    const reqLength = document.getElementById('req-length');
    const reqUppercase = document.getElementById('req-uppercase');
    const reqLowercase = document.getElementById('req-lowercase');
    const reqDigit = document.getElementById('req-digit');
    const reqSpecial = document.getElementById('req-special');
    const reqNoRepeats = document.getElementById('req-no-repeats');
    
    toggleCustomizeButton.addEventListener('click', function() {
        customizePanel.classList.toggle('hidden');
        
        if (customizePanel.classList.contains('hidden')) {
            toggleCustomizeButton.innerHTML = '<i class="fas fa-sliders-h"></i> Personalizar requisitos';
        } else {
            toggleCustomizeButton.innerHTML = '<i class="fas fa-times"></i> Cerrar panel';
        }
    });
    
    minLengthInput.addEventListener('change', function() {
        const value = parseInt(minLengthInput.value);
        if (isNaN(value) || value < 4) {
            minLengthInput.value = 4;
        } else if (value > 64) {
            minLengthInput.value = 64;
        }
        
        minLengthDisplay.textContent = minLengthInput.value;
        
        if (parseInt(passwordLength.value) < parseInt(minLengthInput.value)) {
            passwordLength.value = minLengthInput.value;
        }
    });
    
    function updateRequirementDisplay() {
        reqLength.classList.toggle('disabled', !reqLengthToggle.checked);
        reqUppercase.classList.toggle('disabled', !reqUppercaseToggle.checked);
        reqLowercase.classList.toggle('disabled', !reqLowercaseToggle.checked);
        reqDigit.classList.toggle('disabled', !reqDigitToggle.checked);
        reqSpecial.classList.toggle('disabled', !reqSpecialToggle.checked);
        reqNoRepeats.classList.toggle('disabled', !reqNoRepeatsToggle.checked);
    }
    
    reqLengthToggle.addEventListener('change', updateRequirementDisplay);
    reqUppercaseToggle.addEventListener('change', updateRequirementDisplay);
    reqLowercaseToggle.addEventListener('change', updateRequirementDisplay);
    reqDigitToggle.addEventListener('change', updateRequirementDisplay);
    reqSpecialToggle.addEventListener('change', updateRequirementDisplay);
    reqNoRepeatsToggle.addEventListener('change', updateRequirementDisplay);
    
    function resetValidation() {
        [reqLength, reqUppercase, reqLowercase, reqDigit, reqSpecial, reqNoRepeats].forEach(el => {
            el.classList.remove('valid');
        });
    }
    
    function updateValidation(validation) {
        resetValidation();
        
        if (validation.has_minimum_length) reqLength.classList.add('valid');
        if (validation.has_uppercase) reqUppercase.classList.add('valid');
        if (validation.has_lowercase) reqLowercase.classList.add('valid');
        if (validation.has_digit) reqDigit.classList.add('valid');
        if (validation.has_special_char) reqSpecial.classList.add('valid');
        if (validation.has_no_repeats) reqNoRepeats.classList.add('valid');
    }
    
    decreaseLength.addEventListener('click', function() {
        let currentLength = parseInt(passwordLength.value);
        let minLength = parseInt(minLengthInput.value);
        
        if (currentLength > minLength) {
            passwordLength.value = currentLength - 1;
        }
    });
    
    increaseLength.addEventListener('click', function() {
        let currentLength = parseInt(passwordLength.value);
        passwordLength.value = currentLength + 1;
    });
    
    passwordLength.addEventListener('change', function() {
        let length = parseInt(passwordLength.value);
        let minLength = parseInt(minLengthInput.value);
        
        if (isNaN(length) || length < minLength) {
            passwordLength.value = minLength;
        }
    });
    
    generateButton.addEventListener('click', function() {
        const length = parseInt(passwordLength.value);
        
        passwordOutput.value = "Generando...";
        generateButton.disabled = true;
        
        const requirements = {
            length: length,
            min_length: parseInt(minLengthInput.value),
            require_uppercase: reqUppercaseToggle.checked,
            require_lowercase: reqLowercaseToggle.checked,
            require_digit: reqDigitToggle.checked,
            require_special: reqSpecialToggle.checked,
            special_chars: specialCharsInput.value,
            no_repeats: reqNoRepeatsToggle.checked
        };
        
        fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requirements),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }
            return response.json();
        })
        .then(data => {
            passwordOutput.value = data.password;
            
            updateValidation(data.validation);
            
            generateButton.classList.add('success');
            setTimeout(() => {
                generateButton.classList.remove('success');
            }, 1000);
        })
        .catch(error => {
            console.error('Error:', error);
            passwordOutput.value = "Error al generar contraseña";
        })
        .finally(() => {
            generateButton.disabled = false;
        });
    });
    
    copyButton.addEventListener('click', function() {
        if (!passwordOutput.value) return;
        
        passwordOutput.select();
        document.execCommand('copy');
        
        const originalIcon = copyButton.innerHTML;
        copyButton.innerHTML = '<i class="fas fa-check"></i>';
        
        setTimeout(() => {
            copyButton.innerHTML = originalIcon;
        }, 1500);
        
        window.getSelection().removeAllRanges();
    });
    
    updateRequirementDisplay();
    
    generateButton.click();
});