// Pentagon Pizza Surveillance Map
let map;
let pizzaOutlets = [];
const PENTAGON_COORDS = [38.8719, -77.0563];

// Initialize map
function initMap() {
    // Create map centered on Pentagon
    map = L.map('map').setView(PENTAGON_COORDS, 13);
    
    // Add dark tile layer for OSINT aesthetic
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 18,
    }).addTo(map);
    
    // Add Pentagon marker
    const pentagonIcon = L.divIcon({
        className: 'pentagon-marker',
        html: '<div style="background-color: #dc3545; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">🏛️ Pentagon</div>',
        iconSize: [80, 30],
        iconAnchor: [40, 15]
    });
    
    L.marker(PENTAGON_COORDS, { icon: pentagonIcon })
        .addTo(map)
        .bindPopup('<strong>The Pentagon</strong><br>Arlington, VA<br><em>Ground Zero for Pizza Intelligence</em>');
    
    // Load pizza outlets
    loadPizzaOutlets();
}

// Load pizza outlets from API
async function loadPizzaOutlets() {
    try {
        const response = await fetch('/api/outlets');
        const outlets = await response.json();
        
        pizzaOutlets = outlets;
        displayPizzaOutlets(outlets);
    } catch (error) {
        console.error('Error loading pizza outlets:', error);
        // Fallback to default outlets
        loadDefaultOutlets();
    }
}

// Display pizza outlets on map
function displayPizzaOutlets(outlets) {
    outlets.forEach(outlet => {
        const activityLevel = outlet.latest_activity.activity_score || 0;
        const busyLevel = outlet.latest_activity.busy_level || 'unknown';
        
        // Color code based on activity level
        let markerColor = '#6c757d'; // default gray
        if (activityLevel >= 80) {
            markerColor = '#dc3545'; // red - very busy
        } else if (activityLevel >= 60) {
            markerColor = '#fd7e14'; // orange - busy
        } else if (activityLevel >= 40) {
            markerColor = '#ffc107'; // yellow - moderate
        } else if (activityLevel > 0) {
            markerColor = '#28a745'; // green - not busy
        }
        
        // Create custom pizza marker
        const pizzaIcon = L.divIcon({
            className: 'pizza-marker',
            html: `<div style="background-color: ${markerColor}; color: white; padding: 2px 6px; border-radius: 50%; font-size: 14px; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">🍕</div>`,
            iconSize: [30, 30],
            iconAnchor: [15, 15]
        });
        
        // Calculate distance from Pentagon
        const distance = calculateDistance(
            PENTAGON_COORDS[0], PENTAGON_COORDS[1],
            outlet.latitude, outlet.longitude
        );
        
        // Create popup content
        const popupContent = `
            <div style="color: #c9d1d9; background-color: #161b22; padding: 10px; border-radius: 6px; min-width: 250px;">
                <h5 style="color: #f0ad4e; margin-bottom: 10px;">${outlet.name}</h5>
                <p style="margin-bottom: 8px;"><strong>Address:</strong> ${outlet.address}</p>
                <p style="margin-bottom: 8px;"><strong>Distance from Pentagon:</strong> ${distance.toFixed(1)} km</p>
                <p style="margin-bottom: 8px;"><strong>Current Status:</strong> 
                    <span style="color: ${markerColor}; font-weight: bold;">${busyLevel}</span>
                </p>
                <p style="margin-bottom: 8px;"><strong>Activity Score:</strong> ${activityLevel}/100</p>
                ${outlet.rating ? `<p style="margin-bottom: 8px;"><strong>Rating:</strong> ${'⭐'.repeat(Math.floor(outlet.rating))} (${outlet.rating})</p>` : ''}
                <p style="margin-bottom: 0; font-size: 12px; color: #7d8590;">
                    Last updated: ${outlet.latest_activity.timestamp ? new Date(outlet.latest_activity.timestamp).toLocaleString() : 'Unknown'}
                </p>
            </div>
        `;
        
        // Add marker to map
        L.marker([outlet.latitude, outlet.longitude], { icon: pizzaIcon })
            .addTo(map)
            .bindPopup(popupContent);
    });
}

// Load default outlets if API fails
function loadDefaultOutlets() {
    const defaultOutlets = [
        {
            name: 'Extreme Pizza',
            address: '1419 S Fern St, Arlington, VA',
            latitude: 38.8625,
            longitude: -77.0647,
            latest_activity: { busy_level: 'a bit busier than usual', activity_score: 75 }
        },
        {
            name: 'We, The Pizza',
            address: '2100 Crystal Dr, Arlington, VA',
            latitude: 38.8583,
            longitude: -77.0492,
            latest_activity: { busy_level: 'less busy than usual', activity_score: 35 }
        },
        {
            name: 'District Pizza Palace',
            address: '2325 S Eads St, Arlington, VA',
            latitude: 38.8542,
            longitude: -77.0575,
            latest_activity: { busy_level: 'less busy than usual', activity_score: 30 }
        },
        {
            name: 'California Pizza Kitchen',
            address: '1201 S Hayes St, Arlington, VA',
            latitude: 38.8653,
            longitude: -77.0603,
            latest_activity: { busy_level: 'not busy', activity_score: 20 }
        },
        {
            name: 'Domino\'s Pizza - S Ball St',
            address: '3535 S Ball St, Arlington, VA',
            latitude: 38.8456,
            longitude: -77.0789,
            latest_activity: { busy_level: 'less busy than usual', activity_score: 25 }
        },
        {
            name: 'Domino\'s Pizza - K St NW',
            address: '2029 K St NW, Washington, DC',
            latitude: 38.9026,
            longitude: -77.0459,
            latest_activity: { busy_level: 'less busy than usual', activity_score: 40 }
        }
    ];
    
    displayPizzaOutlets(defaultOutlets);
}

// Calculate distance between two coordinates (in km)
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Radius of the Earth in km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = 
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
        Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
}

// Update map data periodically
function startMapUpdates() {
    setInterval(() => {
        loadPizzaOutlets();
    }, 300000); // Update every 5 minutes
}

// Initialize map when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initMap();
    startMapUpdates();
});
