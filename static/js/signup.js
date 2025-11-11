(function () {
    // Firebase configuration - will be loaded from Django settings
    const firebaseConfig = {
        apiKey: "{{ FIREBASE_CONFIG.apiKey }}",
        authDomain: "{{ FIREBASE_CONFIG.authDomain }}",
        projectId: "{{ FIREBASE_CONFIG.projectId }}",
        storageBucket: "{{ FIREBASE_CONFIG.storageBucket }}",
        messagingSenderId: "{{ FIREBASE_CONFIG.messagingSenderId }}",
        appId: "{{ FIREBASE_CONFIG.appId }}",
        databaseURL: "{{ FIREBASE_CONFIG.databaseURL }}"
    };

    // Initialize Firebase only if config is available
    let firebaseInitialized = false;
    let auth = null;
    let recaptchaVerifier = null;

    if (firebaseConfig.apiKey && firebaseConfig.apiKey !== '') {
        try {
            firebase.initializeApp(firebaseConfig);
            auth = firebase.auth();
            firebaseInitialized = true;
        } catch (error) {
            console.log('Firebase initialization skipped:', error);
        }
    }

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

        // Add to container
        const container = document.getElementById('toastContainer');
        container.appendChild(toast);

        // Remove after 5 seconds
        setTimeout(() => removeToast(toast), 5000);
    }

    function removeToast(toast) {
        toast.classList.replace('translate-y-0', '-translate-y-12');
        toast.classList.replace('opacity-100', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
    }

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    const form = document.getElementById('signupForm');
    const passwordInput = document.getElementById('password');
    const toggleBtn = document.querySelector('#signupForm .toggle-password');

    if (toggleBtn && passwordInput) {
        toggleBtn.addEventListener('click', () => {
            const isPassword = passwordInput.type === 'password';
            passwordInput.type = isPassword ? 'text' : 'password';
            // Update icon to match visibility state
            toggleBtn.innerHTML = isPassword
                ? `<svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
          </svg>`
                : `<svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z" />
            <circle cx="12" cy="12" r="3" />
          </svg>`;
        });
    }

    // Initialize reCAPTCHA for Firebase phone auth
    function initializeRecaptcha() {
        if (!firebaseInitialized || recaptchaVerifier) return;
        
        try {
            recaptchaVerifier = new firebase.auth.RecaptchaVerifier('recaptcha-container', {
                'size': 'invisible',
                'callback': (response) => {
                    // reCAPTCHA solved
                }
            });
        } catch (error) {
            console.log('reCAPTCHA initialization skipped:', error);
        }
    }

    // Send OTP to phone number
    async function sendOTP(phoneNumber) {
        if (!firebaseInitialized || !recaptchaVerifier) {
            return null;
        }

        try {
            const confirmationResult = await auth.signInWithPhoneNumber(phoneNumber, recaptchaVerifier);
            return confirmationResult;
        } catch (error) {
            console.error('Error sending OTP:', error);
            throw error;
        }
    }

    // Verify OTP
    async function verifyOTP(confirmationResult, code) {
        if (!confirmationResult) return null;

        try {
            const result = await confirmationResult.confirm(code);
            return result.user;
        } catch (error) {
            console.error('Error verifying OTP:', error);
            throw error;
        }
    }

    if (form) {
        // Add input validation styles
        const inputs = form.querySelectorAll('input[required]');
        inputs.forEach(input => {
            input.addEventListener('invalid', () => {
                input.classList.add('border-red-300');
                showToast(`Please enter a valid ${input.id}`);
            });
            input.addEventListener('input', () => {
                input.classList.remove('border-red-300');
            });
        });

        // Initialize reCAPTCHA when form is ready
        if (firebaseInitialized) {
            setTimeout(initializeRecaptcha, 1000);
        }

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const emailEl = document.getElementById('email');
            const phoneEl = document.getElementById('phone');
            const passwordEl = document.getElementById('password');

            const email = (emailEl?.value || '').trim();
            const phone = (phoneEl?.value || '').trim();
            const password = (passwordEl?.value || '').trim();

            // Basic validation
            if (!email || !password) {
                showToast('Please enter an email and password.');
                return;
            }

            // Email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                showToast('Please enter a valid email address.');
                emailEl.classList.add('border-red-300');
                return;
            }

            // Password validation
            if (password.length < 6) {
                showToast('Password must be at least 6 characters long.');
                passwordEl.classList.add('border-red-300');
                return;
            }

            // Phone validation (if provided)
            if (phone && !/^\+?[\d\s-]{10,}$/.test(phone)) {
                showToast('Please enter a valid phone number with country code (e.g., +1234567890).');
                phoneEl.classList.add('border-red-300');
                return;
            }

            // OTP verification flow if Firebase is initialized and phone is provided
            if (firebaseInitialized && phone && phone.trim()) {
                try {
                    // Ensure phone has country code
                    let formattedPhone = phone.trim();
                    if (!formattedPhone.startsWith('+')) {
                        showToast('Please include country code in phone number (e.g., +1 for US).');
                        phoneEl.classList.add('border-red-300');
                        return;
                    }

                    showToast('Sending OTP to your phone...', 'success');
                    
                    // Send OTP
                    const confirmationResult = await sendOTP(formattedPhone);
                    
                    if (!confirmationResult) {
                        throw new Error('Failed to send OTP');
                    }

                    // Prompt for OTP
                    const otp = prompt('Enter the OTP sent to your phone:');
                    
                    if (!otp) {
                        showToast('OTP verification cancelled.');
                        return;
                    }

                    showToast('Verifying OTP...', 'success');
                    
                    // Verify OTP
                    await verifyOTP(confirmationResult, otp);
                    
                    showToast('Phone verified successfully!', 'success');
                } catch (error) {
                    console.error('OTP verification error:', error);
                    showToast('OTP verification failed. Proceeding without phone verification.');
                }
            }

            // Use email as username for simplicity
            const payload = {
                username: email,
                email,
                password,
                phone_number: phone || undefined,
            };

            try {
                showToast('Creating your account...', 'success');

                const res = await fetch('/api/user/register/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken') || '',
                    },
                    body: JSON.stringify(payload),
                });

                const data = await res.json().catch(() => ({}));

                if (!res.ok) {
                    const errors = [];

                    // Collect all error messages
                    if (data.detail) {
                        errors.push(data.detail);
                    } else {
                        // Handle specific field errors
                        if (data.email) {
                            errors.push(`Email: ${data.email.join(', ')}`);
                            emailEl.classList.add('border-red-300');
                        }
                        if (data.username) {
                            errors.push(`Username: ${data.username.join(', ')}`);
                            emailEl.classList.add('border-red-300');
                        }
                        if (data.password) {
                            errors.push(`Password: ${data.password.join(', ')}`);
                            passwordEl.classList.add('border-red-300');
                        }
                        if (data.phone_number) {
                            errors.push(`Phone number: ${data.phone_number.join(', ')}`);
                            phoneEl.classList.add('border-red-300');
                        }
                    }

                    // If no specific errors were found, use the generic message
                    if (errors.length === 0) {
                        errors.push(Object.values(data).flat().join(', ') || 'Registration failed.');
                    }

                    // Show all errors in one toast with a list
                    showToast(errors);
                    return;
                }

                // Show success message
                showToast('Account created successfully! Logging you in...', 'success');

                // Auto-login after successful registration
                try {
                    const loginRes = await fetch('/api/token/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            username: email,
                            password: password
                        })
                    });

                    if (loginRes.ok) {
                        const loginData = await loginRes.json();
                        
                        // Store tokens
                        localStorage.setItem('access_token', loginData.access);
                        localStorage.setItem('refresh_token', loginData.refresh);
                        
                        // Set the access token in a cookie for Django authentication
                        document.cookie = `jwt=${loginData.access}; path=/; sameSite=Lax`;

                        // Redirect to dashboard
                        setTimeout(() => {
                            window.location.href = '/dashboard/';
                        }, 1000);
                    } else {
                        // If auto-login fails, redirect to login page
                        setTimeout(() => {
                            window.location.href = '/login/';
                        }, 2000);
                    }
                } catch (loginErr) {
                    console.error('Auto-login error:', loginErr);
                    // If auto-login fails, redirect to login page
                    setTimeout(() => {
                        window.location.href = '/login/';
                    }, 2000);
                }
            } catch (err) {
                console.error(err);
                showToast('Network error. Please try again.');
            }
        });
    }

    // Add invisible reCAPTCHA container
    if (firebaseInitialized) {
        const recaptchaContainer = document.createElement('div');
        recaptchaContainer.id = 'recaptcha-container';
        document.body.appendChild(recaptchaContainer);
    }
})();
