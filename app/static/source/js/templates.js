angular.module('templates-main', ['main-header.html', 'twist-base.html', 'twist-content.html', 'twist-header.html', 'twist-login.html', 'twist-track-sample.html']);

angular.module("main-header.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("main-header.html",
    "<div>HEADER FILE!</div>");
}]);

angular.module("twist-base.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("twist-base.html",
    "<twist-header></twist-header>\n" +
    "<div ui-view class=\"twst-main-body\"></div>\n" +
    "<div class=\"twst-main-footer\">&copy;{{current_year}} Twist Bioscience</div>");
}]);

angular.module("twist-content.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("twist-content.html",
    "<div class=\"twst-content-main\">CONTENT</div>");
}]);

angular.module("twist-header.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("twist-header.html",
    "<div class=\"twst-header\">\n" +
    "  <div class=\"twst-header-inner\"><img src=\"/static/images/twist.png\" class=\"twst-header-logo-image\">\n" +
    "    <h1 class=\"twst-header-title\">Sample Tracker</h1>\n" +
    "    <div ng-if=\"user.data\" class=\"twst-header-user-info\">\n" +
    "      <p>Logged in as {{user.data.name}}</p><a href=\"/logout\" class=\"twst-logout-button twst-button\">Logout</a>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "</div>");
}]);

angular.module("twist-login.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("twist-login.html",
    "<div ng-if=\"googleLoginUrl\" class=\"twst-login-main\">\n" +
    "  <h3>Please Sign In</h3><a href=\"{{googleLoginUrl}}\" class=\"twst-button\"><img style=\"height:30px; margin-right:8px;\" src=\"/static/images/google-g-logo-2012.png\"><span>Sign In</span></a>\n" +
    "</div>");
}]);

angular.module("twist-track-sample.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("twist-track-sample.html",
    "<div class=\"twst-sample-track-main\"> \n" +
    "  <h1>Record Step</h1>\n" +
    "  <div ng-if=\"!stepTypeOptions\" class=\"twst-spinner\"></div>\n" +
    "  <form ng-show=\"stepTypeOptions\" class=\"twst-sample-track-main-inputs\">\n" +
    "    <div class=\"twst-sample-track-result-message\">\n" +
    "      <twst-message message=\"submissionResultMessage\" visible-and-valid=\"submissionResultVisible\"></twst-message>\n" +
    "    </div>\n" +
    "    <p class=\"twst-input-label-block\">Step Type:</p>\n" +
    "    <div dropdown class=\"btn-group twst-sample-track-step-options-select\">\n" +
    "      <twst-thumb-validation-icon validation=\"selectedStepType\"></twst-thumb-validation-icon>\n" +
    "      <button id=\"single-button\" type=\"button\" dropdown-toggle class=\"btn btn-primary\">{{stepTypeDropdownValue}}&nbsp;<span class=\"caret\"></span></button>\n" +
    "      <ul role=\"menu\" aria-labelledby=\"single-button\" class=\"dropdown-menu\">\n" +
    "        <li role=\"menuitem\" ng-repeat=\"option in stepTypeOptions\"><a ng-click=\"selectStepType(option)\">{{option.text}}</a></li>\n" +
    "      </ul>\n" +
    "    </div>\n" +
    "    <div class=\"twst-sample-track-plate-barcodes\">\n" +
    "      <div class=\"twst-sample-track-plate-barcodes-left\">\n" +
    "        <p class=\"twst-input-label-block\"><span ng-if=\"destinationPlates.length\">Source&nbsp;</span><span>Plate Barcode:</span></p>\n" +
    "        <div ng-repeat=\"plate in sourcePlates\" class=\"twst-input-label-row\">\n" +
    "          <input type=\"text\" ng-model=\"plate.text\" typeahead=\"barcode for barcode in getTypeAheadBarcodes($index)\" typeahead-loading=\"loadingLocations\" typeahead-no-results=\"noResults\" class=\"form-control\">\n" +
    "          <twst-thumb-validation-icon validation=\"plate.text\"></twst-thumb-validation-icon><i ng-show=\"loadingLocations\" class=\"glyphicon glyphicon-refresh\"></i>\n" +
    "          <div ng-show=\"noResults\"><i class=\"glyphicon glyphicon-remove\">No Results Found</i></div>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "      <div class=\"twst-sample-track-plate-barcodes-left\">\n" +
    "        <p ng-class=\"{'twst-invisible': !destinationPlates.length}\" class=\"twst-input-label-block\">Destination Plate Barcode:</p>\n" +
    "        <div ng-repeat=\"plate in destinationPlates\" class=\"twst-input-label-row\">\n" +
    "          <input type=\"text\" ng-model=\"plate.text\" class=\"form-control\">\n" +
    "          <twst-thumb-validation-icon validation=\"plate.text\"></twst-thumb-validation-icon>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "    </div>\n" +
    "    <div class=\"twst-sample-track-main-buttons\">\n" +
    "      <div ng-if=\"submittingStep\" class=\"twst-spinner twst-step-submitting-spinner\"></div>\n" +
    "      <button ng-class=\"{'twst-disabled-button' : !sampleTrackFormReady()}\" ng-click=\"submitStep()\" class=\"twst-button twst-blue-button\">Submit</button><a ng-click=\"clearForm()\" class=\"twst-sample-track-clear-btn\">Clear Form</a>\n" +
    "    </div>\n" +
    "  </form>\n" +
    "</div>");
}]);
