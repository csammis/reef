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
        var $row = $('<tr>').addClass('data').addClass('measurement-type-id-' + config.id)
            .hover(
                    function() { $(this).addClass('entry-hover'); $('.measurement-type-' + config.id).show(); },
                    function() { $(this).removeClass('entry-hover'); $('.measurement-type-' + config.id).hide(); }
                );

        $('<td>').addClass(config.id + '-label').html(config.label).appendTo($row);
        $('<td>').addClass(config.id + '-units').html(config.units).appendTo($row);

        var range_html = '';
        if (config.acceptable_range !== null && config.acceptable_range !== undefined) {
            range_html = Math.min(config.acceptable_range[0], config.acceptable_range[1]) + ' - ' + Math.max(config.acceptable_range[0], config.acceptable_range[1]);
        }
        $('<td>').addClass(config.id + '-range').html(range_html).appendTo($row);

        var $control = $('<span>').addClass('measurement-type-' + config.id).hide();
        $('<a>').attr('href', '#').html('<img src="/static/images/edit.svg" alt="Edit this measurement type" class="icon" />').click(function() {
            onEditMeasurementType(config.id);
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
            .fail(function(data) { alert(data.responseJSON.message); });
        }).appendTo($control);

        $('<td>').addClass(config.id + '-control').append($control).appendTo($row);

        return $row;
    };

    function createJsonForUpdate(labelSelector, unitsSelector, rangeSelector) {
        var range = $(rangeSelector).val();
        var ranges = range.split('-');
        for (i = 0; i < ranges.length; i++) {
            ranges[i] = ranges[i].trim();
        }
        
        var config = {
            'label': $(labelSelector).val(),
            'units': $(unitsSelector).val(),
            'rangeHtml': range
        };

        if (range.length != 0) {
            config['acceptable_range'] = ranges;
        }

        return config;
    }

    function onEditMeasurementType(id) {
        var originals = {
            labelElement: $('.' + id + '-label'),
            label: $('.' + id + '-label').html(),
            unitsElement: $('.' + id + '-units'),
            units: $('.' + id + '-units').html(),
            rangeElement: $('.' + id + '-range'),
            range: $('.' + id + '-range').html(),
            controlElement: $('.' + id + '-control'),
            controlSpan: $('.measurement-type-' + id)
        };

        var finished = function() {
            originals.labelElement.empty().html(originals.label);
            originals.unitsElement.empty().html(originals.units)
            originals.rangeElement.empty().html(originals.range);
            originals.controlElement.empty().append(originals.controlSpan);
        };

        var submitEdit = function() {
            var newConfig = createJsonForUpdate('#inline-edit-label-' + id, '#inline-edit-units-' + id, '#inline-edit-range-' + id);
            $.ajax({
                url: '/configs/measurements/' + id,
                type: 'PUT',
                dataType: 'json',
                data: newConfig })
            .done(function() {
                originals.label = newConfig.label;
                originals.units = newConfig.units;
                originals.range = newConfig.rangeHtml;
                finished();
            })
            .fail(function(data) { alert('Unable to update measurement type: ' + data.responseJSON.message); });
        };

        originals.labelElement.empty()
            .append('<input type="text" value="' + originals.label + '" class="inline-edit" id="inline-edit-label-' + id + '" />');
        originals.unitsElement.empty()
            .append('<input type="text" value="' + originals.units + '" class="inline-edit" id="inline-edit-units-' + id + '" />');
        originals.rangeElement.empty()
            .append('<input type="text" value="' + originals.range + '" class="inline-edit" id="inline-edit-range-' + id + '" />');

        bindInputsToKeyHandler('.measurement-type-id-' + id, submitEdit, finished);
        $('#inline-edit-label-' + id).focus().select();

        originals.controlSpan.detach();
        $('<a>').attr('href', '#').html('<img src="/static/images/submit-entry.svg" alt="Save changes" class="icon" />').click(submitEdit).appendTo(originals.controlElement);
        $('<a>').attr('href', '#').html('<img src="/static/images/cancel.svg" alt="Cancel edit" class="icon" />').click(finished).appendTo(originals.controlElement);
    }

    function addNewMeasurement() {
        var config = createJsonForUpdate('#new_measurement_name', '#new_measurement_units', '#new_measurement_range');

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
        .fail(function(data) {
            alert(data.responseJSON.message);
        });
        return false;
    }

    window.onload = function() {
        $('#submit_new_measurement').click(addNewMeasurement);
        bindInputsToKeyHandler('.measurement_new_entry', addNewMeasurement);
        sendConfigRequest();
    };

})();
