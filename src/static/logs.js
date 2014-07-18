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

        if (json.logentries.length == 0) {
            $('<div>')
                .addClass('logentry-empty')
                .html('No log entries here!')
                .appendTo('#logentries');
            
        }

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
        var classForDate = time_display.replace(/\//g, '-');
        var $logentryElement = $('#logentries').find('.' + classForDate);
        if (!$logentryElement.exists()) {
            $logentryElement = $('<article>').addClass('logentry').addClass(classForDate);
        }

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

    function showDateEntry() {
        $('#datechanger').hide();
        $('#submit-div').prepend(createDateEntrySpan())
    };

    function createDateEntrySpan() {
        var $span = $('<span>').addClass('entry-date').text('Date: ');

        $('<input type="text" id="entry_time">').appendTo($span).datepicker({
            showOtherMonths: true,
            selectOtherMonths: true,
            showOn: 'both',
            buttonImage: '/static/images/calendar.svg',
            buttonImageOnly: true});

        return $span;
    };

    function doAddLogEntry() {
        
        var entry = $('#entry').val();
        var entry_time = $('#entry_time').val();

        if (entry_time != undefined) {
            // Since there's no time part and the server's going to conver to UTC,
            // convert to midnight UTC local equivalent so the tz conversion won't jack everything up
            var d = new Date(entry_time);
            d.setMinutes(d.getMinutes() + d.getTimezoneOffset());
            entry_time = d.toString();
        }

        onAddActionStart();
        $.ajax({
            url: '/logentries/',
            type: 'POST',
            dataType: 'json',
            data: {
                'entry': entry,
                'time': entry_time
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

            $('#entry').val('');
            $('#entry').focus();
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

        $('div[class="logentry-empty"]').remove();

        createLogEntryElement(entry, entry_time, time_display, last_time_display)
            .hide()
            .prependTo('#logentries')
            .fadeIn();

    };

    window.onload = function() {
        $.fn.exists = function() {
            return this.length !== 0;
        }

        $('#add_log_entry').submit(doAddLogEntry);
        $('#submit-link').click(doAddLogEntry);
        $('#changedate').click(showDateEntry);

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
