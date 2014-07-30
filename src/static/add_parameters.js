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

        for(var i = 0; i < json.configs.length; i++) {
            var config = json.configs[i];
            $select.append('<option value="' + config.id + '">' + config.label + '</option');
        }

        onActionComplete();
    };

    function doAddMeasurement() {
        var value = $('#measurement_value').val();
        var type_id = $('#measurement_type').val();
        var time = $('#measurement_time').val();

        if (value == '') {
            alert('fill in a value');
        }
        else if (type_id == '') {
            alert('select a type');
        }
        else {
            onActionStart();
            sendAddMeasurement(type_id, time, value);
        }
        return false;
    };

    function sendAddMeasurement(type_id, time, value) {
        $.ajax({
            url: '/measurements/',
            type: 'POST',
            dataType: 'json',
            data: {
                'measurement_type_id': type_id,
                'value': value,
                'time': time
                }
            })
        .done(function(json) {loadAddMeasurementSuccess(json); })
        .fail(function(data) { alert(data.message); })
        .always(function() { onActionComplete(); });
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
