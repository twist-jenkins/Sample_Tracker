angular.module('twist.app').controller('plateDetailsBarcodeEnteredController', ['$scope', '$state', '$stateParams',
    function ($scope, $state, $stateParams) {
        var barcode = decodeURIComponent($stateParams.entered_barcode);
        while (barcode != unescape(barcode)) {
            barcode = unescape(barcode);
        }
        $scope.getPlateDetails(barcode);
    }]
);
