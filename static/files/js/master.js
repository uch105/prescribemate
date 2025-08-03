// script.js

document.addEventListener('DOMContentLoaded', () => {
    // Auto-fading Messages
    const messagesContainer = document.querySelector('.messages-container');
    if (messagesContainer) {
        const messages = messagesContainer.querySelectorAll('.message');
        messages.forEach(message => {
            const closeBtn = message.querySelector('.close-btn');
            if (closeBtn) {
                closeBtn.addEventListener('click', () => {
                    message.classList.add('fade-out');
                    message.addEventListener('transitionend', () => {
                        message.remove();
                    });
                });
            }

            // Auto-fade after 5 seconds
            setTimeout(() => {
                message.classList.add('fade-out');
                message.addEventListener('transitionend', () => {
                    message.remove();
                });
            }, 25000); // Adjust time as needed (5000ms = 5 seconds)
        });
    }

    // Password Show/Hide Toggle
    document.querySelectorAll('.password-toggle').forEach(toggle => {
        toggle.addEventListener('click', () => {
            const passwordInput = toggle.previousElementSibling; // Assumes input is sibling
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                toggle.textContent = 'Hide'; // Or change to an eye-slash icon
            } else {
                passwordInput.type = 'password';
                toggle.textContent = 'Show'; // Or change to an eye icon
            }
        });
    });

    // File Upload Button Display Name
    document.querySelectorAll('.file-upload-wrapper input[type="file"]').forEach(input => {
        input.addEventListener('change', function() {
            const fileNameDisplay = this.closest('.file-upload-wrapper').querySelector('.file-upload-name');
            if (this.files.length > 0) {
                fileNameDisplay.textContent = this.files[0].name;
            } else {
                fileNameDisplay.textContent = 'No file chosen';
            }
        });
    });

    // Text Input Suggestion Box (Autocomplete)
    document.querySelectorAll('.autocomplete-input').forEach(input => {
        const container = input.closest('.autocomplete-container');
        const suggestionsBox = container.querySelector('.autocomplete-suggestions');
        let currentActive = -1;

        const suggestions = ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry', 'Fig', 'Grape']; // Example data

        input.addEventListener('input', () => {
            const inputValue = input.value.toLowerCase();
            suggestionsBox.innerHTML = '';
            currentActive = -1;

            if (inputValue.length === 0) {
                suggestionsBox.classList.remove('show');
                return;
            }

            const filteredSuggestions = suggestions.filter(s => s.toLowerCase().includes(inputValue));

            if (filteredSuggestions.length > 0) {
                filteredSuggestions.forEach((item, index) => {
                    const div = document.createElement('div');
                    div.classList.add('autocomplete-suggestion-item');
                    div.textContent = item;
                    div.addEventListener('click', () => {
                        input.value = item;
                        suggestionsBox.classList.remove('show');
                    });
                    suggestionsBox.appendChild(div);
                });
                suggestionsBox.classList.add('show');
            } else {
                suggestionsBox.classList.remove('show');
            }
        });

        input.addEventListener('keydown', (e) => {
            const items = suggestionsBox.querySelectorAll('.autocomplete-suggestion-item');
            if (e.key === 'ArrowDown') {
                currentActive++;
                if (currentActive >= items.length) currentActive = 0;
                setActive(items, currentActive);
            } else if (e.key === 'ArrowUp') {
                currentActive--;
                if (currentActive < 0) currentActive = items.length - 1;
                setActive(items, currentActive);
            } else if (e.key === 'Enter') {
                e.preventDefault();
                if (currentActive > -1 && items[currentActive]) {
                    items[currentActive].click();
                }
            }
        });

        function setActive(items, index) {
            items.forEach(item => item.classList.remove('active'));
            if (items[index]) {
                items[index].classList.add('active');
                items[index].scrollIntoView({ block: 'nearest' });
            }
        }

        document.addEventListener('click', (e) => {
            if (!container.contains(e.target)) {
                suggestionsBox.classList.remove('show');
            }
        });
    });

    // Dark Mode Toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        // Check for saved preference in localStorage
        if (localStorage.getItem('darkMode') === 'enabled') {
            document.body.classList.add('dark-mode');
            darkModeToggle.checked = true;
        }

        darkModeToggle.addEventListener('change', () => {
            if (darkModeToggle.checked) {
                document.body.classList.add('dark-mode');
                localStorage.setItem('darkMode', 'enabled');
            } else {
                document.body.classList.remove('dark-mode');
                localStorage.setItem('darkMode', 'disabled');
            }
        });
    }

    // Navbar Mobile Toggle
    const navbarToggle = document.querySelector('.navbar-toggle');
    const navbarMenu = document.querySelector('.navbar-menu');

    if (navbarToggle && navbarMenu) {
        navbarToggle.addEventListener('click', () => {
            navbarMenu.classList.toggle('active');
        });
    }
});

// Function to add a message (for Django integration)
function addMessage(type, text) {
    const messagesContainer = document.getElementById('messages-container');
    if (!messagesContainer) {
        console.error('Messages container not found!');
        return;
    }

    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `message-${type}`);
    messageDiv.innerHTML = `
        <span class="message-text">${text}</span>
        <button class="close-btn">&times;</button>
    `;
    messagesContainer.appendChild(messageDiv);

    const closeBtn = messageDiv.querySelector('.close-btn');
    closeBtn.addEventListener('click', () => {
        messageDiv.classList.add('fade-out');
        messageDiv.addEventListener('transitionend', () => {
            messageDiv.remove();
        });
    });

    setTimeout(() => {
        messageDiv.classList.add('fade-out');
        messageDiv.addEventListener('transitionend', () => {
            messageDiv.remove();
        });
    }, 5000); // Auto-fade after 5 seconds
}

// Example usage for Django messages (you'd integrate this in your Django template)
// {% if messages %}
// <script>
//     document.addEventListener('DOMContentLoaded', function() {
//         {% for message in messages %}
//             addMessage('{{ message.tags }}', '{{ message|escapejs }}');
//         {% endfor %}
//     });
// </script>
// {% endif %}