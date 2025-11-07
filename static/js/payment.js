// payment.js - Validaciones y formateo para el formulario de pago

document.addEventListener('DOMContentLoaded', function() {
    const paymentForm = document.getElementById('payment-form');
    const cardNumberInput = document.getElementById('card_number');
    const cardNameInput = document.getElementById('card_name');
    const expiryDateInput = document.getElementById('expiry_date');
    const cvvInput = document.getElementById('cvv');
    const cardDetailsSection = document.getElementById('card-details');
    const paymentMethodInputs = document.querySelectorAll('input[name="payment_method"]');

    // Manejar cambio de método de pago
    paymentMethodInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.value === 'card') {
                cardDetailsSection.style.display = 'block';
                // Hacer campos requeridos
                cardNumberInput.required = true;
                cardNameInput.required = true;
                expiryDateInput.required = true;
                cvvInput.required = true;
            } else {
                cardDetailsSection.style.display = 'none';
                // Quitar requerido
                cardNumberInput.required = false;
                cardNameInput.required = false;
                expiryDateInput.required = false;
                cvvInput.required = false;
            }
        });
    });

    // Función para formatear el número de tarjeta (añadir espacios cada 4 dígitos)
    function formatCardNumber(value) {
        const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
        const matches = v.match(/\d{4,16}/g);
        const match = (matches && matches[0]) || '';
        const parts = [];

        for (let i = 0, len = match.length; i < len; i += 4) {
            parts.push(match.substring(i, i + 4));
        }

        if (parts.length) {
            return parts.join(' ');
        } else {
            return value;
        }
    }

    // Función para formatear la fecha de expiración (MM/AA)
    function formatExpiryDate(value) {
        const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
        
        if (v.length >= 2) {
            return v.substring(0, 2) + '/' + v.substring(2, 4);
        }
        
        return v;
    }

    // Función para validar la fecha de expiración
    function validateExpiryDate(expiry) {
        const parts = expiry.split('/');
        if (parts.length !== 2) return false;

        const month = parseInt(parts[0], 10);
        const year = parseInt('20' + parts[1], 10);

        if (month < 1 || month > 12) return false;

        const now = new Date();
        const currentYear = now.getFullYear();
        const currentMonth = now.getMonth() + 1;

        if (year < currentYear || (year === currentYear && month < currentMonth)) {
            return false;
        }

        return true;
    }

    // Función para mostrar error en un campo
    function showError(input, message) {
        input.classList.add('border-red-500');
        input.classList.remove('border-gray-700');
        
        // Eliminar mensaje de error previo si existe
        const existingError = input.parentElement.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }

        // Crear nuevo mensaje de error
        const errorDiv = document.createElement('p');
        errorDiv.className = 'error-message text-red-400 text-xs mt-1';
        errorDiv.textContent = message;
        
        // Insertar después del párrafo de ejemplo
        const exampleText = input.parentElement.querySelector('.text-gray-400');
        if (exampleText) {
            exampleText.insertAdjacentElement('afterend', errorDiv);
        } else {
            input.parentElement.appendChild(errorDiv);
        }
    }

    // Función para limpiar error de un campo
    function clearError(input) {
        input.classList.remove('border-red-500');
        input.classList.add('border-gray-700');
        
        const errorMessage = input.parentElement.querySelector('.error-message');
        if (errorMessage) {
            errorMessage.remove();
        }
    }

    // Función para validar el campo de número de tarjeta
    function validateCardNumber() {
        const value = cardNumberInput.value.replace(/\s/g, '');
        
        if (value.length === 0) {
            showError(cardNumberInput, 'El número de tarjeta es requerido');
            return false;
        }
        
        if (value.length < 13 || value.length > 19) {
            showError(cardNumberInput, 'El número de tarjeta debe tener entre 13 y 19 dígitos');
            return false;
        }

        if (!/^\d+$/.test(value)) {
            showError(cardNumberInput, 'El número de tarjeta solo debe contener dígitos');
            return false;
        }

        clearError(cardNumberInput);
        return true;
    }

    // Función para validar el nombre en la tarjeta
    function validateCardName() {
        const value = cardNameInput.value.trim();
        
        if (value.length === 0) {
            showError(cardNameInput, 'El nombre en la tarjeta es requerido');
            return false;
        }
        
        if (value.length < 3) {
            showError(cardNameInput, 'El nombre debe tener al menos 3 caracteres');
            return false;
        }

        if (!/^[a-zA-Z\s]+$/.test(value)) {
            showError(cardNameInput, 'El nombre solo debe contener letras y espacios');
            return false;
        }

        clearError(cardNameInput);
        return true;
    }

    // Función para validar la fecha de expiración
    function validateExpiry() {
        const value = expiryDateInput.value.trim();
        
        if (value.length === 0) {
            showError(expiryDateInput, 'La fecha de expiración es requerida');
            return false;
        }
        
        if (value.length !== 5) {
            showError(expiryDateInput, 'Formato inválido. Use MM/AA');
            return false;
        }

        if (!validateExpiryDate(value)) {
            showError(expiryDateInput, 'La tarjeta ha expirado o la fecha es inválida');
            return false;
        }

        clearError(expiryDateInput);
        return true;
    }

    // Función para validar el CVV
    function validateCVV() {
        const value = cvvInput.value.trim();
        
        if (value.length === 0) {
            showError(cvvInput, 'El CVV es requerido');
            return false;
        }
        
        if (value.length < 3 || value.length > 4) {
            showError(cvvInput, 'El CVV debe tener 3 o 4 dígitos');
            return false;
        }

        if (!/^\d+$/.test(value)) {
            showError(cvvInput, 'El CVV solo debe contener números');
            return false;
        }

        clearError(cvvInput);
        return true;
    }

    // Event listeners para formateo automático
    if (cardNumberInput) {
        cardNumberInput.addEventListener('input', function(e) {
            const formatted = formatCardNumber(e.target.value);
            e.target.value = formatted;
        });

        cardNumberInput.addEventListener('blur', validateCardNumber);
    }

    if (cardNameInput) {
        cardNameInput.addEventListener('input', function(e) {
            // Convertir a mayúsculas automáticamente
            e.target.value = e.target.value.toUpperCase();
        });

        cardNameInput.addEventListener('blur', validateCardName);
    }

    if (expiryDateInput) {
        expiryDateInput.addEventListener('input', function(e) {
            const formatted = formatExpiryDate(e.target.value);
            e.target.value = formatted;
        });

        expiryDateInput.addEventListener('blur', validateExpiry);
    }

    if (cvvInput) {
        cvvInput.addEventListener('input', function(e) {
            // Solo permitir números
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });

        cvvInput.addEventListener('blur', validateCVV);
    }

    // Mostrar/ocultar campos de tarjeta según el método de pago seleccionado
    paymentMethodInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.value === 'card') {
                cardDetailsSection.style.display = 'block';
                // Hacer los campos requeridos
                cardNumberInput.required = true;
                cardNameInput.required = true;
                expiryDateInput.required = true;
                cvvInput.required = true;
            } else {
                cardDetailsSection.style.display = 'none';
                // Quitar requeridos
                cardNumberInput.required = false;
                cardNameInput.required = false;
                expiryDateInput.required = false;
                cvvInput.required = false;
                // Limpiar errores
                clearError(cardNumberInput);
                clearError(cardNameInput);
                clearError(expiryDateInput);
                clearError(cvvInput);
            }
        });
    });

    // Validación al enviar el formulario
    if (paymentForm) {
        paymentForm.addEventListener('submit', function(e) {
            const selectedPaymentMethod = document.querySelector('input[name="payment_method"]:checked').value;
            
            if (selectedPaymentMethod === 'card') {
                const isCardNumberValid = validateCardNumber();
                const isCardNameValid = validateCardName();
                const isExpiryValid = validateExpiry();
                const isCVVValid = validateCVV();

                if (!isCardNumberValid || !isCardNameValid || !isExpiryValid || !isCVVValid) {
                    e.preventDefault();
                    
                    // Scroll al primer campo con error
                    const firstError = document.querySelector('.border-red-500');
                    if (firstError) {
                        firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        firstError.focus();
                    }
                }
            }
        });
    }

    // Agregar efecto visual cuando se selecciona un método de pago
    const paymentOptions = document.querySelectorAll('input[name="payment_method"]');
    paymentOptions.forEach(option => {
        option.addEventListener('change', function() {
            // Remover clases activas
            document.querySelectorAll('input[name="payment_method"]').forEach(input => {
                const label = input.closest('label');
                const div = label.querySelector('div');
                div.classList.remove('ring-2', 'ring-blue-500');
            });

            // Agregar clase activa al seleccionado
            if (this.checked) {
                const label = this.closest('label');
                const div = label.querySelector('div');
                div.classList.add('ring-2', 'ring-blue-500');
            }
        });
    });

    // Activar el método de pago por defecto al cargar
    const defaultPaymentMethod = document.querySelector('input[name="payment_method"]:checked');
    if (defaultPaymentMethod) {
        const label = defaultPaymentMethod.closest('label');
        const div = label.querySelector('div');
        div.classList.add('ring-2', 'ring-blue-500');
    }
});
