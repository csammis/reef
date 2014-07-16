(function() {

    function sendConfigRequest() {
        $.ajax({
            url: '/configs/measurements',
            type: 'GET',
            dataType: 'json'})
        .done(function(json) { loadMeasurementSelect(json); });
    };

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

    function doAddMeasurement() {
        var value = $('#measurement_value').val();
        var type = $('#measurement_type').val();
        var time = $('#measurement_time').val();

        if (value == '') {
            alert('fill in a value');
        }
        else if (type == '') {
            alert('select a type');
        }
        else {
            onActionStart();
            sendAddMeasurement(type, time, value);
        }
        return false;
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
                }
            })
        .done(function(json) {loadAddMeasurementSuccess(json); });
    };

    function loadAddMeasurementSuccess(json) {
        alert('yay');
        onActionComplete();
    }

    window.onload = function() {
        $('#measurement_time').datepicker({showOtherMonths: true});
        $('#add_parameter').submit(doAddMeasurement);

        sendConfigRequest();
    };

    function onActionComplete() {
        $('#busyindicator').hide();
        $('#submitButton').removeAttr('disabled');
    };

    function onActionStart() {
        $('#busyindicator').show();
        $('#submitButton').attr('disabled', 'disabled');
    };

})();
