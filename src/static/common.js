function bindInputsToKeyHandler(selector, enterPressed, escPressed) {
    $(selector).find('input').keydown(function(event) {
        if (event.which == 13 && enterPressed !== undefined) {
            event.preventDefault();
            enterPressed();
        }

        if (event.which == 27 && escPressed !== undefined) {
            event.preventDefault();
            escPressed();
        }
    });
}

function fetchAndBuildTankTabs(tabChangedFunction) {
    $.ajax({ url: '/configs/tanks', type: 'GET', dataType: 'json' })
        .fail(function(data) { alert(data.responseJSON.message); })
        .done(function(json) {
            var tanks = json.tanks;
            var $tabs = $('#tabs');
            var $list = $tabs.find('ul').first();
            for (var i = 0; i < tanks.length; i++) {
                $('<li>').attr('rpi-data', tanks[i].id).append($('<a>').attr('href', 'tank-tab-' + tanks[i].id).html(tanks[i].name)).appendTo($list);
            }

            $tabs.tabs({ beforeLoad: function(event, ui) {
                event.preventDefault();

                var tank_id = ui.tab.attr('rpi-data');
                tabChangedFunction(tank_id);
            }});
        });
}

