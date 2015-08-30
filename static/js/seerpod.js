var autocomplete;
function initialize() {
    autocomplete = new google.maps.places.Autocomplete(
    /** @type {HTMLInputElement} */(document.getElementById('autocomplete')),
    { types: ['geocode'] });
        google.maps.event.addListener(autocomplete, 'place_changed', function() {
    });
}

google.maps.event.addDomListener(window, 'load', initialize);

var x = document.getElementById("autocomplete");

$.fn.spin = function(opts) {
    this.each(function() {
        var $this = $(this),
        spinner = $this.data('spinner');
        if (spinner) spinner.stop();
        if (opts !== false) {
            opts = $.extend({color: $this.css('color')}, opts);
            spinner = new Spinner(opts).spin(this);
            $this.data('spinner', spinner);
        }
	});
	return this;
};

function getLocation() {
    var opts = {
	    lines: 10, // The number of lines to draw
	    length: 5, // The length of each line
		width: 4, // The line thickness
		radius: 5, // The radius of the inner circle
		color: '#fff', // #rbg or #rrggbb
		speed: 0.5, // Rounds per second
		trail: 66, // Afterglow percentage
		shadow: true // Whether to render a shadow
	};

    $("#home-address-search").hide()
    $("#spinner").show().spin(opts);

    x.placeholder = 'Using your current Location';
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(getReverseGeocodingData);
    }
}

function getReverseGeocodingData(position) {

    var latlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
    // This is making the Geocode request
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode({ 'latLng': latlng }, function (results, status) {
        if (status !== google.maps.GeocoderStatus.OK) {
            alert(status);
        }
        // This is checking to see if the Geoeode Status is OK before proceeding
        if (status == google.maps.GeocoderStatus.OK) {
            console.log(results);
            var address = (results[0].formatted_address);
             x.value = address;
            $("#spinner").hide()
             $("#home-address-search").show()
        }
    });
}