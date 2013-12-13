(function($,d3) {

  window.contourmap = function(json_contour_file, year, width, height, colors, states_json) {

    $(document).ready(function() {

        $('#yearlabel').text(""+year);

        var svg = d3.select("svg")
                .attr("width", width)
                .attr("height",height);

		//Define map projection
		var projection = d3.geo.albersUsa()
				.translate([width/2, height/2])
				.scale([width]);

		//Define path generator
		var path = d3.geo.path()
				.projection(projection);

        function dolevel(g, json, e) {
            var legenditemrect = undefined;
            if (e) {
                legenditemrect = d3.select('.legenditem.level'+e.level+' rect').attr({
                    'width' : 50,
                    'height' : 20
                });
            }
            var t = g.selectAll("path")
    				 .data(json.features)
    				 .enter()
    				 .append("path")
    				 .attr("d", path)
                     .style({"fill":e.color,"stroke":"black"});
            ;
        }

        d3.json(json_contour_file, function(json) {
            var i,
                level,
                featureCollection;
            for (i=0; i<json.length; ++i) {
                level = json[i].level;
                featureCollection = json[i].featureCollection;
                dolevel(svg.append("g").attr("class", "level"),
                        featureCollection,
                        { "color" : colors[level], "level" : level });
            }

            d3.json(states_json, function(json) {
                svg.append("g")
                    .attr("class", "level")
                    .selectAll("path")
    				.data(json.features)
    				.enter()
    				.append("path")
    				.attr("d", path)
                    .style({"fill":"none","stroke":"black"});
            });

        });



    });

  };

}(jQuery,d3));
