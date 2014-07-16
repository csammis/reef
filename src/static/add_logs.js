(function() {

    function sendAddLogEntry(entry, entry_time) {
        $.ajax({
            url: '/logentries/',
            type: 'POST',
            dataType: 'json',
            data: {
                'entry': entry,
                'entry_time': entry_time
            }})
        .done(function(json) { sendAddLogEntrySuccess(json); });
    }

    function sendAddLogEntrySuccess(json) {
        alert('well done');
        onActionComplete();
    }

    function doAddLogEntry() {
        var entry = $('#entry').val();
        var entry_time = $('#entry_time').val();

        if (entry == '') {
            alert('enter an entry');
        } else {
            onActionStart();
            sendAddLogEntry(entry, entry_time);
        }
        return false;
    }

    window.onload = function() {
        $('#entry_time').datepicker({showOtherMonths: true});
        $('#add_log_entry').submit(doAddLogEntry);        

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
})();
