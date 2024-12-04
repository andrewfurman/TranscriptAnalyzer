// static/analyzer.js

document.addEventListener('DOMContentLoaded', function() {
    const analyzeForm = document.getElementById('analyzeForm');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const analyzeButton = document.getElementById('analyzeButton');

    // Add click handler for the analyze button
    analyzeButton.addEventListener('click', function(e) {
        e.preventDefault(); // Prevent default button behavior
        
        // Show loading state
        loadingSpinner.classList.remove('hidden');
        analyzeButton.disabled = true;
        
        // Submit the form
        analyzeForm.submit();
    });

    // Handle form submission
    analyzeForm.addEventListener('submit', function(e) {
        // Show loading state
        loadingSpinner.classList.remove('hidden');
        analyzeButton.disabled = true;
    });
});