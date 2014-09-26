// DOM building helper functions

function createEditDeleteControlsInRow(id, forSetting, $tr, editFunction, deleteFunction) {
    var $control = $('<span>').attr('id', forSetting + '-' + id);

    $('<button>').append(
            $('<img>').addClass('icon').attr('src','/static/images/edit.svg'))
        .button()
        .addClass('inline-button')
        .attr('data', id)
        .click(editFunction)
        .appendTo($control);

    $('<button>').append(
            $('<img>').addClass('icon').attr('src', '/static/images/delete.svg'))
        .button()
        .addClass('inline-button')
        .attr('data', id)
        .click(deleteFunction)
        .appendTo($control);

    $('<td>').attr('id', 'control-' + forSetting + '-' + id)
        .append($control)
        .appendTo($tr);
};

function createSaveCancelControls(originals, saveFunction, cancelFunction) {
    originals.controlSpan.detach();
    $('<button>').append(
            $('<img>').addClass('icon').attr('src', '/static/images/submit-entry.svg'))
        .button()
        .addClass('inline-button')
        .click(saveFunction)
        .appendTo(originals.controlElement);

    $('<button>').append(
            $('<img>').addClass('icon').attr('src', '/static/images/cancel.svg'))
        .button()
        .addClass('inline-button')
        .click(cancelFunction)
        .appendTo(originals.controlElement);
};

function inlineEditize($element, id, leaveBlank) {
    var value = $element.html();
    var $input = $('<input>').attr('type','text').attr('id',id).addClass('inline-edit');
    if (leaveBlank === undefined || leaveBlank == false) {
        $input.val(value);
    }
    $element.empty().append($input);
};

(function() {
    window.onload = function() {
        $('#tabs').tabs();
    };
})();
