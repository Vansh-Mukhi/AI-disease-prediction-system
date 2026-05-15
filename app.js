const API_URL = '/api';

// Authentication handling
function setToken(token, user) {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
}

function getToken() {
    return localStorage.getItem('token');
}

function getUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login.html';
}

function checkAuth() {
    if (!getToken() && !window.location.pathname.includes('login') && window.location.pathname !== '/' && window.location.pathname !== '/index.html') {
        window.location.href = '/login.html';
    }
}

// UI Helpers
function showAlert(message, type = 'error') {
    const alertEl = document.getElementById('alert');
    if (alertEl) {
        alertEl.textContent = message;
        alertEl.className = `alert alert-${type}`;
        alertEl.style.display = 'block';
        setTimeout(() => {
            alertEl.style.display = 'none';
        }, 5000);
    }
}

function toggleLoader(btnId, isLoading) {
    const btn = document.getElementById(btnId);
    const text = btn.querySelector('.btn-text');
    const loader = btn.querySelector('.loader');
    
    if (isLoading) {
        btn.disabled = true;
        if(text) text.style.display = 'none';
        if(loader) loader.style.display = 'block';
    } else {
        btn.disabled = false;
        if(text) text.style.display = 'inline';
        if(loader) loader.style.display = 'none';
    }
}

// Setup Nav
function setupNav() {
    const user = getUser();
    const navLinks = document.getElementById('nav-links');
    if (!navLinks) return;
    
    if (user) {
        navLinks.innerHTML = `
            <li><a href="/dashboard.html">Dashboard</a></li>
            <li><a href="#" onclick="logout()">Logout (${user.name})</a></li>
        `;
    } else {
        navLinks.innerHTML = `
            <li><a href="/login.html">Login</a></li>
        `;
    }
}

// Auth Pages Logic
async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    toggleLoader('loginBtn', true);
    try {
        const res = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await res.json();
        
        if (res.ok) {
            setToken(data.token, data.user);
            window.location.href = '/dashboard.html';
        } else {
            showAlert(data.message || 'Login failed');
        }
    } catch (err) {
        showAlert('Connection error');
    } finally {
        toggleLoader('loginBtn', false);
    }
}

async function handleSignup(e) {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    toggleLoader('signupBtn', true);
    try {
        const res = await fetch(`${API_URL}/auth/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password })
        });
        const data = await res.json();
        
        if (res.ok) {
            setToken(data.token, data.user);
            window.location.href = '/dashboard.html';
        } else {
            showAlert(data.message || 'Signup failed');
        }
    } catch (err) {
        showAlert('Connection error');
    } finally {
        toggleLoader('signupBtn', false);
    }
}

// Dashboard Logic
async function loadHistory() {
    const historyBody = document.getElementById('history-body');
    if (!historyBody) return;
    
    try {
        const res = await fetch(`${API_URL}/user/history`, {
            headers: { 'Authorization': `Bearer ${getToken()}` }
        });
        
        if (res.ok) {
            const data = await res.json();
            if (data.history.length === 0) {
                historyBody.innerHTML = '<tr><td colspan="4" style="text-align:center">No predictions yet.</td></tr>';
                return;
            }
            
            historyBody.innerHTML = data.history.map(item => `
                <tr>
                    <td>${new Date(item.timestamp).toLocaleDateString()}</td>
                    <td style="text-transform: capitalize">${item.disease}</td>
                    <td>
                        <span class="badge ${item.prediction === 1 ? 'badge-positive' : 'badge-negative'}">
                            ${item.prediction === 1 ? 'Positive' : 'Negative'}
                        </span>
                    </td>
                    <td>${(item.confidence_score * 100).toFixed(2)}%</td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error('Failed to load history', err);
    }
}

// Prediction Logic
async function submitPrediction(disease) {
    const form = document.getElementById('predictForm');
    const inputs = form.querySelectorAll('input');
    const features = Array.from(inputs).map(input => parseFloat(input.value));
    
    toggleLoader('predictBtn', true);
    try {
        const res = await fetch(`${API_URL}/predict/${disease}`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getToken()}`
            },
            body: JSON.stringify({ features })
        });
        
        const data = await res.json();
        
        if (res.ok) {
            const resultBox = document.getElementById('resultBox');
            const resultText = document.getElementById('resultText');
            
            resultBox.className = `glass-panel result-box active`;
            resultBox.style.borderColor = data.result.prediction === 1 ? 'var(--danger)' : 'var(--secondary)';
            
            resultText.innerHTML = `
                <h3 style="color: ${data.result.prediction === 1 ? 'var(--danger)' : 'var(--secondary)'}; margin-bottom: 10px;">
                    Result: ${data.result.prediction === 1 ? 'Positive' : 'Negative'}
                </h3>
                <p>Confidence: ${(data.result.confidence_score * 100).toFixed(2)}%</p>
                <p style="margin-top: 15px; font-size: 0.9em; color: var(--text-muted);">
                    Disclaimer: This is an AI prediction and should not replace professional medical advice.
                </p>
            `;
        } else {
            showAlert(data.message || 'Prediction failed');
        }
    } catch (err) {
        showAlert('Connection error');
    } finally {
        toggleLoader('predictBtn', false);
    }
}

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    setupNav();
    
    // Attach event listeners if elements exist
    const loginForm = document.getElementById('loginForm');
    if (loginForm) loginForm.addEventListener('submit', handleLogin);
    
    const signupForm = document.getElementById('signupForm');
    if (signupForm) signupForm.addEventListener('submit', handleSignup);
    
    if (window.location.pathname.includes('dashboard')) {
        const userName = document.getElementById('user-name');
        if (userName) userName.textContent = getUser().name;
        loadHistory();
    }
});
