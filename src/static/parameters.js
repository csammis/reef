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
    var timeFormat = d3.time.format('%Y-%m-%dT%H:%M:%S');

    function sendConfigRequest() {
        $.ajax({
            url: '/configs/measurements',
            type: 'GET',
            dataType: 'json',
            success: function(json) {
                stashConfigs(json);
            }
        });
    };

    function stashConfigs(json) {
        configs = json.configs;
        sendDataRequest();
    };

    function sendDataRequest() {
        $.ajax({
            url: '/measurements/',
            type: 'GET',
            dataType: 'json',
            success: function(json) {
                renderJson(json);
            }
        });
    };

    function getSvgForParameter(parameter) {
        if (!svgs.hasOwnProperty(parameter)) {
            var label = parameter;
            if (configs.hasOwnProperty(parameter)) {
                label = configs[parameter].measurement_label;
            }

            $('#graphs').append('<h3>' + label + '</h3>').append('<div id="graph' + parameter + '"></div>').addClass('graphdiv');
            svgs[parameter] = d3.select('#graph' + parameter).append('svg:svg')
                .attr('width', WIDTH + MARGIN.LEFT + MARGIN.RIGHT)
                .attr('height', HEIGHT + MARGIN.TOP + MARGIN.BOTTOM)
                .append('g')
                .attr('transform', 'translate(' + MARGIN.LEFT + ',' + MARGIN.TOP + ')');
        }

        return svgs[parameter];
    }
    
    function renderJson(json) {

        // Slice up the event data into measurement types
        var full_dataset = json.events;
        var dataSplits = {};
        var measurementTypes = new Array();
        for (var i = 0; i < full_dataset.length; i++) {
            d = full_dataset[i];
            if (dataSplits[d.measurement_type] === undefined) {
                dataSplits[d.measurement_type] = new Array();
                measurementTypes.push(d.measurement_type);
            }
            dataSplits[d.measurement_type].push(full_dataset[i]);
        }

        // Create a common X axis for all measurements
        var xScale = d3.time.scale()
            .range([HORIZONTAL_PADDING, WIDTH - HORIZONTAL_PADDING])
            .domain(d3.extent(full_dataset, function(d) { return timeFormat.parse(d.measurement_time); }));

        // Generate a graph for each measurement type
        for (var i = 0; i < measurementTypes.length; i++) {
            var mt = measurementTypes[i];
            var ds = dataSplits[mt];
            
            var yScale = d3.scale.linear()
                .range([HEIGHT - VERTICAL_PADDING, VERTICAL_PADDING])
                .domain(d3.extent(ds, function(d) { return d.value; })).nice(2);

            var xAxis = d3.svg.axis().scale(xScale).orient('bottom');
            var yAxis = d3.svg.axis().scale(yScale).orient('left');

            var s = getSvgForParameter(mt);

            // Axes and common labeling
            s.append('g')
                .attr('class', 'xAxis')
                .attr('transform', 'translate(0,' + (HEIGHT - VERTICAL_PADDING) + ')')
                .call(xAxis);

            s.append('g')
                .attr('class', 'yAxis')
                .attr('transform', 'translate(' + HORIZONTAL_PADDING + ',0)')
                .call(yAxis);

            s.append('text')
                .attr('x', (WIDTH + MARGIN.LEFT) / 2)
                .attr('y', HEIGHT + MARGIN.BOTTOM)
                .style('text-anchor', 'middle')
                .style('font-family', 'sans-serif')
                .text('Measurement date');

            // Draw any customizations that are configured for this measurement
            if (configs.hasOwnProperty(mt)) {
                var v0 = Math.min(configs[mt].range[0], configs[mt].range[1]);
                var v1 = Math.max(configs[mt].range[0], configs[mt].range[1]);

                s.append('rect')
                    .attr('x', HORIZONTAL_PADDING)
                    .attr('y', yScale(v1))
                    .attr('width', WIDTH - (HORIZONTAL_PADDING * 2))
                    .attr('height', yScale(v0) - yScale(v1))
                    .attr('fill', 'lightgreen')
                    .attr('stroke', 'darkgreen');

                s.append('text')
                    .attr('transform', 'rotate(-90)')
                    .attr('y', 0 - MARGIN.LEFT)
                    .attr('x', 0 - (HEIGHT / 2))
                    .attr('dy', '1em')
                    .style('text-anchor', 'middle')
                    .style('font-family', 'sans-serif')
                    .text(configs[mt].value_label);
            }

            // Draw connecting lines between measurements of each type
            var lineFunction = d3.svg.line()
                .x(function(d) { return xScale(timeFormat.parse(d.measurement_time)); })
                .y(function(d) { return yScale(d.value); })
                .interpolate('linear');
                
            s.append('path')
                .attr('d', lineFunction(ds))
                .attr('class', 'measurement_' + mt + ' line');

            s.selectAll('circle')
               .data(ds)
               .enter()
               .append('circle')
               .attr('class', function(d) { return 'measurement_' + d.measurement_type; })
               .attr('cx', function(d) { return xScale(timeFormat.parse(d.measurement_time)); })
               .attr('cy', function(d) { return yScale(d.value); })
               .attr('r', 4);
        }
    };

    $(function() {
        // Bind up html controls
    });

    window.onload = sendConfigRequest();
})();
