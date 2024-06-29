var map = L.map('map').setView([35.70072333, 51.38072233], 20);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

var redIcon = L.divIcon({
    className: 'leaflet-div-icon',
    html: '<i class=" fs-1 fa-solid fa-location-dot"></i>',
    iconSize: [30, 30],
    iconAnchor: [15, 15]
});
var marker;
map.on('click', function (e) {
    if (marker) {
        map.removeLayer(marker)
    }
    let homeUrl = ''
    marker = L.marker(e.latlng, {icon: redIcon}).addTo(map)
    let lat = e.latlng.lat;
    let lng = e.latlng.lng;
    map.setView(e.latlng, 15);
    $.ajax({
        url: homeUrl,
        type: 'get',
        headers: {'X-CSRFToken': "{{ csrf_token }}"},
        data: {
            'lat': lat,
            'lng': lng
        },
        success: function (data) {

        }
    });
});

jalaliDatepicker.startWatch();