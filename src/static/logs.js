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
                    createLogEntryElement(logentry, time_display, next_time_display));
        }
    };

    function createLogEntryElement(logentry, time_display, last_time_display) {
        var classForDate = time_display.replace(/\//g, '-');
        var $logentryElement = $('#logentries').find('.' + classForDate);
        if (!$logentryElement.exists()) {
            $logentryElement = $('<article>').addClass('logentry').addClass(classForDate);
        }

        var id = logentry.id;

        // Create a container for the entry and associated controls
        var $entryElement = $('<p>').addClass('logentry-entry').addClass('id-' + id)
            .hover(
                    function() { $('.logentry-control-' + id).show(); },
                    function() { $('.logentry-control-' + id).hide(); }
                  );
        
        var $entrySpan = $('<span>').addClass('entry-group').appendTo($entryElement);

        // Add the entry with associated handlers for edit control
        $('<span>').html(logentry.entry)
            .click(function() {
                var $originalElement = $(this);
                var $stash = $(this).closest('.entry-group');
                var $container = $stash.parent();

                $stash.detach();

                function finished() { $container.empty(); $stash.appendTo($container); }
                
                $('.id-' + id)
                    .append('<input type="text" value="' + $originalElement.html() + '" class="logentry-inline-edit" id="inline-edit-' + id + '" />&nbsp;')
                    .append('<a href="#" id="save-edit-' + id + '">Save</a> <a href="#" id="cancel-edit-' + id + '">Cancel</a>');
                $('#cancel-edit-' + id).click(function() {
                    finished();
                    return false;
                });
                $('#save-edit-' + id).click(function() {
                    var newEntry = $('#inline-edit-' + id).val();
                    $.ajax({
                        url: '/logentries/' + id,
                        type: 'PUT',
                        dataType: 'json',
                        data: {
                            entry: newEntry
                        }})
                    .done(function(json) { $originalElement.html(newEntry); finished(); })
                    .fail(function(json) { alert("Couldn't edit entry"); });
                    return false;
                });
            })
            .hover(
                    function() { $(this).addClass('entry-hover'); },
                    function() { $(this).removeClass('entry-hover'); }
                  )
            .appendTo($entrySpan);

        // Set up the control for deleting an entry
        var $editEntryElement = $('<span>').addClass('logentry-control-' + id).addClass('logentry-control').hide();
        $('<a>').attr('href', '#').html('<img src="/static/images/delete.svg" class="icon" alt="Delete this entry" />').click(function() {
            $.ajax({
                url: '/logentries/' + id,
                type: 'DELETE',
                dataType: 'json'})
            .done(function(json) { removeLogEntry(id); })
            .fail(function(json) { alert("Couldn't delete entry"); });
        }).appendTo($editEntryElement);

        $entrySpan.append($editEntryElement);

        // Append into the article container for the current date
        $logentryElement.append($entryElement);

        // Create a footer
        if (time_display != last_time_display) {
            var $date_div = $('<footer>')
                .addClass('logentry-date')
                .html('<time datetime="' + logentry.entry_time + '">' + time_display + '</time>');
            $logentryElement.append($date_div);
        }

        return $logentryElement;
    };

    function removeLogEntry(id) {
        var $target = $('.id-' + id).first();
        var $parent = $target.parent();
        var $elementToRemove;
        if ($parent.children('p').length == 1) {
            $elementToRemove = $parent;
        } else {
            $elementToRemove = $target;
        }
        $elementToRemove.fadeOut({
            complete: function() { $(this).remove(); }
        });
    }

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

        createLogEntryElement(json.logentry, time_display, last_time_display)
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
