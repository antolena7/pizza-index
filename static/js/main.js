// Main JavaScript for Pizza Index functionality

// Copy link functionality
document.addEventListener('DOMContentLoaded', function() {
    const copyLinkBtn = document.getElementById('copyLinkBtn');
    const copySuccess = document.getElementById('copySuccess');
    
    if (copyLinkBtn) {
        copyLinkBtn.addEventListener('click', function() {
            // Copy current URL to clipboard
            navigator.clipboard.writeText(window.location.href).then(function() {
                // Show success message
                copySuccess.style.display = 'block';
                setTimeout(function() {
                    copySuccess.style.display = 'none';
                }, 3000);
            }).catch(function(err) {
                console.error('Failed to copy link: ', err);
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = window.location.href;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                
                copySuccess.style.display = 'block';
                setTimeout(function() {
                    copySuccess.style.display = 'none';
                }, 3000);
            });
        });
    }
});

// Auto-refresh pizza watch data
function updatePizzaWatch() {
    fetch('/api/pizza-data')
        .then(response => response.json())
        .then(data => {
            const pizzaWatchList = document.querySelector('.pizza-watch-list');
            if (pizzaWatchList && data && data.length > 0) {
                pizzaWatchList.innerHTML = '';
                
                data.forEach(item => {
                    const watchItem = document.createElement('div');
                    watchItem.className = 'pizza-watch-item mb-2';
                    watchItem.innerHTML = `
                        <strong class="text-warning">${item.outlet} – ${item.address}:</strong>
                        <span class="text-light">${item.busy_level} at ${item.timestamp}</span>
                    `;
                    pizzaWatchList.appendChild(watchItem);
                });
            }
        })
        .catch(error => {
            console.error('Error updating pizza watch:', error);
        });
}

// Auto-refresh news feed
function updateNewsFeed() {
    fetch('/api/news-feed')
        .then(response => response.json())
        .then(data => {
            const newsFeed = document.querySelector('.news-feed');
            if (newsFeed && data && data.length > 0) {
                newsFeed.innerHTML = '';
                
                data.forEach(article => {
                    const newsItem = document.createElement('div');
                    newsItem.className = 'news-item mb-4';
                    newsItem.innerHTML = `
                        <h4 class="h5 text-warning">${article.source}: ${article.title}</h4>
                        <p class="text-muted"><em>${article.published_date}</em></p>
                        <p class="text-light"><strong>Why it matters:</strong> ${article.description}</p>
                        <a href="${article.url}" target="_blank" class="text-warning">Read more</a>
                    `;
                    newsFeed.appendChild(newsItem);
                });
            }
        })
        .catch(error => {
            console.error('Error updating news feed:', error);
        });
}

// Start periodic updates
function startDataUpdates() {
    // Update pizza watch every 5 minutes
    setInterval(updatePizzaWatch, 300000);
    
    // Update news feed every 10 minutes
    setInterval(updateNewsFeed, 600000);
}

// Initialize updates when page loads
document.addEventListener('DOMContentLoaded', function() {
    startDataUpdates();
    
    // Add loading indicators for dynamic content
    const pizzaWatchSection = document.querySelector('.pizza-watch-list');
    const newsFeedSection = document.querySelector('.news-feed');
    
    if (pizzaWatchSection) {
        pizzaWatchSection.addEventListener('update-start', function() {
            this.classList.add('loading');
        });
        
        pizzaWatchSection.addEventListener('update-end', function() {
            this.classList.remove('loading');
        });
    }
    
    if (newsFeedSection) {
        newsFeedSection.addEventListener('update-start', function() {
            this.classList.add('loading');
        });
        
        newsFeedSection.addEventListener('update-end', function() {
            this.classList.remove('loading');
        });
    }
});

// Handle share button interactions
document.addEventListener('DOMContentLoaded', function() {
    const shareButtons = document.querySelectorAll('.share-buttons a, .share-buttons button');
    
    shareButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add visual feedback
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });
});

// Add keyboard navigation support
document.addEventListener('keydown', function(e) {
    // Press 'R' to refresh data
    if (e.key === 'r' || e.key === 'R') {
        if (!e.ctrlKey && !e.metaKey) {
            e.preventDefault();
            updatePizzaWatch();
            updateNewsFeed();
        }
    }
    
    // Press 'C' to copy link
    if (e.key === 'c' || e.key === 'C') {
        if (!e.ctrlKey && !e.metaKey) {
            const copyBtn = document.getElementById('copyLinkBtn');
            if (copyBtn) {
                copyBtn.click();
            }
        }
    }
});

// Add visual feedback for real-time updates
function showUpdateNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'alert alert-info position-fixed';
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 300px;';
    notification.innerHTML = `
        <i class="fas fa-sync-alt fa-spin"></i> ${message}
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Error handling for failed requests
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    
    // Show user-friendly error message
    const errorNotification = document.createElement('div');
    errorNotification.className = 'alert alert-warning position-fixed';
    errorNotification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 300px;';
    errorNotification.innerHTML = `
        <i class="fas fa-exclamation-triangle"></i> Data update failed. Retrying...
    `;
    
    document.body.appendChild(errorNotification);
    
    setTimeout(() => {
        errorNotification.remove();
    }, 5000);
});

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', function() {
        setTimeout(function() {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
        }, 0);
    });
}
