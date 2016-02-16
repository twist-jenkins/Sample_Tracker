angular.module('twist.app').controller('plateDetailsBarcodeEnteredController', ['$scope', '$state', '$stateParams',
    function ($scope, $state, $stateParams) {
        var barcode = decodeURIComponent($stateParams.entered_barcode);
        $scope.getPlateDetails(barcode);
    }]
);
