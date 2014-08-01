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

    var svgs = {};
    var configs = {};
    // configIDs is used to support iterating over the configurations as they're returned from the server as opposed to some arbitrary for (.. in ..) order
    var configIDs = new Array();
    var timeFormat = d3.time.format('%Y-%m-%dT%H:%M:%S');
    var dataSplits = {};


    function sendConfigRequest() {
        $.ajax({
            url: '/configs/measurements',
            type: 'GET',
            dataType: 'json'})
        .done(function(json) { stashConfigs(json); });
    };

    function stashConfigs(json) {
        for (var i = 0; i < json.configs.length; i++) {
            var config_id = json.configs[i].id;
            configs[config_id] = json.configs[i];
            configIDs.push(config_id);
        }
        configs['length'] = json.configs.length;
        sendDataRequest();
    };

    function sendDataRequest() {
        $.ajax({
            url: '/measurements/',
            type: 'GET',
            dataType: 'json'})
        .done(function(json) { renderJson(json); });
    };

    function getSvgForParameter(mt) {
        if (!svgs.hasOwnProperty(mt)) {

            ds = dataSplits[mt];

            // Initialize a new SVG with all the graph trimmings
            var label = configs[mt].label;
            $('#graphs').append('<h3>' + label + '</h3>').append('<div id="graph' + mt + '"></div>').addClass('graphdiv');

            svgs[mt] = d3.select('#graph' + mt).append('svg:svg')
                .attr('width', WIDTH + MARGIN.LEFT + MARGIN.RIGHT)
                .attr('height', HEIGHT + MARGIN.TOP + MARGIN.BOTTOM)
                .append('g')
                .attr('transform', 'translate(' + MARGIN.LEFT + ',' + MARGIN.TOP + ')');

            // Axes and labeling
            svgs[mt].append('g')
                .attr('class', 'xAxis')
                .attr('transform', 'translate(0,' + (HEIGHT - VERTICAL_PADDING) + ')');
            svgs[mt].append('g')
                .attr('class', 'yAxis')
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
            if (configs[mt].acceptable_range) {
                var v0 = Math.min(configs[mt].acceptable_range[0], configs[mt].acceptable_range[1]);
                var v1 = Math.max(configs[mt].acceptable_range[0], configs[mt].acceptable_range[1]);

                svgs[mt].append('rect')
                    .attr('x', HORIZONTAL_PADDING)
                    .attr('y', ds.yScale(v1))
                    .attr('width', WIDTH - (HORIZONTAL_PADDING * 2))
                    .attr('height', ds.yScale(v0) - ds.yScale(v1))
                    .attr('class', 'acceptable_range');
            }

            // Point connecting path element
            svgs[mt].append('path')
                .attr('stroke', 'black')
                .attr('class', 'line');
        }

        return svgs[mt];
    }
    
    function renderJson(json) {

        var full_dataset = json.measurements;

        // Split up the full dataset into measurement-specific slices
        for (var i = 0; i < full_dataset.length; i++) {
            d = full_dataset[i];
            if (dataSplits[d.measurement_type_id] === undefined) {
                dataSplits[d.measurement_type_id] = initializeNewDataset();
            }
            dataSplits[d.measurement_type_id].data.push(full_dataset[i]);
        }
        
        // Generate a graph and controls for each measurement type
        for (var c = 0; c < configIDs.length; c++) {
            var mt = configs[configIDs[c]].id;
            if (dataSplits[mt] === undefined) {
                dataSplits[mt] = initializeNewDataset();
            }
            renderDatasetForMeasurementTypeOverTime(mt);
            buildParameterEntryForMeasurementType(mt);
        }
    };

    function initializeNewDataset() {
        return {
            data: new Array(),
            xScale: d3.time.scale().range([HORIZONTAL_PADDING, WIDTH - HORIZONTAL_PADDING]),
            yScale: d3.scale.linear().range([HEIGHT - VERTICAL_PADDING, VERTICAL_PADDING])
        };
    }

    function buildParameterEntryForMeasurementType(mt) {
        var $entryContainer = $('<div>').addClass('entry-' + mt).appendTo($('#graphs'));

        $('<span>').html('New entry: ').appendTo($entryContainer);
        $('<span>').html('<input type="text" class="parameter-entry" id="parameter-entry-' + mt + '" /> ').appendTo($entryContainer);
        $('<span>').addClass('entry-units').html(configs[mt].units).appendTo($entryContainer);
        
        function submitEntry() {
            var $input = $('#parameter-entry-' + mt);
            var value = $input.val();
            $.ajax({
                url: '/measurements/',
                type: 'POST',
                dataType: 'json',
                data: {
                    'value': value,
                    'measurement_type_id': mt }
            })
            .done(function(json) {
                $input.val('').focus();
                dataSplits[mt].data.push(json.event);
                renderDatasetForMeasurementTypeOverTime(mt);
            })
            .fail(function(data) { alert(data.message); });
        };

        $('<a>').attr('href', '#').css('margin-left','0.5em').html('save').click(function() {
            submitEntry();
            return false;
        }).appendTo($entryContainer);

        bindInputsToKeyHandler('.entry-' + mt, submitEntry);
    };

    function renderDatasetForMeasurementTypeOverTime(mt) {

        function xPos(d) { return timeFormat.parse(d.measurement_time); };
        function yPos(d) { return d.value; };

        var ds = dataSplits[mt];
        ds.xScale.domain(d3.extent(ds.data, xPos));
        ds.yScale.domain(d3.extent(ds.data, yPos)).nice(2);

        var s = getSvgForParameter(mt);

        // Draw connecting lines between measurements of each type
        var lineFunction = d3.svg.line()
            .x(function(d) { return ds.xScale(timeFormat.parse(d.measurement_time)); })
            .y(function(d) { return ds.yScale(d.value); })
            .interpolate('linear');
        
        var points = s.selectAll('circle').data(ds.data);
        var line = s.select('path.line').data(ds.data);
        
        points.transition()
            .attr('cx', function(d) { return ds.xScale(xPos(d)); })
            .attr('cy', function(d) { return ds.yScale(yPos(d)); });
        line.transition()
            .attr('d', lineFunction(ds.data));

        if (configs[mt].acceptable_range) {
            var v0 = Math.min(configs[mt].acceptable_range[0], configs[mt].acceptable_range[1]);
            var v1 = Math.max(configs[mt].acceptable_range[0], configs[mt].acceptable_range[1]);
            s.select('.acceptable_range').transition()
                .attr('y', ds.yScale(v1))
                .attr('height', ds.yScale(v0) - ds.yScale(v1));
        }

        points.enter()
           .append('circle')
           .attr('class', function(d) { return 'measurement_' + d.measurement_type; })
           .attr('cx', function(d) { return ds.xScale(xPos(d)); })
           .attr('cy', function(d) { return ds.yScale(yPos(d)); })
           .attr('r', 4);

        // Draw the axes
        var xAxis = d3.svg.axis().scale(ds.xScale).orient('bottom');
        s.selectAll('.xAxis').call(xAxis);
        var yAxis = d3.svg.axis().scale(ds.yScale).orient('left');
        s.selectAll('.yAxis').call(yAxis);
    }

    $(function() {
        // Bind up html controls
    });

    window.onload = sendConfigRequest();
})();
