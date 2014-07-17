(function() {

    function sendDataRequest() {
        $.ajax({
            url: '/logentries/',
            type: 'GET',
            dataType: 'json'})
        .done(function(json) { renderLogEntries(json); })
        .fail(function(resp) { showDataRequestFailure(); });
    };

    function showDataRequestFailure() {
        alert("whoops");
    }

    function renderLogEntries(json) {
        $('#logentries').empty();

        for (var i = json.logentries.length - 1; i >= 0; i--) {
            var logentry = json.logentries[i];

            var entry_time = new Date(logentry.entry_time);
            var time_display = entry_time.toLocaleDateString();
            var next_time_display = '';
            if (i - 1 >= 0) {
                next_time_display = new Date(json.logentries[i - 1].entry_time).toLocaleDateString();
            }

            $('#logentries').append(
                    createLogEntryElement(logentry.entry, logentry.entry_time, time_display, next_time_display));
        }
    };

    function createLogEntryElement(content, fulltime, time_display, last_time_display) {
        var $logentryElement = $('<article>').addClass('logentry');

        var $entryElement = $('<p>').addClass('logentry-entry').html(content);
        $logentryElement.append($entryElement);

        if (time_display != last_time_display) {
            var $date_div = $('<footer>')
                .addClass('logentry-date')
                .html('<time datetime="' + fulltime + '">' + time_display + '</time>');
            $logentryElement.append($date_div);
        }

        return $logentryElement;
    };

    function doAddLogEntry() {

        
        var entry = $('#entry').val();
        var entry_time = $('#entry_time').val();

        onAddActionStart();
        $.ajax({
            url: '/logentries/',
            type: 'POST',
            dataType: 'json',
            data: {
                'entry': entry,
                'entry_time': entry_time
            }})
        .done(function(json) { handlePostLogEntryResponse(json, true); })
        .fail(function(resp) { handlePostLogEntryResponse(resp, false); });

        return false;
    };

    function handlePostLogEntryResponse(json, success) {
        if (success) {
            $.ajax({
                url: '/logentries/' + json.log_id,
                type: 'GET',
                dataType: 'json'})
            .done(function(json) { handleGetSingleEntryResponse(json); })
            .fail(function(resp) { showDataRequestFailure(); });
        } else {
            alert(json.responseJSON.message);
        }
        onAddActionComplete();
    };

    function handleGetSingleEntryResponse(json) {
        var entry = json.logentry.entry;
        var entry_time = json.logentry.entry_time;
        var time_display = new Date(entry_time).toLocaleDateString();

        var last_time_display = $('#logentries').find('time:first').text();
        console.log(last_time_display);

        createLogEntryElement(entry, entry_time, time_display, last_time_display)
            .hide()
            .prependTo('#logentries')
            .fadeIn();

    };

    window.onload = function() {
        $('#entry_time').datepicker({showOtherMonths: true});
        $('#add_log_entry').submit(doAddLogEntry);        

        sendDataRequest();
    };

    /*
     * UI updaters for beginning and ending a log entry addition
     */
    function onAddActionComplete() {
        $('#busyindicator').hide();
        $('#submitButton').removeAttr('disabled');
    };

    function onAddActionStart() {
        $('#busyindicator').show();
        $('#submitButton').attr('disabled', 'disabled');
    };
})();
