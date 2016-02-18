angular.module('twist.app').controller('plateDetailsController', ['$scope', '$state', 'Api', 'TypeAhead',
    function ($scope, $state, Api, TypeAhead) {
        $scope.getTypeAheadBarcodes = TypeAhead.getTypeAheadBarcodes;
        $scope.plateBarcode = '';
        $scope.lastUsedBarcode = null;

        $scope.getDetailsClicked = function () {
            if ($scope.plateBarcode.length > 5) {
                if ($scope.plateBarcode === $scope.lastUsedBarcode) {
                    $scope.getPlateDetails($scope.plateBarcode);
                } else {
                    $state.go('root.plate_details.barcode_entered', {
                        entered_barcode: $scope.plateBarcode
                    });
                }
            }
        };

        $scope.getPlateDetails = function (barcode) {
            $scope.plateDetails = null;
            $scope.plateBarcode = barcode;
            $scope.lastUsedBarcode = barcode;

            $scope.fetchingDetails = true;

            $scope.retrievedPlateBarcode = '';

            Api.getBasicPlateDetails(barcode).success(function (data) {
                $scope.fetchingDetails = false;
                $scope.plateDetails = data;
                $scope.retrievedPlateBarcode = $scope.plateBarcode + '';
            });
        }

        $scope.getExcelHref = function () {
            return $scope.plateBarcode.length < 6 ? null : '/api/v1/plate-barcodes/' + $scope.plateBarcode + '/csv';
        }
    }]
);
