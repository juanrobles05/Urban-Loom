/**
 * Cart Counter - Updates the shopping cart badge
 */

function updateCartCount() {
    fetch('/orders/cart-count/')
        .then(response => response.json())
        .then(data => {
            const cartCount = document.getElementById('cart-count');
            if (cartCount) {
                if (data.count > 0) {
                    cartCount.textContent = data.count;
                    cartCount.classList.remove('hidden');
                } else {
                    cartCount.classList.add('hidden');
                }
            }
        })
        .catch(error => console.error('Error updating cart count:', error));
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
});

// Expose function globally for manual updates
window.updateCartCount = updateCartCount;
