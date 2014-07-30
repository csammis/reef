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
