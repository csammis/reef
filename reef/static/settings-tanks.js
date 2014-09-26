(function() {
    function sendConfigRequests() {
        doJqueryAjax('/configs/tanks', 'GET', function(json) {
            var $grid = $('#tanks_grid');
            $grid.children('tr.data').remove();
            for (var i = 0; i < json.tanks.length; i++) {
                $grid.append(buildTank(json.tanks[i]));
            }
        });
    };

    function buildTank(config) {
        var $row = $('<tr>').addClass('data').attr('id', 'tank-id-' + config.id).hoverize();
        $('<td>').attr('id', 'tank-name-' + config.id).html(config.name).appendTo($row);
        createEditDeleteControlsInRow(config.id, 'tank', $row, onEditTank, onDeleteTank);
        return $row;
    }

    function onDeleteTank() {
        var id = $(this).attr('data');
        doJqueryAjax('/configs/tanks/' + id, 'DELETE', function(json) { $('#tank-id-' + id).fadeRemove(); });
    }

    function onEditTank() {
        var id = $(this).attr('data');

        var originals = {
            nameElement: $('#tank-name-' + id),
            controlElement: $('#control-tank-' + id),
            controlSpan: $('#tank-' + id)
        };
        originals['name'] = originals.nameElement.html();

        var finished = function() {
            originals.nameElement.empty().html(originals.name);
            originals.controlElement.empty().append(originals.controlSpan);
        };

        var submitEdit = function() {
            var config = {'name': $('#inline-edit-tank-name-' + id).val()};
            doJqueryAjax('/configs/tanks/' + id, 'PUT', function() {
                originals.name = config.name;
                finished();
            }, config);
        }

        inlineEditize(originals.nameElement, 'inline-edit-tank-name-' + id);
        createSaveCancelControls(originals, submitEdit, finished);
        bindInputsToKeyHandler('#tank-id-' + id, submitEdit, finished);
        $('#inline-edit-tank-name-' + id).focus().select();
    }

    function addNewTank() {
        var config = {'name': $('#new_tank_name').val() };
        doJqueryAjax('/configs/tanks', 'POST', function(json) {
            buildTank(json.tank).hide().appendTo($('#tanks_grid')).fadeIn();
            $('#new_tank_name').val('').focus();
        }, config);
        return false;
    };
    
    $('#submit_new_tank').button().click(addNewTank);
    bindInputsToKeyHandler('.tank_new_entry', addNewTank);
    sendConfigRequests();

})();
