// Function to create a line chart for test scores
function createScoresChart(canvasId, labels, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(242, 150, 13, 0.4)');
    gradient.addColorStop(1, 'rgba(242, 150, 13, 0)');

    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Test Scores',
                data: data,
                borderColor: '#f2960d',
                borderWidth: 2,
                tension: 0.4,
                fill: true,
                backgroundColor: gradient,
                pointBackgroundColor: '#f2960d',
                pointBorderColor: '#fff',
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 2000,
                easing: 'easeInOutQuart'
            },
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: {
                        color: '#e8decf'
                    },
                    ticks: {
                        font: {
                            family: 'Inter'
                        },
                        color: '#9c7a4a'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            family: 'Inter'
                        },
                        color: '#9c7a4a'
                    }
                }
            }
        }
    });
}

// Function to create a doughnut chart for subject completion
function createSubjectChart(canvasId, labels, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');

    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    '#f2960d',
                    '#9c7a4a',
                    '#08870f',
                    '#e8decf'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 2000,
                easing: 'easeInOutQuart'
            },
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: '#1c170d',
                        padding: 10,
                        font: {
                            family: 'Inter',
                            size: 12
                        }
                    }
                }
            },
            cutout: '70%'
        }
    });
}

// Fetch dashboard data and initialize charts
async function loadDashboardData() {
    try {
        const response = await fetch('/api/dashboard-data/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include'
        });

        if (!response.ok) {
            console.error('Failed to fetch dashboard data');
            // Use fallback data if API fails
            useFallbackData();
            return;
        }

        const data = await response.json();
        
        // Use real data if available, otherwise use fallback
        if (data.scores && data.scores.labels.length > 0) {
            createScoresChart('scoresChart', data.scores.labels, data.scores.data);
        } else {
            // Fallback data for scores
            createScoresChart('scoresChart', ['No Data'], [0]);
        }

        if (data.subjects && data.subjects.labels.length > 0) {
            createSubjectChart('subjectChart', data.subjects.labels, data.subjects.data);
        } else {
            // Fallback data for subjects
            createSubjectChart('subjectChart', ['No Data'], [100]);
        }
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        useFallbackData();
    }
}

// Fallback function with dummy data
function useFallbackData() {
    const weekLabels = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
    const scoreData = [75, 82, 68, 90];
    createScoresChart('scoresChart', weekLabels, scoreData);

    const subjectLabels = ['Math', 'Science', 'English', 'History'];
    const completionData = [85, 78, 92, 70];
    createSubjectChart('subjectChart', subjectLabels, completionData);
}

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function () {
    loadDashboardData();
});