(function() {

    function sendConfigRequests() {
        doJqueryAjax('/configs/measurements', 'GET', function(json) {
            var $grid = $('#measurements_grid');
            $grid.children('tr.data').remove();
            for (var i = 0; i < json.configs.length; i++) {
                $('#measurements_grid').append(buildMeasurementType(json.configs[i]));
            }
        });
       
        doJqueryAjax('/configs/tanks', 'GET', function(json) {
            var $grid = $('#tanks_grid');
            $grid.children('tr.data').remove();
            for (var i = 0; i < json.tanks.length; i++) {
                $grid.append(buildTank(json.tanks[i]));
            }
        });
    };

    function buildTank(config) {
        var $row = $('<tr>').addClass('data').attr('id', 'tank-id-' + config.id).hoverize();
        $('<td>').attr('id', 'tank-name-' + config.id).html(config.name).appendTo($row);
        createEditDeleteControlsInRow(config.id, 'tank', $row, onEditTank, onDeleteTank);
        return $row;
    }

    function buildMeasurementType(config) {
        var $row = $('<tr>').addClass('data').attr('id', 'measurement-type-id-' + config.id).hoverize();

        $('<td>').attr('id', 'label-' + config.id).html(config.label).appendTo($row);
        $('<td>').attr('id', 'units-' + config.id).html(config.units).appendTo($row);

        var range_html = '';
        if (config.acceptable_range !== null && config.acceptable_range !== undefined) {
            range_html = Math.min(config.acceptable_range[0], config.acceptable_range[1]) + ' - ' + Math.max(config.acceptable_range[0], config.acceptable_range[1]);
        }
        $('<td>').attr('id', 'range-' + config.id).html(range_html).appendTo($row);
        createEditDeleteControlsInRow(config.id, 'measurement-type', $row, onEditMeasurementType, onDeleteMeasurementType);
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

    function onDeleteMeasurementType() {
        var id = $(this).attr('data');
        doJqueryAjax('/configs/measurements/' + id, 'DELETE', function(json) { $('#measurement-type-id-' + id).fadeRemove(); });
    }

    function onDeleteTank() {
        var id = $(this).attr('data');
        doJqueryAjax('/configs/tanks/' + id, 'DELETE', function(json) { $('#tank-id-' + id).fadeRemove(); });
    }

    function onEditTank() {
        var id = $(this).attr('data');

        var originals = {
            nameElement: $('#tank-name-' + id),
            controlElement: $('#control-tank-' + id),
            controlSpan: $('#tank-' + id)
        };
        originals['name'] = originals.nameElement.html();

        var finished = function() {
            originals.nameElement.empty().html(originals.name);
            originals.controlElement.empty().append(originals.controlSpan);
        };

        var submitEdit = function() {
            var config = {'name': $('#inline-edit-tank-name-' + id).val()};
            doJqueryAjax('/configs/tanks/' + id, 'PUT', function() {
                originals.name = config.name;
                finished();
            }, config);
        }

        inlineEditize(originals.nameElement, 'inline-edit-tank-name-' + id);
        createSaveCancelControls(originals, submitEdit, finished);
        bindInputsToKeyHandler('#tank-id-' + id, submitEdit, finished);
        $('#inline-edit-tank-name-' + id).focus().select();
    }

    function onEditMeasurementType() {
        var id = $(this).attr('data');

        var originals = {
            labelElement: $('#label-' + id),
            unitsElement: $('#units-' + id),
            rangeElement: $('#range-' + id),
            controlElement: $('#control-measurement-type-' + id),
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
            doJqueryAjax('/configs/measurements/' + id, 'PUT', function() {
                originals.label = newConfig.label;
                originals.units = newConfig.units;
                originals.range = newConfig.rangeHtml;
                finished();
            }, newConfig);
        };

        inlineEditize(originals.labelElement, 'inline-edit-label-' + id);
        inlineEditize(originals.unitsElement, 'inline-edit-units-' + id);
        inlineEditize(originals.rangeElement, 'inline-edit-range-' + id);
        createSaveCancelControls(originals, submitEdit, finished);
        bindInputsToKeyHandler('#measurement-type-id-' + id, submitEdit, finished);
        $('#inline-edit-label-' + id).focus().select();
    }

    function addNewMeasurement() {
        var config = createJsonForUpdate('#new_measurement_name', '#new_measurement_units', '#new_measurement_range');
        doJqueryAjax('/configs/measurements', 'POST', function(json) {
            buildMeasurementType(json.measurement_type).hide().appendTo($('#measurements_grid')).fadeIn();
            $('#new_measurement_name').val('').focus();
            $('#new_measurement_units').val('');
            $('#new_measurement_range').val('');
        }, config);
        return false;
    }

    function addNewTank() {
        var config = {'name': $('#new_tank_name').val() };
        doJqueryAjax('/configs/tanks', 'POST', function(json) {
            buildTank(json.tank).hide().appendTo($('#tanks_grid')).fadeIn();
            $('#new_tank_name').val('').focus();
        }, config);
        return false;
    };

    window.onload = function() {
        $('#submit_new_measurement').button().click(addNewMeasurement);
        $('#submit_new_tank').button().click(addNewTank);
        bindInputsToKeyHandler('.tank_new_entry', addNewTank);
        bindInputsToKeyHandler('.measurement_new_entry', addNewMeasurement);
        $('#tabs').tabs();

        sendConfigRequests();
    };

    // DOM building helper functions
    
    function createEditDeleteControlsInRow(id, forSetting, $tr, editFunction, deleteFunction) {
        var $control = $('<span>').attr('id', forSetting + '-' + id);

        $('<button>').append(
                $('<img>').addClass('icon').attr('src','/static/images/edit.svg'))
            .button()
            .addClass('inline-button')
            .attr('data', id)
            .click(editFunction)
            .appendTo($control);

        $('<button>').append(
                $('<img>').addClass('icon').attr('src', '/static/images/delete.svg'))
            .button()
            .addClass('inline-button')
            .attr('data', id)
            .click(deleteFunction)
            .appendTo($control);

        $('<td>').attr('id', 'control-' + forSetting + '-' + id)
            .append($control)
            .appendTo($tr);
    };

    function createSaveCancelControls(originals, saveFunction, cancelFunction) {
        originals.controlSpan.detach();
        $('<button>').append(
                $('<img>').addClass('icon').attr('src', '/static/images/submit-entry.svg'))
            .button()
            .addClass('inline-button')
            .click(saveFunction)
            .appendTo(originals.controlElement);

        $('<button>').append(
                $('<img>').addClass('icon').attr('src', '/static/images/cancel.svg'))
            .button()
            .addClass('inline-button')
            .click(cancelFunction)
            .appendTo(originals.controlElement);
    };

    function inlineEditize($element, id) {
        var value = $element.html();
        $element.empty().append($('<input>').attr('type','text').attr('id',id).addClass('inline-edit').val(value));
    };

})();
