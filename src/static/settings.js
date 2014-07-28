(function() {

    function sendConfigRequest() {
        $.ajax({
            url: '/configs/measurements',
            type: 'GET',
            dataType: 'json'})
        .done(function(json) { buildMeasurementTypes(json); })
        .fail(function() { alert('Failed to get configured measurement types'); });
    };

    function buildMeasurementTypes(json) {
        $('#measurements_grid').children('tr.data').remove();
        for (var i = 0; i < json.configs.length; i++) {
            var config = json.configs[i];
            buildMeasurementType(config);
        }
    };

    function buildMeasurementType(config) {
        var $row = $('<tr>').addClass('data');

        $('<td>').html(config.label).appendTo($row);
        $('<td>').html(config.units).appendTo($row);

        var range_html = '';
        if (config.acceptable_range !== null) {
            range_html = Math.min(config.acceptable_range[0], config.acceptable_range[1]) + ' - ' + Math.max(config.acceptable_range[0], config.acceptable_range[1]);
        }
        $('<td>').html(range_html).appendTo($row);

        $('#measurements_grid').append($row);
    };

    window.onload = function() {
        sendConfigRequest();
    };
})();
