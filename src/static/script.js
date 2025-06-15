// API Configuration
const API_CONFIG = {
    development: {
        baseUrl: 'http://localhost:5000/api/v1'
    },
    production: {
        baseUrl: 'https://your-production-domain.com/api/v1' // Replace with your actual production URL
    }
};

// Determine environment
const isDevelopment = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const currentConfig = isDevelopment ? API_CONFIG.development : API_CONFIG.production;

// API endpoints
const API_BASE_URL = currentConfig.baseUrl;
const ENDPOINTS = {
    messages: `${API_BASE_URL}/messages`,
    statistics: `${API_BASE_URL}/statistics`,
    categories: `${API_BASE_URL}/categories`,
    trends: `${API_BASE_URL}/trends/daily`,
    volume: `${API_BASE_URL}/trends/volume/daily`,
    topRecipients: `${API_BASE_URL}/top/recipients`,
    topSenders: `${API_BASE_URL}/top/senders`
};

// Chart instances
let categoryChart = null;
let trendsChart = null;
let volumeChart = null;

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Load initial data
        await Promise.all([
            loadStatistics(),
            loadMessages(),
            loadCharts(),
            loadTopEntities()
        ]);

        // Set up event listeners
        setupEventListeners();
    } catch (error) {
        console.error('Error initializing dashboard:', error);
        showError('Failed to load dashboard data. Please try refreshing the page.');
    }
});

// Load and display statistics
async function loadStatistics() {
    try {
        const response = await fetch(ENDPOINTS.statistics);
        const data = await response.json();
        
        // Update summary cards
        document.getElementById('totalMessages').textContent = data.total_messages.toLocaleString();
        document.getElementById('totalTransactions').textContent = data.total_transactions.toLocaleString();
        document.getElementById('totalVolume').textContent = `${data.total_volume.toLocaleString()} RWF`;
        document.getElementById('avgTransaction').textContent = `${data.avg_transaction.toLocaleString()} RWF`;
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Load and display messages
async function loadMessages() {
    try {
        const response = await fetch(ENDPOINTS.messages);
        const data = await response.json();
        
        const tbody = document.getElementById('messagesTableBody');
        tbody.innerHTML = '';
        
        data.messages.forEach(message => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${new Date(message.timestamp).toLocaleString()}</td>
                <td>${message.category}</td>
                <td>${message.transaction_amount ? `${message.transaction_amount.toLocaleString()} ${message.currency}` : '-'}</td>
                <td>${message.recipient_name || message.sender_phone}</td>
                <td>${message.new_balance ? `${message.new_balance.toLocaleString()} ${message.currency}` : '-'}</td>
                <td>${message.message_body.substring(0, 50)}...</td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading messages:', error);
    }
}

// Load and display charts
async function loadCharts() {
    try {
        const [categoriesResponse, trendsResponse, volumeResponse] = await Promise.all([
            fetch(ENDPOINTS.categories),
            fetch(ENDPOINTS.trends),
            fetch(ENDPOINTS.volume)
        ]);

        const categoriesData = await categoriesResponse.json();
        const trendsData = await trendsResponse.json();
        const volumeData = await volumeResponse.json();
        
        // Create charts
        createCategoryChart(categoriesData);
        createTrendsChart(trendsData);
        createVolumeChart(volumeData);
    } catch (error) {
        console.error('Error loading charts:', error);
    }
}

// Create category pie chart
function createCategoryChart(data) {
    const ctx = document.getElementById('categoryChart').getContext('2d');
    categoryChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(data),
            datasets: [{
                data: Object.values(data),
                backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
                    '#FF9F40', '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right'
                }
            }
        }
    });
}

// Create trends line chart
function createTrendsChart(data) {
    const ctx = document.getElementById('trendsChart').getContext('2d');
    trendsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: 'Daily Transactions',
                data: Object.values(data),
                borderColor: '#36A2EB',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Create volume bar chart
function createVolumeChart(data) {
    const ctx = document.getElementById('volumeChart').getContext('2d');
    volumeChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: 'Daily Transaction Volume (RWF)',
                data: Object.values(data),
                backgroundColor: '#4BC0C0'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: value => `${value.toLocaleString()} RWF`
                    }
                }
            }
        }
    });
}

// Load and display top entities
async function loadTopEntities() {
    try {
        const [recipientsResponse, sendersResponse] = await Promise.all([
            fetch(ENDPOINTS.topRecipients),
            fetch(ENDPOINTS.topSenders)
        ]);

        const recipientsData = await recipientsResponse.json();
        const sendersData = await sendersResponse.json();
        
        // Display top recipients
        const topRecipientsDiv = document.getElementById('topRecipients');
        topRecipientsDiv.innerHTML = Object.entries(recipientsData)
            .map(([name, amount]) => `
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span>${name}</span>
                    <span class="badge bg-primary">${amount.toLocaleString()} RWF</span>
                </div>
            `).join('');
        
        // Display top senders
        const topSendersDiv = document.getElementById('topSenders');
        topSendersDiv.innerHTML = Object.entries(sendersData)
            .map(([name, amount]) => `
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span>${name}</span>
                    <span class="badge bg-primary">${amount.toLocaleString()} RWF</span>
                </div>
            `).join('');
    } catch (error) {
        console.error('Error loading top entities:', error);
    }
}

// Set up event listeners
function setupEventListeners() {
    // Date range filters
    document.getElementById('startDate').addEventListener('change', applyFilters);
    document.getElementById('endDate').addEventListener('change', applyFilters);
    
    // Category filter
    document.getElementById('categoryFilter').addEventListener('change', applyFilters);
    
    // Search input
    document.getElementById('searchInput').addEventListener('input', debounce(applyFilters, 300));
}

// Apply filters
async function applyFilters() {
    try {
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;
        const category = document.getElementById('categoryFilter').value;
        const search = document.getElementById('searchInput').value;
        
        // Build query parameters
        const params = new URLSearchParams();
        if (startDate) params.append('start_date', startDate);
        if (endDate) params.append('end_date', endDate);
        if (category) params.append('category', category);
        if (search) params.append('search', search);
        
        // Fetch filtered messages
        const response = await fetch(`${ENDPOINTS.messages}?${params.toString()}`);
        const data = await response.json();
        
        // Update display
        updateMessagesTable(data.messages);
        
        // Reload charts with filtered data
        await loadCharts();
    } catch (error) {
        console.error('Error applying filters:', error);
    }
}

// Clear filters
function clearFilters() {
    document.getElementById('startDate').value = '';
    document.getElementById('endDate').value = '';
    document.getElementById('categoryFilter').value = '';
    document.getElementById('searchInput').value = '';
    applyFilters();
}

// Update messages table with filtered data
function updateMessagesTable(messages) {
    const tbody = document.getElementById('messagesTableBody');
    tbody.innerHTML = '';
    
    messages.forEach(message => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${new Date(message.timestamp).toLocaleString()}</td>
            <td>${message.category}</td>
            <td>${message.transaction_amount ? `${message.transaction_amount.toLocaleString()} ${message.currency}` : '-'}</td>
            <td>${message.recipient_name || message.sender_phone}</td>
            <td>${message.new_balance ? `${message.new_balance.toLocaleString()} ${message.currency}` : '-'}</td>
            <td>${message.message_body.substring(0, 50)}...</td>
        `;
        tbody.appendChild(row);
    });
}

// Utility function for debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Show error message
function showError(message) {
    // You can implement a more sophisticated error display
    alert(message);
}
