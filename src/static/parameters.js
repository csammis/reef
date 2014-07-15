(function() {
    var WIDTH = 1000;
    var HEIGHT = 400;
    var HORIZONTAL_PADDING = 35;
    var VERTICAL_PADDING = 20;

    var svg = d3.select('#graph')
                .append('svg:svg')
                .attr('width', WIDTH)
                .attr('height', HEIGHT)
                .text('All Parameters');

    var timeFormat = d3.time.format('%Y-%m-%dT%H:%M:%S');

    function sendRequest() {
        $.ajax({
            url: '/measurements/',
            type: 'GET',
            dataType: 'json',
            success: function(json) {
                renderJson(json);
            }
        });
    };
    
    function renderJson(json) {

        // Slice up the event data into measurement types
        var dataset = json.events;
        var dataSplits = Object;
        var measurementTypes = new Array();
        for (var i = 0; i < dataset.length; i++) {
            d = dataset[i];
            if (dataSplits[d.measurement_type] === undefined) {
                dataSplits[d.measurement_type] = new Array();
                measurementTypes.push(d.measurement_type);
            }
            dataSplits[d.measurement_type].push(dataset[i]);
        }

        var xScale = d3.time.scale()
            .range([HORIZONTAL_PADDING, WIDTH - HORIZONTAL_PADDING])
            .domain(d3.extent(dataset, function(d) { return timeFormat.parse(d.measurement_time); }));
        var yScale = d3.scale.linear()
            .range([HEIGHT - VERTICAL_PADDING, VERTICAL_PADDING])
            .domain(d3.extent(dataset, function(d) { return d.value; }));

        var xAxis = d3.svg.axis().scale(xScale).orient('bottom');
        var yAxis = d3.svg.axis().scale(yScale).orient('left');

        svg.append('g')
            .attr('class', 'xAxis')
            .attr('transform', 'translate(0,' + (HEIGHT - VERTICAL_PADDING) + ')')
            .call(xAxis);

        svg.append('g')
            .attr('class', 'yAxis')
            .attr('transform', 'translate(' + HORIZONTAL_PADDING + ',0)')
            .call(yAxis);
       
        svg.selectAll('circle')
           .data(dataset)
           .enter()
           .append('circle')
           .attr('class', function(d) { return 'measurement_' + d.measurement_type; })
           .attr('cx', function(d) { return xScale(timeFormat.parse(d.measurement_time)); })
           .attr('cy', function(d) { return yScale(d.value); })
           .attr('r', 4);

        // Draw connecting lines between measurements of each type
        var lineFunction = d3.svg.line()
            .x(function(d) { return xScale(timeFormat.parse(d.measurement_time)); })
            .y(function(d) { return yScale(d.value); })
            .interpolate('linear');
            
        for (var i = 0; i < measurementTypes.length; i++) {
            svg.append('path')
                .attr('d', lineFunction(dataSplits[measurementTypes[i]]))
                .attr('class', 'measurement_' + measurementTypes[i] + ' line');
        }
    };

    $(function() {
        // Bind up html controls
    });

    window.onload = sendRequest();
})();
