function showTab(tab) {
    const tabs = ['profile', 'orders', 'wishlist', 'settings'];
    tabs.forEach(function(t) {
        document.getElementById('tab-content-' + t).classList.add('hidden');
        document.getElementById('tab-' + t).classList.remove('bg-gray-800', 'text-white');
    });
    document.getElementById('tab-content-' + tab).classList.remove('hidden');
    document.getElementById('tab-' + tab).classList.add('bg-gray-800', 'text-white');
}
// Set default tab
window.addEventListener('DOMContentLoaded', function() {
    showTab('profile');
});
