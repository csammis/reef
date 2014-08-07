(function() {
    var WIDTH = 1000;
    var HEIGHT = 400;
    var HORIZONTAL_PADDING = 35;
    var MARGIN = {
            LEFT: 20,
            RIGHT: 0,
            TOP: 0,
            BOTTOM: 20 };
    var VERTICAL_PADDING = 20;

    var COLORS = ['rgb(166,206,227)','rgb(31,120,180)',
                  'rgb(178,223,138)','rgb(51,160,44)',
                  'rgb(251,154,153)','rgb(227,26,28)',
                  'rgb(253,191,111)','rgb(255,127,0)',
                  'rgb(202,178,214)','rgb(106,61,154)',
                  'rgb(255,255,153)','rgb(177,89,40)'];

    function shadeRGBColor(color, percent) {
        var f=color.split(","),t=percent<0?0:255,p=percent<0?percent*-1:percent,R=parseInt(f[0].slice(4)),G=parseInt(f[1]),B=parseInt(f[2]);
        return "rgb("+(Math.round((t-R)*p)+R)+","+(Math.round((t-G)*p)+G)+","+(Math.round((t-B)*p)+B)+")";
    }


    var color_scale = d3.scale.ordinal().range(COLORS);

    var svgs = {};
    var configs = {};
    // configIDs is used to support iterating over the configurations as they're returned from the server as opposed to some arbitrary for (.. in ..) order
    var configIDs = new Array();
    var timeFormat = d3.time.format('%Y-%m-%dT%H:%M:%S');
    var dataSplits = {};

    var datasetForSvg = d3.map();

    function sendConfigRequest() {
        $.ajax({
            url: '/configs/measurements',
            type: 'GET',
            dataType: 'json'})
        .done(function(json) { stashConfigsAndLoadData(json); });
    }

    function stashConfigsAndLoadData(json) {
        for (var i = 0; i < json.configs.length; i++) {
            var config_id = json.configs[i].id;
            configs[config_id] = json.configs[i];
            configIDs.push(config_id);
        }
        color_scale.domain(configIDs);
        configs['length'] = json.configs.length;
        
        $.ajax({
            url: '/measurements/',
            type: 'GET',
            dataType: 'json'})
        .done(function(json) { renderJson(json); });
    }

    function getSvgForParameter(mt) {
        if (!svgs.hasOwnProperty(mt)) {

            ds = dataSplits[mt];

            // Initialize a new SVG with all the graph trimmings
            var label = configs[mt].label;
            var $graphs = $('#graphs');
            $('<h3>').html(label).appendTo($graphs);
            $('<div>').attr('id', 'graph-' + mt)
                .addClass('graphdisplay')
                .appendTo($graphs);

            svgs[mt] = d3.select('#graph-' + mt).append('svg:svg')
                .attr('width', WIDTH + MARGIN.LEFT + MARGIN.RIGHT)
                .attr('height', HEIGHT + MARGIN.TOP + MARGIN.BOTTOM)
                .append('g')
                .attr('transform', 'translate(' + MARGIN.LEFT + ',' + MARGIN.TOP + ')');

            // Axes and labeling
            svgs[mt].append('g')
                .attr('class', 'xAxis')
                .attr('transform', 'translate(0,' + (HEIGHT - VERTICAL_PADDING) + ')');

            svgs[mt].append('g')
                .attr('class', 'yAxis yAxis' + mt)
                .attr('transform', 'translate(' + HORIZONTAL_PADDING + ',0)');

            svgs[mt].append('text')
                .attr('x', (WIDTH + MARGIN.LEFT) / 2)
                .attr('y', HEIGHT + MARGIN.BOTTOM)
                .attr('class', 'axis_label')
                .text('Measurement date');

            if (configs[mt].units) {
                svgs[mt].append('text')
                    .attr('transform', 'rotate(-90)')
                    .attr('y', 0 - MARGIN.LEFT)
                    .attr('x', 0 - (HEIGHT / 2))
                    .attr('dy', '1em')
                    .attr('class', 'axis_label')
                    .text(configs[mt].units);
            }

            // Acceptable range coloring
            if (ds.acceptable_range.get(mt)) {
                var range = ds.acceptable_range.get(mt);
                var yScale = ds.yScale.get(mt);
                var v0 = Math.min(range[0], range[1]);
                var v1 = Math.max(range[0], range[1]);

                svgs[mt].append('rect')
                    .attr('x', HORIZONTAL_PADDING + 5)
                    .attr('y', yScale(v1))
                    .attr('width', WIDTH - (HORIZONTAL_PADDING * 2) - 5)
                    .attr('height', yScale(v0) - yScale(v1))
                    .attr('class', 'acceptable_range');
            }
            
            buildControlsForMeasurementType(mt);
        }

        return svgs[mt];
    }

    function initializeNewDataset(primary_dataset) {
        var dataset = {
            primary_key: primary_dataset,
            data: d3.map(),
            xScale: d3.time.scale().range([HORIZONTAL_PADDING, WIDTH - HORIZONTAL_PADDING]),
            yScale: d3.map(),
            acceptable_range: d3.map(),
            add: function(mt) {
                this.data.set(mt, dataSplits[mt].data.get(mt));
                this.yScale.set(mt, d3.scale.linear().range([HEIGHT - VERTICAL_PADDING, VERTICAL_PADDING]));
                this.acceptable_range.set(mt, configs[mt].acceptable_range);
            },
            remove: function(mt) {
                this.data.remove(mt);
                this.yScale.remove(mt);
                this.acceptable_range.remove(mt);
            }
        };

        dataset.yScale.set(primary_dataset, d3.scale.linear().range([HEIGHT - VERTICAL_PADDING, VERTICAL_PADDING]));
        dataset.acceptable_range.set(primary_dataset, configs[primary_dataset].acceptable_range);

        return dataset;
    };
    
    function renderJson(json) {
        var full_dataset = json.measurements;

        // Split up the full dataset into measurement-specific slices
        for (var i = 0; i < full_dataset.length; i++) {
            var d = full_dataset[i];
            var mt = d.measurement_type_id;
            if (dataSplits[mt] === undefined) {
                dataSplits[mt] = initializeNewDataset(mt);
                dataSplits[mt].data.set(mt, new Array());
            }
            dataSplits[mt].data.get(mt).push(full_dataset[i]);
        }
        
        // Generate a graph and controls for each defined measurement type
        for (var c = 0; c < configIDs.length; c++) {
            var mt = configs[configIDs[c]].id;
            if (dataSplits[mt] === undefined) {
                dataSplits[mt] = initializeNewDataset([mt]);
            }
            renderDatasetForMeasurementTypeOverTime(mt);
        }
    }
    
    function buildControlsForMeasurementType(mt) {
        var $entryContainer = $('<div>').attr('id', 'entry-' + mt)
            .addClass('graphcontrol')
            .appendTo($('#graphs'));

        var entryLabel = configs[mt].units;
        if (entryLabel == '') {
            entryLabel = configs[mt].label;
        }
        $('<h4>').html('New entry').appendTo($entryContainer);
        $('<span>').addClass('entry-units').html(entryLabel + ':&nbsp;').appendTo($entryContainer);
        $('<span>').append(
                $('<input>').attr('type', 'text')
                    .addClass('parameter-entry')
                    .attr('id', 'parameter-entry-' + mt))
            .appendTo($entryContainer);

        function submitEntry() {
            var $input = $('#parameter-entry-' + mt);
            var value = $input.val();
            var post_data = {
                'value': value,
                'measurement_type_id': mt
            };

            var entry_time = $('#entry-time-' + mt).val();
            if (entry_time != undefined) {
                // Since there's no time part and the server's going to convert to UTC,
                // convert to midnight UTC local equivalent so the tz conversion won't jack everything up
                var d = new Date(entry_time);
                d.setMinutes(d.getMinutes() + d.getTimezoneOffset());
                entry_time = d.toString();
                post_data['time'] = entry_time;
            }

            $.ajax({
                url: '/measurements/',
                type: 'POST',
                dataType: 'json',
                data: post_data
            })
            .done(function(json) {
                $input.val('').focus();
                dataSplits[mt].data.push(json.event);
                renderDatasetForMeasurementTypeOverTime(mt);
            })
            .fail(function(data) { alert(data.message); });
        };
        $('<span>').addClass('entry-units').html('<br />Measured:&nbsp;').appendTo($entryContainer);
        $('<input>').addClass('date-entry')
            .attr('type', 'text')
            .attr('id', 'entry-time-' + mt)
            .datepicker({
                showOtherMonths: true,
                selectOtherMonths: true,
                showOn: 'both',
                buttonImage: '/static/images/calendar.svg',
                buttonImageOnly: true})
            .datepicker("setDate", new Date())
            .appendTo($entryContainer);

        $('<button>').html('Save').button().addClass('inline-button').click(function() {
            submitEntry();
            return false;
        }).appendTo($entryContainer);

        $('<h4>').html('Plot against').appendTo($entryContainer);
        var $checkboxContainer = $('<div>').addClass('.checkbox-group').appendTo($entryContainer);
        for (var i = 0; i < configIDs.length; i++) {
            if (configIDs[i] == mt) {
                continue;
            }

            var $span = $('<span>').addClass('plot-against').appendTo($checkboxContainer);
            $('<input>').attr('type', 'checkbox').attr('measurement_type', configIDs[i]).change(function() {
                var svg = getSvgForParameter(mt);
                var existingDataset = datasetForSvg.get(mt);
                var thisMeasurementType = $(this).attr('measurement_type');
                if ($(this).is(':checked') == false) {
                    existingDataset.remove(thisMeasurementType);
                } else {
                    existingDataset.add(thisMeasurementType);
                }
                renderDatasetOverTime(svg, existingDataset);
            }).appendTo($span);
            $('<span>').html('&nbsp;' + configs[configIDs[i]].label).appendTo($span);
            $('<br />').appendTo($checkboxContainer);
        }
        
        $('<div>').css('clear','both').appendTo($('#graphs'));

        bindInputsToKeyHandler('#entry-' + mt, submitEntry);
    }

    function renderDatasetForMeasurementTypeOverTime(mt) {
        renderDatasetOverTime(getSvgForParameter(mt), dataSplits[mt]);
        datasetForSvg.set(mt, dataSplits[mt]);
    }

    function renderDatasetOverTime(svg, dataset) {
        function xPos(d) { return timeFormat.parse(d.measurement_time); };
        function yPos(d) { return d.value; };

        // Remove previously added datapoints except the primary set for this graph
        var current_datasets = svg.attr('current-datasets');
        if (current_datasets) {
            var keys = current_datasets.split(',');
            for (var i = 0; i < keys.length; i++) {
                if (keys[i] != dataset.primary_key) {
                    svg.selectAll('circle.y' + keys[i]).remove();
                    svg.selectAll('path.line.y' + keys[i]).remove();
                }
            }
        }
        // Stash the list of datasets rendered onto this SVG for later cleanup
        svg.attr('current-datasets', dataset.data.keys().join(','));

        // Set time domain across all sets in the dataset
        dataset.xScale.domain(d3.extent(d3.merge(dataset.data.values()), xPos));

        dataset.data.forEach(function(key, value) {

            var yScale = dataset.yScale.get(key);

            yScale.domain(d3.extent(value, yPos)).nice(2);

            // Draw connecting lines between measurements of each type
            var lineFunction = d3.svg.line()
                .x(function(d) { return dataset.xScale(timeFormat.parse(d.measurement_time)); })
                .y(function(d) { return yScale(d.value); })
                .interpolate('monotone');

            var classSelector = 'y' + key;
            
            var points = svg.selectAll('circle.' + classSelector).data(value);
            var line = svg.select('path.line.' + classSelector);
            if (line.empty()) {
                line = svg.append('path')
                        .attr('class', 'line ' + classSelector);
            }
            line.data(value)
                .attr('stroke', function(d) { return color_scale(d.measurement_type_id); });
            
            points.transition()
                .attr('cx', function(d) { return dataset.xScale(xPos(d)); })
                .attr('cy', function(d) { return yScale(yPos(d)); });
            line.transition()
                .attr('d', lineFunction(value));

            if (dataset.acceptable_range.get(key)) {
                var range = dataset.acceptable_range.get(key);
                var v0 = Math.min(range[0], range[1]);
                var v1 = Math.max(range[0], range[1]);
                svg.select('.acceptable_range').transition()
                    .attr('y', yScale(v1))
                    .attr('height', yScale(v0) - yScale(v1));
            }

            points.enter()
               .append('circle')
               .attr('class', classSelector)
               .attr('cx', function(d) { return dataset.xScale(xPos(d)); })
               .attr('cy', function(d) { return yScale(yPos(d)); })
               .attr('fill', function(d) { return shadeRGBColor(color_scale(d.measurement_type_id), -0.2); })
               .attr('r', 4);
        });

        // Draw the axes
        var xAxis = d3.svg.axis().scale(dataset.xScale).orient('bottom');
        svg.selectAll('.xAxis').call(xAxis);
        var yAxisPrimary = d3.svg.axis().scale(dataset.yScale.get(dataset.primary_key)).orient('left');
        svg.selectAll('.yAxis' + dataset.primary_key).call(yAxisPrimary);
    }

    window.onload = sendConfigRequest();
})();
