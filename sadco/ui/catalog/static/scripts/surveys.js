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
            L.circleMarker(latlng, {radius: 1}).addTo(map);
        }
    );
}