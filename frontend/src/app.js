// Configuration
const API_URL = 'http://localhost:5000/api';

// State
let state = {
    initialized: false,
    modelsTrained: false,
    historicalChart: null,
    predictionsChart: null
};

// DOM Elements
const elements = {
    initBtn: document.getElementById('initBtn'),
    trainBtn: document.getElementById('trainBtn'),
    refreshBtn: document.getElementById('refreshBtn'),
    predictBtn: document.getElementById('predictBtn'),
    predictionDays: document.getElementById('predictionDays'),
    statusIndicator: document.getElementById('status-indicator'),
    loadingOverlay: document.getElementById('loadingOverlay'),
    currentPrice: document.getElementById('currentPrice'),
    priceHigh: document.getElementById('priceHigh'),
    priceLow: document.getElementById('priceLow'),
    priceVolume: document.getElementById('priceVolume'),
    priceDate: document.getElementById('priceDate'),
    indicators: document.getElementById('indicators'),
    modelStatus: document.getElementById('modelStatus')
};

// Utility Functions
function showLoading() {
    elements.loadingOverlay.style.display = 'flex';
}

function hideLoading() {
    elements.loadingOverlay.style.display = 'none';
}

function updateStatus(message, isConnected = false) {
    elements.statusIndicator.textContent = message;
    if (isConnected) {
        elements.statusIndicator.classList.add('connected');
        elements.statusIndicator.textContent = '🟢 ' + message;
    } else {
        elements.statusIndicator.classList.remove('connected');
        elements.statusIndicator.textContent = '⚪ ' + message;
    }
}

function formatNumber(num, decimals = 2) {
    return Number(num).toFixed(decimals);
}

function formatVolume(volume) {
    if (volume >= 1000000) {
        return (volume / 1000000).toFixed(2) + 'M';
    } else if (volume >= 1000) {
        return (volume / 1000).toFixed(2) + 'K';
    }
    return volume.toString();
}

// API Functions
async function apiCall(endpoint, method = 'GET', body = null) {
    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            }
        };

        if (body) {
            options.body = JSON.stringify(body);
        }

        const response = await fetch(`${API_URL}${endpoint}`, options);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'API request failed');
        }

        return data;
    } catch (error) {
        console.error('API Error:', error);
        alert(`Error: ${error.message}`);
        throw error;
    }
}

// Initialize System
async function initialize() {
    showLoading();
    updateStatus('Initializing...');

    try {
        await apiCall('/initialize', 'POST', {
            ticker: '^AXJO',
            start_date: '2018-01-01'
        });

        state.initialized = true;
        updateStatus('System Initialized', true);

        // Enable buttons
        elements.trainBtn.disabled = false;
        elements.refreshBtn.disabled = false;

        // Load initial data
        await loadCurrentPrice();
        await loadHistoricalData();
        await loadIndicators();

        alert('System initialized successfully! You can now train models.');
    } catch (error) {
        updateStatus('Initialization Failed');
    } finally {
        hideLoading();
    }
}

// Train Models
async function trainModels() {
    showLoading();
    updateStatus('Training Models...');

    try {
        const result = await apiCall('/train', 'POST', {
            train_ratio: 0.8
        });

        state.modelsTrained = true;
        updateStatus('Models Trained', true);

        // Enable predict button
        elements.predictBtn.disabled = false;

        // Update model status
        updateModelStatus(result.details);

        alert(`Models trained successfully!\nModels: ${result.details.models_trained.join(', ')}`);
    } catch (error) {
        updateStatus('Training Failed');
    } finally {
        hideLoading();
    }
}

// Load Current Price
async function loadCurrentPrice() {
    try {
        const result = await apiCall('/current');

        if (result.status === 'success' && result.data) {
            const data = result.data;
            elements.currentPrice.querySelector('.price-value').textContent = `$${formatNumber(data.close)}`;
            elements.priceHigh.textContent = `$${formatNumber(data.high)}`;
            elements.priceLow.textContent = `$${formatNumber(data.low)}`;
            elements.priceVolume.textContent = formatVolume(data.volume);
            elements.priceDate.textContent = data.date;
        }
    } catch (error) {
        console.error('Error loading current price:', error);
    }
}

