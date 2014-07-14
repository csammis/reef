(function() {
    var WIDTH = 600;
    var HEIGHT = 400;
    var PADDING = 25;

    var svg = d3.select('#graph')
                .append('svg:svg')
                .attr('width', WIDTH)
                .attr('height', HEIGHT)
                .text('All Parameters');

    var timeFormat = d3.time.format('%Y-%m-%dT%H:%M:%S');


    // Doing this quick + dirty because I don't want to drag in jquery right this second
    var req = new XMLHttpRequest;
    req.overrideMimeType('application/json');
    req.open('GET', '/measurements/');
    req.onload = function() {
        if (req.status == 200) {
            renderJson(JSON.parse(req.responseText));
        }
    };
    req.send(null);

    var renderJson = function(json) {

        var dataset = json.events;

        var xScale = d3.time.scale()
                        .range([PADDING, WIDTH - PADDING])
                        .domain(d3.extent(dataset, function(d) { return timeFormat.parse(d.measurement_time); }));
        var yScale = d3.scale.linear()
                        .range([HEIGHT - PADDING, PADDING])
                        .domain(d3.extent(dataset, function(d) { return d.value; }));

        var xAxis = d3.svg.axis().scale(xScale).orient('bottom');
        var yAxis = d3.svg.axis().scale(yScale).orient('left');

        svg.append('g')
            .attr('class', 'xAxis')
            .attr('transform', 'translate(0,' + (HEIGHT - PADDING) + ')')
            .call(xAxis);

        svg.append('g')
            .attr('class', 'yAxis')
            .attr('transform', 'translate(' + PADDING + ',0)')
            .call(yAxis);
        
                
        svg.selectAll('circle')
           .data(dataset)
           .enter()
           .append('circle')
           .attr('cx', function(d) { return xScale(timeFormat.parse(d.measurement_time)); })
           .attr('cy', function(d) { return yScale(d.value); })
           .attr('r', 4);
    };

})();
