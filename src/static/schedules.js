(function() {

    function sendDataRequest() {
        $.ajax({ url: '/configs/tanks', type: 'GET', dataType: 'json' })
        .fail(function(data) { alert(data.responseJSON.message); })
        .done(function(json) {
            var tanks = json.tanks;
            var $tabs = $('#tabs');
            var $list = $tabs.find('ul').first();
            for (var i = 0; i < tanks.length; i++) {
                $('<li>').attr('rpi-data', tanks[i].id).append($('<a>').attr('href', tanks[i].name).html(tanks[i].name)).appendTo($list);
            }
            $tabs.tabs();
        });
    };

    window.onload = function() {
        sendDataRequest();
    };
})();
