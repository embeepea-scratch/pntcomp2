var page = require('webpage').create();
page.open("{{htmlfile}}", function () {
    page.render("{{pngfile}}");
    phantom.exit();
});
