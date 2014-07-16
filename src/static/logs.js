(function() {

    function sendDataRequest() {
        $.ajax({
            url: '/logentries/',
            type: 'GET',
            dataType: 'json'})
        .done(function(json) { renderLogEntries(json); });
    };

    function renderLogEntries(json) {
        for (entry in json.logentries) {
            if (json.logentries.hasOwnProperty(entry)) {
                var $span = $('<span>');
                $span.append($('<span>').addClass('logentry_date').html(json.logentries[entry].entry_time));
                $span.append($('<span>').addClass('logentry_entry').html(json.logentries[entry].entry));
                var $div = $('<div>').addClass('logentry');
                $div.append($span);

                $("#logentries").append($div);
            }
        }
    };

    window.onload = function() {
        sendDataRequest();
    };
})();
