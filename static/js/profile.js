/**
 * Profile Page - Address Management
 * Handles address CRUD operations and modal interactions
 */

// Tab Navigation Functions
function showTab(tab) {
    const tabs = ['profile', 'orders', 'wishlist', 'settings'];
    tabs.forEach(function(t) {
        document.getElementById('tab-content-' + t).classList.add('hidden');
        document.getElementById('tab-' + t).classList.remove('bg-gray-800', 'text-white');
    });
    document.getElementById('tab-content-' + tab).classList.remove('hidden');
    document.getElementById('tab-' + tab).classList.add('bg-gray-800', 'text-white');
}

// Modal Functions
function openAddressModal() {
    const modal = document.getElementById('address-modal');
    modal.classList.remove('hidden');
    // Prevent body scroll when modal is open
    document.body.style.overflow = 'hidden';
}

function closeAddressModal() {
    const modal = document.getElementById('address-modal');
    modal.classList.add('hidden');
    document.getElementById('add-address-form').reset();
    // Restore body scroll
    document.body.style.overflow = 'auto';
}

// Edit Address Inline Form
function editAddress(addressId) {
    const addressItem = document.querySelector(`[data-address-id="${addressId}"]`);
    const display = addressItem.querySelector('.address-display');
    const editForm = addressItem.querySelector('.address-edit-form');

    display.classList.add('hidden');
    editForm.classList.remove('hidden');
}

function cancelEdit(addressId) {
    const addressItem = document.querySelector(`[data-address-id="${addressId}"]`);
    const display = addressItem.querySelector('.address-display');
    const editForm = addressItem.querySelector('.address-edit-form');

    display.classList.remove('hidden');
    editForm.classList.add('hidden');
}

// Add Address Handler
async function addAddress(event) {
    event.preventDefault();
    event.stopPropagation();

    console.log('addAddress function called');

    const form = event.target;
    const formData = new FormData(form);

    // Add CSRF token to form data
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    formData.append('csrfmiddlewaretoken', csrfToken);

    console.log('FormData contents:');
    for (let [key, value] of formData.entries()) {
        console.log(key, value);
    }

    try {
        console.log('Sending request to /accounts/addresses/add/');
        const response = await fetch('/accounts/addresses/add/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Accept': 'application/json',
            },
            body: formData
        });

        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);

        if (response.ok) {
            const result = await response.json();
            console.log('Response result:', result);

            if (result.success) {
                closeAddressModal();
                // Reload the page to show the new address
                location.reload();
            } else {
                alert('Error al agregar la dirección: ' + JSON.stringify(result.errors));
            }
        } else {
            console.log('Response not ok:', response.status, response.statusText);
            alert('Error al agregar la dirección');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al agregar la dirección');
    }

    return false;
}

// Save Address Handler
async function saveAddress(event, addressId) {
    event.preventDefault();
    event.stopPropagation();

    console.log('saveAddress function called for address:', addressId);

    const form = event.target;
    const formData = new FormData(form);

    // Get CSRF token from the main form or meta tag
    let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!csrfToken) {
        csrfToken = document.querySelector('meta[name="csrf-token"]');
        if (csrfToken) {
            formData.append('csrfmiddlewaretoken', csrfToken.content);
        }
    } else {
        formData.append('csrfmiddlewaretoken', csrfToken.value);
    }

    console.log('FormData contents:');
    for (let [key, value] of formData.entries()) {
        console.log(key, value);
    }

    try {
        console.log(`Sending request to /accounts/addresses/${addressId}/edit/`);
        const response = await fetch(`/accounts/addresses/${addressId}/edit/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken ? (csrfToken.value || csrfToken.content) : '',
                'Accept': 'application/json',
            },
            body: formData
        });

        console.log('Response status:', response.status);

        if (response.ok) {
            const result = await response.json();
            console.log('Response result:', result);

            if (result.success) {
                // Reload the page to show the updated address
                location.reload();
            } else {
                alert('Error al actualizar la dirección: ' + JSON.stringify(result.errors));
            }
        } else {
            console.log('Response not ok:', response.status, response.statusText);
            alert('Error al actualizar la dirección');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al actualizar la dirección');
    }

    return false;
}

// Delete Address Handler
async function deleteAddress(addressId) {
    if (confirm('¿Estás seguro de que quieres eliminar esta dirección?')) {
        // Get CSRF token
        let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        const csrfValue = csrfToken ? csrfToken.value : '';

        try {
            const response = await fetch(`/accounts/addresses/${addressId}/delete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfValue,
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `csrfmiddlewaretoken=${csrfValue}`
            });

            if (response.ok) {
                const result = await response.json();
                if (result.success) {
                    // Remove the address from DOM
                    const addressItem = document.querySelector(`[data-address-id="${addressId}"]`);
                    addressItem.remove();

                    // Show "no addresses" message if no addresses left
                    const container = document.getElementById('addresses-container');
                    if (container.children.length === 0) {
                        container.innerHTML = '<div id="no-addresses" class="text-gray-400 text-center py-8">No tienes direcciones de envío guardadas.</div>';
                    }
                } else {
                    alert('Error al eliminar la dirección: ' + result.message);
                }
            } else {
                alert('Error al eliminar la dirección');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error al eliminar la dirección');
        }
    }
}

// Initialize Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tab if needed
    const tabProfile = document.getElementById('tab-content-profile');
    if (tabProfile) {
        showTab('profile');
    }

    // Initialize modal
    const modal = document.getElementById('address-modal');
    if (modal) {
        // Close modal when clicking outside
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeAddressModal();
            }
        });

        // Prevent modal from closing when clicking inside
        const modalContent = modal.querySelector('.bg-gray-900');
        if (modalContent) {
            modalContent.addEventListener('click', function(e) {
                e.stopPropagation();
            });
        }
    }

    // Open modal button
    const openModalBtn = document.getElementById('open-address-modal-btn');
    if (openModalBtn) {
        openModalBtn.addEventListener('click', openAddressModal);
    }

    // Close modal button
    const closeModalBtn = document.getElementById('close-modal-btn');
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', closeAddressModal);
    }

    // Add event listener to form to prevent default submission
    const addForm = document.getElementById('add-address-form');
    if (addForm) {
        addForm.addEventListener('submit', addAddress);
    }

    // Event delegation for edit buttons
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('edit-address-btn') || e.target.closest('.edit-address-btn')) {
            const button = e.target.classList.contains('edit-address-btn') ? e.target : e.target.closest('.edit-address-btn');
            const addressId = button.getAttribute('data-address-id');
            editAddress(addressId);
        }
    });

    // Event delegation for delete buttons
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-address-btn') || e.target.closest('.delete-address-btn')) {
            const button = e.target.classList.contains('delete-address-btn') ? e.target : e.target.closest('.delete-address-btn');
            const addressId = button.getAttribute('data-address-id');
            deleteAddress(addressId);
        }
    });

    // Event delegation for cancel edit buttons
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('cancel-edit-btn') || e.target.closest('.cancel-edit-btn')) {
            const button = e.target.classList.contains('cancel-edit-btn') ? e.target : e.target.closest('.cancel-edit-btn');
            const addressId = button.getAttribute('data-address-id');
            cancelEdit(addressId);
        }
    });

    // Add event listeners to all edit forms
    const editForms = document.querySelectorAll('.edit-address-form');
    editForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const addressId = form.getAttribute('data-address-id');
            saveAddress(event, addressId);
        });
    });
});
