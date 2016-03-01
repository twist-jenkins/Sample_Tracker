angular.module('twist.app').controller('plateDetailsController', ['$scope', '$state', 'Api', 'TypeAhead', '$timeout', 
    function ($scope, $state, Api, TypeAhead, $timeout) {
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

            $scope.clearPlateErrorVisible = function () {
                $scope.plateError = null;
            }

            Api.getBasicPlateDetails(barcode).success(function (data) {
                $scope.fetchingDetails = false;
                $scope.plateDetails = data;
                $scope.retrievedPlateBarcode = $scope.plateBarcode + '';
            }).error(function (data) {
                $scope.fetchingDetails = false;
                $scope.plateError = data.message;
                $scope.plateErrorVisible = -1;

            });
        }

        $scope.getExcel = function () {
            if ($scope.plateDetails) {
                document.location.href = '/api/v1/plate-barcodes/' + $scope.plateBarcode + '/csv';
            }
        }
    }]
);
