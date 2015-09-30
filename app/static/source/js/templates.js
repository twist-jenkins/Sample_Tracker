angular.module('templates-main', ['main-header.html', 'twist-base.html', 'twist-header.html']);

angular.module("main-header.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("main-header.html",
    "<div>HEADER FILE!</div>");
}]);

angular.module("twist-base.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("twist-base.html",
    "<twist-header></twist-header>\n" +
    "<div class=\"twst-main-body\">BODY</div>\n" +
    "<div class=\"twst-main-footer\">&copy;{{current_year}} Twist Bioscience</div>");
}]);

angular.module("twist-header.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("twist-header.html",
    "<div class=\"twst-header\"><img src=\"/static/images/twist.png\" class=\"twst-header-logo-image\"/>\n" +
    "  <h1 class=\"twst-header-title\">Sample Tracker</h1>\n" +
    "  <div class=\"twst-header-user-info\">\n" +
    "    <p>Logged in as {{user}}<a href=\"/logout\" class=\"twst-button\">Logout</a></p>\n" +
    "  </div>\n" +
    "</div>");
}]);
