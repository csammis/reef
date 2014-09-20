(function() {

    function doAddTank() {
        $.ajax({
            url: '/configs/tanks',
            type: 'POST',
            dataType: 'json',
            data: { 'name': $('#setup-tank-name').val() }
        })
        .done(function() { finishSetup(); })
        .fail(function() { alert('oops'); });
    }

    function finishSetup() {
        var $container = $('#main');
        $('<h4>').html('All done!').appendTo($container);
        $('<p>').addClass('description')
            .html('This site is ready to launch! Now you can <a href="/settings/">add additional settings</a> to customize your site.')
            .appendTo($container);
    }

    window.onload = function() {
        $('#submit-tank-name').button().addClass('inline-button').click(function() {
            $(this).hide();
            doAddTank();
        });
    };
})();
