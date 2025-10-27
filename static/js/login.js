document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');
    const togglePassword = document.querySelector('.toggle-password');
    const passwordInput = document.getElementById('password');

    function showToast(messages, type = 'error') {
        // Convert single message to array
        const messageArray = Array.isArray(messages) ? messages : [messages];

        const toast = document.createElement('div');
        toast.className = `toast toast-${type} translate-y-0 opacity-100`;

        // Create content wrapper
        const wrapper = document.createElement('div');
        wrapper.className = 'relative pr-4'; // Space for close button

        // Create header with icon
        const header = document.createElement('div');
        header.className = 'flex items-center';

        // Add icon based on type
        const icon = document.createElement('span');
        if (type === 'success') {
            icon.innerHTML = `<svg class="w-5 h-5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>`;
        } else {
            icon.innerHTML = `<svg class="w-5 h-5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>`;
        }
        header.appendChild(icon);

        // Add first message to header
        const headerText = document.createElement('span');
        headerText.className = 'font-medium';
        headerText.textContent = messageArray[0];
        header.appendChild(headerText);

        wrapper.appendChild(header);

        // If there are additional messages, add them as a list
        if (messageArray.length > 1) {
            const list = document.createElement('ul');
            list.className = 'toast-list';
            messageArray.slice(1).forEach(msg => {
                const li = document.createElement('li');
                li.textContent = msg;
                list.appendChild(li);
            });
            wrapper.appendChild(list);
        }

        toast.appendChild(wrapper);

        // Add close button
        const closeBtn = document.createElement('button');
        closeBtn.className = 'absolute top-1 right-1 p-1 hover:text-gray-600';
        closeBtn.innerHTML = `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
        </svg>`;
        closeBtn.onclick = () => removeToast(toast);
        toast.appendChild(closeBtn);

        // Add to container (create if doesn't exist)
        let container = document.getElementById('toastContainer');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toastContainer';
            document.body.appendChild(container);
        }
        container.appendChild(toast);

        // Remove after 5 seconds
        setTimeout(() => removeToast(toast), 5000);
    } function removeToast(toast) {
        toast.classList.replace('translate-y-0', '-translate-y-12');
        toast.classList.replace('opacity-100', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
    }

    // Toggle password visibility (no image src swapping needed)
    if (togglePassword) {
        togglePassword.addEventListener('click', function () {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            // Optionally toggle a CSS class to style the icon if needed
            togglePassword.classList.toggle('is-visible', type === 'text');
        });
    }

    // Add input validation styles
    const inputs = loginForm.querySelectorAll('input[required]');
    inputs.forEach(input => {
        input.addEventListener('invalid', () => {
            input.classList.add('border-red-300');
            showToast(`Please enter a valid ${input.id}`);
        });
        input.addEventListener('input', () => {
            input.classList.remove('border-red-300');
        });
    });

    // Handle form submission
    loginForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const emailEl = document.getElementById('email');
        const passwordEl = document.getElementById('password');

        const email = (emailEl?.value || '').trim();
        const password = (passwordEl?.value || '').trim();

        // Basic validation
        if (!email || !password) {
            showToast('Please enter an email and password.');
            return;
        }

        try {
            const response = await fetch('/api/token/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: email,
                    password: password
                })
            });

            const data = await response.json().catch(() => ({}));

            if (!response.ok) {
                const errors = [];

                // Collect all error messages
                if (data.detail) {
                    errors.push(data.detail);
                } else {
                    // Handle specific field errors
                    if (data.username) {
                        errors.push(`Username: ${data.username.join(', ')}`);
                        emailEl.classList.add('border-red-300');
                    }
                    if (data.password) {
                        errors.push(`Password: ${data.password.join(', ')}`);
                        passwordEl.classList.add('border-red-300');
                    }
                    if (data.non_field_errors) {
                        errors.push(...data.non_field_errors);
                    }
                }

                if (errors.length === 0) {
                    errors.push('Login failed. Please check your credentials and try again.');
                    emailEl.classList.add('border-red-300');
                    passwordEl.classList.add('border-red-300');
                }

                // Show all errors in one toast with a list
                showToast(errors);
                return;
            }

            // Store tokens
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);

            // Set the access token in a cookie for Django authentication
            document.cookie = `jwt=${data.access}; path=/; sameSite=Lax`;

            // Show success message and redirect
            showToast('Login successful! Redirecting...', 'success');

            // Simple redirect after a short delay
            setTimeout(() => {
                window.location.href = '/dashboard/';
            }, 1000);
        } catch (error) {
            console.error('Login error:', error);
            showToast('An error occurred. Please try again.');
        }
    });
});