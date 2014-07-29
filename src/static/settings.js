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
            $('#measurements_grid').append(buildMeasurementType(config));
        }
    };

    function buildMeasurementType(config) {
        var $row = $('<tr>').addClass('data')
            .hover(
                    function() { $(this).addClass('entry-hover'); $('.measurement-type-' + config.id).show(); },
                    function() { $(this).removeClass('entry-hover'); $('.measurement-type-' + config.id).hide(); }
                );

        $('<td>').html(config.label).appendTo($row);
        $('<td>').html(config.units).appendTo($row);

        var range_html = '';
        if (config.acceptable_range !== null && config.acceptable_range !== undefined) {
            range_html = Math.min(config.acceptable_range[0], config.acceptable_range[1]) + ' - ' + Math.max(config.acceptable_range[0], config.acceptable_range[1]);
        }
        $('<td>').html(range_html).appendTo($row);

        var $control = $('<span>').addClass('measurement-type-' + config.id).hide();
        $('<a>').attr('href', '#').html('<img src="/static/images/edit.svg" alt="Edit this measurement type" class="icon" />').click(function() {
            
        }).appendTo($control);
        $('<a>').attr('href', '#').html('<img src="/static/images/delete.svg" alt="Delete this measurement type" class="icon" />').click(function() {
            $.ajax({
                url: '/configs/measurements/' + config.id,
                type: 'DELETE',
                dataType: 'json'})
            .done(function(json) {
                $row.fadeOut({
                    complete: function() { $(this).remove(); }
                });
            })
            .fail(function(data) { alert(data.message); });
        }).appendTo($control);

        $('<td>').append($control).appendTo($row);

        return $row;
    };

    function addNewMeasurement() {
        var label = $('#new_measurement_name').val();
        var units = $('#new_measurement_units').val();
        var range = $('#new_measurement_range').val();

        var ranges = range.split('-');
        for (var i = 0; i < ranges.length; i++) {
            ranges[i] = ranges[i].trim();
        }

        var config = {
            'label': label,
            'units': units
        };
        if (range.length != 0) {
            config['acceptable_range'] = ranges;
        }

        $.ajax({
            url: '/configs/measurements',
            type: 'POST',
            dataType: 'json',
            data: config})
        .done(function(json) {
            buildMeasurementType(config)
                .hide()
                .appendTo($('#measurements_grid'))
                .fadeIn();
            $('#new_measurement_name').val('').focus();
            $('#new_measurement_units').val('');
            $('#new_measurement_range').val('');
        })
        .fail(function(data) { alert(data); });
        return false;
    }

    window.onload = function() {
        $('#submit_new_measurement').click(addNewMeasurement);
        sendConfigRequest();
    };
})();
