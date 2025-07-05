document.addEventListener('DOMContentLoaded', function() {
    // Auto-fade messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    
    messages.forEach(message => {
        // Set timeout for auto-fade
        setTimeout(() => {
            message.classList.add('fade-out');
            
            // Remove element after fade completes
            setTimeout(() => {
                message.remove();
            }, 500); // Match this with CSS transition time
        }, 5000);
        
        // Close button functionality
        const closeBtn = message.querySelector('.close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                message.classList.add('fade-out');
                setTimeout(() => {
                    message.remove();
                }, 500);
            });
        }
    });
});