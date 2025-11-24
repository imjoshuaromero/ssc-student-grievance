// Use the same origin as the current page to avoid CORS issues
const API_BASE_URL = `${window.location.protocol}//${window.location.host}/api`;

// Show Alert Function
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alertContainer');
    const alertClass = {
        'success': 'alert-success',
        'error': 'alert-error',
        'warning': 'alert-warning',
        'info': 'alert-info'
    }[type] || 'alert-info';
    
    const icon = {
        'success': 'fa-check-circle',
        'error': 'fa-exclamation-circle',
        'warning': 'fa-exclamation-triangle',
        'info': 'fa-info-circle'
    }[type] || 'fa-info-circle';
    
    alertContainer.innerHTML = `
        <div class="alert ${alertClass} shadow-lg">
            <div>
                <i class="fas ${icon}"></i>
                <span>${message}</span>
            </div>
        </div>
    `;
    
    setTimeout(() => {
        alertContainer.innerHTML = '';
    }, 5000);
}

// Toggle Password Visibility
function initPasswordToggle() {
    const toggleBtn = document.getElementById('togglePassword');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            const passwordInput = document.getElementById('password');
            const eyeIcon = document.getElementById('eyeIcon');
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                eyeIcon.classList.remove('fa-eye');
                eyeIcon.classList.add('fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                eyeIcon.classList.remove('fa-eye-slash');
                eyeIcon.classList.add('fa-eye');
            }
        });
    }
}

// Google Sign In
function initGoogleSignIn() {
    const googleBtn = document.getElementById('googleSignInBtn');
    if (googleBtn) {
        googleBtn.addEventListener('click', async function() {
            try {
                showAlert('Redirecting to Google...', 'info');
                
                const response = await fetch(`${API_BASE_URL}/auth/google`);
                const data = await response.json();
                
                if (data.auth_url) {
                    window.location.href = data.auth_url;
                } else {
                    showAlert('Failed to initialize Google sign-in', 'error');
                }
            } catch (error) {
                console.error('Google sign-in error:', error);
                showAlert('Failed to connect to Google. Please try again.', 'error');
            }
        });
    }
}

// Traditional Login
function initLoginForm() {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const loginBtn = document.getElementById('loginBtn');
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            // Disable button and show loading
            loginBtn.disabled = true;
            loginBtn.innerHTML = '<span class="loading loading-spinner"></span> Signing in...';
            
            try {
                const response = await fetch(`${API_BASE_URL}/auth/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });
                
                const data = await response.json();
                
                if (response.ok && data.token) {
                    // Save token and user info
                    localStorage.setItem('token', data.token);
                    localStorage.setItem('user', JSON.stringify(data.user));
                    
                    showAlert('Login successful! Redirecting...', 'success');
                    
                    // Redirect based on role
                    setTimeout(() => {
                        if (data.user.role === 'admin') {
                            window.location.href = '/admin-dashboard';
                        } else {
                            window.location.href = '/student-dashboard';
                        }
                    }, 1000);
                } else {
                    showAlert(data.error || 'Invalid email or password', 'error');
                    loginBtn.disabled = false;
                    loginBtn.innerHTML = '<i class="fas fa-sign-in-alt mr-2"></i> Sign In';
                }
            } catch (error) {
                console.error('Login error:', error);
                showAlert('Failed to connect to server. Please try again.', 'error');
                loginBtn.disabled = false;
                loginBtn.innerHTML = '<i class="fas fa-sign-in-alt mr-2"></i> Sign In';
            }
        });
    }
}

// Check if already logged in
function checkAuthStatus() {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    
    // Only redirect from login/register pages, not from dashboard pages
    const currentPath = window.location.pathname;
    const isDashboard = currentPath.includes('dashboard');
    
    if (token && user && !isDashboard) {
        const userData = JSON.parse(user);
        if (userData.role === 'admin') {
            window.location.href = '/admin-dashboard';
        } else {
            window.location.href = '/student-dashboard';
        }
    }
}

// Handle Google OAuth callback
function handleOAuthCallback() {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    const needsRegistration = urlParams.get('needs_registration');
    
    if (token) {
        localStorage.setItem('token', token);
        // Fetch user info
        fetch(`${API_BASE_URL}/users/profile`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(res => res.json())
        .then(data => {
            localStorage.setItem('user', JSON.stringify(data.user));
            showAlert('Google sign-in successful!', 'success');
            
            setTimeout(() => {
                if (data.user.role === 'admin') {
                    window.location.href = '/admin-dashboard';
                } else {
                    window.location.href = '/student-dashboard';
                }
            }, 1000);
        });
    } else if (needsRegistration === 'true') {
        showAlert('Please complete your registration', 'info');
        setTimeout(() => {
            window.location.href = '/register?google=true';
        }, 2000);
    }
}

// Logout function
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
}

// Initialize auth features
document.addEventListener('DOMContentLoaded', function() {
    initPasswordToggle();
    initGoogleSignIn();
    initLoginForm();
    checkAuthStatus();
    handleOAuthCallback();
});