// Load Historical Data
async function loadHistoricalData() {
    try {
        const result = await apiCall('/historical?days=30');

        if (result.status === 'success' && result.data) {
            renderHistoricalChart(result.data);
        }
    } catch (error) {
        console.error('Error loading historical data:', error);
    }
}

// Load Indicators
async function loadIndicators() {
    try {
        const result = await apiCall('/indicators');

        if (result.status === 'success' && result.indicators) {
            const indicators = result.indicators;

            document.getElementById('rsi').textContent = indicators.RSI ? formatNumber(indicators.RSI) : '-';
            document.getElementById('macd').textContent = indicators.MACD ? formatNumber(indicators.MACD) : '-';
            document.getElementById('atr').textContent = indicators.ATR ? formatNumber(indicators.ATR) : '-';
            document.getElementById('stochastic').textContent = indicators['Stochastic_%K'] ? formatNumber(indicators['Stochastic_%K']) : '-';
        }
    } catch (error) {
        console.error('Error loading indicators:', error);
    }
}

// Get Predictions
async function getPredictions() {
    showLoading();

    try {
        const days = parseInt(elements.predictionDays.value);
        const result = await apiCall(`/predict?days=${days}`);

        if (result.status === 'success' && result.predictions) {
            renderPredictionsChart(result.predictions);
            alert('Predictions generated successfully!');
        }
    } catch (error) {
        alert('Error generating predictions');
    } finally {
        hideLoading();
    }
}

// Refresh Data
async function refreshData() {
    showLoading();
    updateStatus('Refreshing Data...');

    try {
        await apiCall('/refresh', 'POST');

        await loadCurrentPrice();
        await loadHistoricalData();
        await loadIndicators();

        updateStatus('Data Refreshed', true);
        alert('Data refreshed successfully!');
    } catch (error) {
        updateStatus('Refresh Failed');
    } finally {
        hideLoading();
    }
}

// Update Model Status
function updateModelStatus(details) {
    if (details && details.models_trained) {
        const models = details.models_trained;
        const statusHTML = models.map(model => `
            <div class="model-item">
                <span class="model-name">${model.toUpperCase()}:</span>
                <span class="model-status">✅ Trained</span>
            </div>
        `).join('');

        elements.modelStatus.innerHTML = statusHTML;
    }
}

// Render Historical Chart
function renderHistoricalChart(data) {
    const ctx = document.getElementById('historicalChart');

    // Destroy existing chart
    if (state.historicalChart) {
        state.historicalChart.destroy();
    }

    state.historicalChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: 'Close Price',
                data: data.close,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 2,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        }
                    }
                }
            }
        }
    });
}

// Render Predictions Chart
function renderPredictionsChart(predictions) {
    const ctx = document.getElementById('predictionsChart');

    // Destroy existing chart
    if (state.predictionsChart) {
        state.predictionsChart.destroy();
    }

    // Prepare datasets
    const datasets = [];
    const colors = {
        arima: '#667eea',
        sarima: '#764ba2',
        ml: '#f093fb',
        ensemble: '#4facfe'
    };

    for (const [model, data] of Object.entries(predictions)) {
        datasets.push({
            label: model.toUpperCase(),
            data: data.prices,
            borderColor: colors[model] || '#999',
            backgroundColor: 'transparent',
            borderWidth: 2,
            tension: 0.4,
            pointRadius: 4,
            pointHoverRadius: 6
        });
    }

    // Use the first prediction's dates
    const labels = Object.values(predictions)[0].dates;

    state.predictionsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': $' + context.parsed.y.toFixed(2);
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        }
                    }
                }
            }
        }
    });
}

// Event Listeners
elements.initBtn.addEventListener('click', initialize);
elements.trainBtn.addEventListener('click', trainModels);
elements.refreshBtn.addEventListener('click', refreshData);
elements.predictBtn.addEventListener('click', getPredictions);

// Check API health on load
async function checkHealth() {
    try {
        const result = await fetch(`${API_URL}/health`);
        const data = await result.json();
        if (data.status === 'healthy') {
            updateStatus('API Connected', true);
        }
    } catch (error) {
        updateStatus('API Not Available');
        console.error('API health check failed:', error);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    checkHealth();
});
