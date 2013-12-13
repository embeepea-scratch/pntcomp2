(function() {
    var colors = {
        "00" : "#2066ab",
        "01" : "#3c93c4",
        "02" : "#91c4e1",
        "03" : "#d3e5f3",
        "04" : "#fbdbc6",
        "05" : "#f4a580",
        "06" : "#da6048",
        "07" : "#b11e2a"
    };
    contourmap("{{contour-json}}", "{{caption}}",
               {{width}}, {{height}}, colors, "lib/lower48-states.json");
/*
    contourmap("../data/22year-anomaly-contours/2012.json",
               "2012", 700, 325, colors, "lib/lower48-states.json");
*/
}());
