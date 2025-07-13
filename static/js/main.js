// Main JavaScript for DigitalBank Application
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all components
    initializeAnimations();
    initializeCharts();
    initializeFormValidation();
    initializeRealTimeUpdates();
    initializeInteractiveElements();
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

// Animation initialization
function initializeAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card, .dashboard-card, .account-card, .insurance-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, { threshold: 0.1 });
    
    cards.forEach(card => observer.observe(card));
    
    // Add hover effects
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Chart initialization
function initializeCharts() {
    const chartCanvas = document.getElementById('transactionChart');
    if (chartCanvas) {
        const ctx = chartCanvas.getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Deposits',
                    data: [1200, 1900, 3000, 5000, 2000, 3000],
                    borderColor: '#28a745',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    tension: 0.4
                }, {
                    label: 'Withdrawals',
                    data: [800, 1200, 2000, 3000, 1500, 2500],
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Transaction History'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    // Pie chart for account distribution
    const pieCanvas = document.getElementById('accountPieChart');
    if (pieCanvas) {
        const ctx = pieCanvas.getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Savings', 'Checking', 'Business'],
                datasets: [{
                    data: [300, 50, 100],
                    backgroundColor: [
                        '#667eea',
                        '#764ba2',
                        '#f093fb'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    }
                }
            }
        });
    }
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Real-time password strength checker
    const passwordField = document.querySelector('input[type="password"]');
    if (passwordField) {
        passwordField.addEventListener('input', function() {
            const strength = checkPasswordStrength(this.value);
            updatePasswordStrengthIndicator(strength);
        });
    }
}

// Password strength checker
function checkPasswordStrength(password) {
    let strength = 0;
    
    if (password.length >= 8) strength++;
    if (password.match(/[a-z]/)) strength++;
    if (password.match(/[A-Z]/)) strength++;
    if (password.match(/[0-9]/)) strength++;
    if (password.match(/[^a-zA-Z0-9]/)) strength++;
    
    return strength;
}

// Update password strength indicator
function updatePasswordStrengthIndicator(strength) {
    const indicator = document.getElementById('passwordStrength');
    if (!indicator) return;
    
    const strengthText = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
    const strengthColors = ['#dc3545', '#fd7e14', '#ffc107', '#28a745', '#20c997'];
    
    indicator.textContent = strengthText[strength - 1] || 'Very Weak';
    indicator.style.color = strengthColors[strength - 1] || '#dc3545';
}

// Real-time updates
function initializeRealTimeUpdates() {
    // Update account balances in real-time
    setInterval(function() {
        updateAccountBalances();
    }, 30000); // Update every 30 seconds
    
    // Live transaction counter
    const transactionCounter = document.getElementById('transactionCounter');
    if (transactionCounter) {
        let count = parseInt(transactionCounter.textContent) || 0;
        setInterval(function() {
            count++;
            transactionCounter.textContent = count;
        }, 5000); // Increment every 5 seconds for demo
    }
}

// Update account balances via AJAX
function updateAccountBalances() {
    const accountCards = document.querySelectorAll('.account-card');
    
    accountCards.forEach(card => {
        const accountId = card.dataset.accountId;
        const balanceElement = card.querySelector('.account-balance');
        
        if (accountId && balanceElement) {
            fetch(`/api/account_balance/${accountId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.balance !== undefined) {
                        balanceElement.textContent = `$${data.balance.toFixed(2)}`;
                    }
                })
                .catch(error => console.error('Error updating balance:', error));
        }
    });
}

// Interactive elements
function initializeInteractiveElements() {
    // Transaction type toggle
    const transactionTypeToggles = document.querySelectorAll('.transaction-type-toggle');
    transactionTypeToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const type = this.dataset.type;
            updateTransactionForm(type);
        });
    });
    
    // Account card selection
    const accountCards = document.querySelectorAll('.account-card');
    accountCards.forEach(card => {
        card.addEventListener('click', function() {
            // Remove active class from all cards
            accountCards.forEach(c => c.classList.remove('active'));
            // Add active class to clicked card
            this.classList.add('active');
        });
    });
    
    // Insurance policy details expander
    const policyCards = document.querySelectorAll('.insurance-card');
    policyCards.forEach(card => {
        const detailsBtn = card.querySelector('.policy-details-btn');
        const details = card.querySelector('.policy-details');
        
        if (detailsBtn && details) {
            detailsBtn.addEventListener('click', function() {
                details.classList.toggle('show');
                this.textContent = details.classList.contains('show') ? 'Hide Details' : 'Show Details';
            });
        }
    });
}

// Update transaction form based on type
function updateTransactionForm(type) {
    const form = document.querySelector('#transactionForm');
    const amountField = form.querySelector('#amount');
    const descriptionField = form.querySelector('#description');
    
    // Update form based on transaction type
    switch(type) {
        case 'deposit':
            amountField.placeholder = 'Enter deposit amount';
            descriptionField.placeholder = 'Deposit description (optional)';
            break;
        case 'withdrawal':
            amountField.placeholder = 'Enter withdrawal amount';
            descriptionField.placeholder = 'Withdrawal reason (optional)';
            break;
        case 'transfer':
            amountField.placeholder = 'Enter transfer amount';
            descriptionField.placeholder = 'Transfer to account (optional)';
            break;
    }
}

// Loading spinner
function showLoading(element) {
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    element.appendChild(spinner);
    element.disabled = true;
}

function hideLoading(element) {
    const spinner = element.querySelector('.spinner');
    if (spinner) {
        spinner.remove();
    }
    element.disabled = false;
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Currency formatter
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Date formatter
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Search functionality
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const items = document.querySelectorAll('.searchable-item');
            
            items.forEach(item => {
                const text = item.textContent.toLowerCase();
                if (text.includes(query)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
}

// Export functionality
function exportData(type) {
    const data = getExportData(type);
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${type}_data_${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
}

// Get data for export
function getExportData(type) {
    // This would typically fetch data from the server
    // For demo purposes, returning sample data
    return {
        type: type,
        timestamp: new Date().toISOString(),
        data: []
    };
}

// Initialize search when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeSearch();
});

// Global error handler
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    showNotification('An error occurred. Please try again.', 'danger');
});

// Network status indicator
window.addEventListener('online', function() {
    showNotification('Connection restored!', 'success');
});

window.addEventListener('offline', function() {
    showNotification('You are offline. Some features may not work.', 'warning');
}); 