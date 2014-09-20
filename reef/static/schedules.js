(function() {

    function sendDataRequest() {
        $.ajax({ url: '/configs/tanks', type: 'GET', dataType: 'json' })
        .fail(function(data) { alert(data.responseJSON.message); })
        .done(function(json) {
            var tanks = json.tanks;
            var $tabs = $('#tabs');
            var $list = $tabs.find('ul').first();
            var tabOptions = { };
            for (var i = 0; i < tanks.length; i++) {
                $('<li>').attr('rpi-data', tanks[i].id).append($('<a>').attr('href', tanks[i].name).html(tanks[i].name)).appendTo($list);
                if (window.location.hash == '#' + tanks[i].name) {
                    tabOptions['active'] = i;
                }
            }

            $tabs.tabs(tabOptions);
        });
    };

    window.onload = function() {
        sendDataRequest();
    };
})();
