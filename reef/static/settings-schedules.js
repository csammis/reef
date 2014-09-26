(function() {

    function valForDayOfWeek(days, i) {
        switch (i) {
            case 0: return days.sunday;
            case 1: return days.monday;
            case 2: return days.tuesday;
            case 3: return days.wednesday;
            case 4: return days.thursday;
            case 5: return days.friday;
            case 6: return days.saturday;
        }
        return undefined;
    }

    function sendConfigRequests() {
        doJqueryAjax('/schedule/', 'GET', function(json) {
            var $div = $('#schedule-entry');
            $div.children().remove();
            for (var i = 0; i < json.all.length; i++) {
                $div.append(buildScheduleForTank(json.all[i]));
            }
        });
    };

    function getPrettyStringForDays(days) {
        var retval = new Array();
        if (days.sunday) retval.push('Sunday');
        if (days.monday) retval.push('Monday');
        if (days.tuesday) retval.push('Tuesday');
        if (days.wednesday) retval.push('Wednesday');
        if (days.thursday) retval.push('Thursday');
        if (days.friday) retval.push('Friday');
        if (days.saturday) retval.push('Saturday');
        
        if (retval.length > 0) {
            return 'every ' + retval.join(', ');
        } else {
            return 'never';
        }
    }

    function buildScheduleForTank(config) {
        var $section = $('<div>').addClass('schedule-for').html('Schedule for tank ' + config.name + ':');
        var $list = $('<ul>').addClass('schedule-list').appendTo($section);
        for (var i = 0; i < config.schedule.length; i++) {
            $list.append(createScheduledEventListItem(config.schedule[i]));
        }
        $addNewElement = $('<li>').attr('id', 'new-entry-' + config.name);
        $('<a>').attr('href', '#').attr('data-name', config.name).attr('data-id', config.id).html('Add new scheduled task').click(onClickAddNewTask).appendTo($addNewElement);
        $addNewElement.appendTo($list);
        return $section;
    }

    function createScheduledEventListItem(se) {
        var $li = $('<li>').attr('id', 'schedule-event-' + se.id);
        var $contents = $('<span>');
        $('<span>').attr('data-name', se.event_name).html(getPrettyStringForScheduledTask(se)).click(function() {
            var originals = {
                spanElement: $(this)
            };

            var finished = function() {
                $li.empty().append($contents);
            };

            var $editTask = $('<span>');
            var $editInput = $('<input>').attr('id', 'inline-edit-task-' + se.id).val($(this).attr('data-name')).appendTo($editTask);
            $editTask.append(' every ').show();
            appendDayCheckboxesToSpan($editTask, se.id, se.on_days);
            $('<button>').html('Save').button().addClass('inline-button').click(function() {
                var postdata = {
                    event_name: $editInput.val(),
                    on_days: getSelectedDaysForName(se.id)
                };

                doJqueryAjax('/schedule/' + se.id, 'PUT', function (json) {
                    originals.spanElement.html(getPrettyStringForScheduledTask(json.schedule));
                    finished();
                }, postdata);
            }).appendTo($editTask);
            $('<button>').html('Cancel').button().addClass('inline-button').click(finished).appendTo($editTask);

            $contents.detach();
            $li.append($editTask);
            $('#inline-edit-task-' + se.id).focus().select();

        }).hoverize().appendTo($contents);
        $('<a>').attr('href', '#').html('Delete').addClass('delete-link').click(function () {
            doJqueryAjax('/schedule/' + se.id, 'DELETE', function(json) {
                $('#schedule-event-' + se.id).fadeRemove();
            });
        }).appendTo($contents);
        $contents.appendTo($li);
        return $li;
    }

    function getPrettyStringForScheduledTask(se) {
        return se.event_name + ' ' + getPrettyStringForDays(se.on_days);
    }

    function onClickAddNewTask() {
        var name = $(this).attr('data-name');
        var id = $(this).attr('data-id');
        var originals = {
            linkElement: $(this),
            lastLiElement: $(this).parent()
        };

        var finished = function() {
            originals.lastLiElement.empty().append(originals.linkElement);
        };

        var $addTask = $('<span>');
        $('<input>').attr('id', 'inline-add-task-' + id).appendTo($addTask);
        $addTask.append(' every ').show();
        appendDayCheckboxesToSpan($addTask, 'tid-' + id);
        $('<button>').html('Add').button().addClass('inline-button').click(function() {
            var postdata = {
                event_name: $('#inline-add-task-' + id).val(),
                on_days: getSelectedDaysForName('tid-' + id)
            };
            
            doJqueryAjax('/schedule/' + name, 'POST', function (json) {
                originals.lastLiElement.before(createScheduledEventListItem(json.schedule));
                finished();
            }, postdata);
        }).appendTo($addTask);
        $('<button>').html('Cancel').button().addClass('inline-button').click(finished).appendTo($addTask);
        
        originals.linkElement.detach();
        originals.lastLiElement.empty().append($addTask);
        $('#inline-add-task-' + name).focus().select();
    }

    function getSelectedDaysForName(name) {
        var days = new Array();
        for (var i = 0; i < 7; i++) {
            if ($('#new-' + i + name).is(':checked')) { days.push(i); }
        }
        return days;
    }

    function appendDayCheckboxesToSpan($span, name, existingValues) {
        for (var i = 0; i < 7; i++) {
            var $input = $('<input>').attr('type', 'checkbox').attr('id', 'new-' + i + name);
            if (existingValues !== undefined) {
                $input.prop('checked', valForDayOfWeek(existingValues, i));
            }
            $span.append($input).append(' ' + DAYS_OF_WEEK[i] + ' ');
        }
    }
    
    sendConfigRequests();

})();
