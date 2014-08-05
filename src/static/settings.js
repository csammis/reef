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
        var $row = $('<tr>').addClass('data').attr('id', 'measurement-type-id-' + config.id)
            .hover(
                    function() { $(this).addClass('entry-hover'); },
                    function() { $(this).removeClass('entry-hover'); }
                );

        $('<td>').attr('id', 'label-' + config.id).html(config.label).appendTo($row);
        $('<td>').attr('id', 'units-' + config.id).html(config.units).appendTo($row);

        var range_html = '';
        if (config.acceptable_range !== null && config.acceptable_range !== undefined) {
            range_html = Math.min(config.acceptable_range[0], config.acceptable_range[1]) + ' - ' + Math.max(config.acceptable_range[0], config.acceptable_range[1]);
        }
        $('<td>').attr('id', 'range-' + config.id).html(range_html).appendTo($row);

        var $control = $('<span>').attr('id', 'measurement-type-' + config.id);
        $('<button>').append(
                $('<img>').addClass('icon').attr('src','/static/images/edit.svg'))
            .button()
            .addClass('inline-button')
            .click(function() { onEditMeasurementType(config.id); })
            .appendTo($control);

        $('<button>').append(
                $('<img>').addClass('icon').attr('src', '/static/images/delete.svg'))
            .button()
            .addClass('inline-button')
            .click(function() {
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
            })
            .appendTo($control);

        $('<td>').attr('id', 'control-' + config.id).append($control).appendTo($row);

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
            labelElement: $('#label-' + id),
            unitsElement: $('#units-' + id),
            rangeElement: $('#range-' + id),
            controlElement: $('#control-' + id),
            controlSpan: $('#measurement-type-' + id)
        };
        originals['label'] = originals.labelElement.html();
        originals['units'] = originals.unitsElement.html();
        originals['range'] = originals.rangeElement.html();

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
            .append(
                    $('<input>').attr('type', 'text')
                        .attr('id', 'inline-edit-label-' + id)
                        .addClass('inline-edit')
                        .val(originals.label));
        originals.unitsElement.empty()
            .append(
                    $('<input>').attr('type', 'text')
                        .attr('id', 'inline-edit-units-' + id)
                        .addClass('inline-edit')
                        .val(originals.units));
        originals.rangeElement.empty()
            .append(
                    $('<input>').attr('type', 'text')
                        .attr('id', 'inline-edit-range-' + id)
                        .addClass('inline-edit')
                        .val(originals.range));

        bindInputsToKeyHandler('#measurement-type-id-' + id, submitEdit, finished);
        $('#inline-edit-label-' + id).focus().select();

        originals.controlSpan.detach();
        $('<button>').append(
                $('<img>').addClass('icon').attr('src', '/static/images/submit-entry.svg'))
            .button()
            .addClass('inline-button')
            .click(submitEdit)
            .appendTo(originals.controlElement);

        $('<button>').append(
                $('<img>').addClass('icon').attr('src', '/static/images/cancel.svg'))
            .button()
            .addClass('inline-button')
            .click(finished)
            .appendTo(originals.controlElement);
    }

    function addNewMeasurement() {
        var config = createJsonForUpdate('#new_measurement_name', '#new_measurement_units', '#new_measurement_range');

        $.ajax({
            url: '/configs/measurements',
            type: 'POST',
            dataType: 'json',
            data: config})
        .done(function(json) {
            buildMeasurementType(json.measurement_type)
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
        $('#submit_new_measurement').button().click(addNewMeasurement);
        bindInputsToKeyHandler('.measurement_new_entry', addNewMeasurement);
        sendConfigRequest();
    };

})();
