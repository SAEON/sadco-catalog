function createStationsMap(stations, n, e, s, w) {
    $('#map').height('500px');

    const map = _initMap(n, e, s, w);

    const bounds = [[n, e], [s, w]];
    map.fitBounds(bounds, {
        animate: false,
        maxZoom: 9
    });

    stations.forEach((station) => {
            var latlng = L.latLng(station['latitude'], station['longitude']);
            L.circleMarker(latlng, {radius: 2, fillColor: 'red', color: 'red', fillOpacity: 1}).addTo(map);
        }
    );
}

function clearSearchFilters() {
    $('#survey_id').val('');
    $('#n').val('');
    $('#e').val('');
    $('#s').val('');
    $('#w').val('');
    $('#after').val('');
    $('#before').val('');
    $('#exclusive_region').val('');
    $('#exclusive_interval').val('');
}
