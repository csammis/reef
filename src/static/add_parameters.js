(function() {

    function sendConfigRequest() {
        $.ajax({
            url: '/configs/measurements',
            type: 'GET',
            dataType: 'json',
            success: function(json) {
                loadMeasurementSelect(json);
            }
        });
    };

    function sendAddMeasurement(type, time, value) {
        $.ajax({
            url: '/measurements/',
            type: 'POST',
            dataType: 'json',
            data: {
                'type': type,
                'value': value,
                'time': time
            },
            success: function(json) {
                loadAddMeasurementSuccess(json);
            }
        });
    };

    function loadAddMeasurementSuccess(json) {
        alert('yay');
        onActionComplete();
    }

    function loadMeasurementSelect(json) {
        var $select = $('#measurement_type');
        $select.empty()
            .append('<option value="">-- Measurement types --</option>');
        for (conf in json.configs) {
            if (json.configs.hasOwnProperty(conf)) {
                var label = conf;
                if (json.configs[conf].measurement_label) {
                    label = json.configs[conf].measurement_label;
                }
                $select.append('<option value="' + conf + '">' + label + '</option');
            }
        }

        onActionComplete();
    };

    function onActionComplete() {
        $('#busyindicator').hide();
        $('#submitButton').removeAttr('disabled');
    };

    function onActionStart() {
        $('#busyindicator').show();
        $('#submitButton').attr('disabled', 'disabled');
    };

    function doAddMeasurement() {
        var value = $('#measurement_value').val();
        var type = $('#measurement_type').val();
        var time = $('#measurement_time').val();

        if ($('#measurement_value').val() == '') {
            alert('fill in a value');
        }
        else if ($('#measurement_type').val() == '') {
            alert('select a type');
        }
        else {
            onActionStart();
            sendAddMeasurement(type, time, value);
        }
        return false;
    };

    window.onload = function() {
        $('#add_parameter').submit(doAddMeasurement);

        sendConfigRequest();
    };

})();
