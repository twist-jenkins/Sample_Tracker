angular.module('twist.app').controller('hamiltonSelectController', ['$scope', '$state', '$stateParams', 'Constants', 'Maps', 'Formatter', '$timeout', 'Api',
    function ($scope, $state, $stateParams, Constants, Maps, Formatter, $timeout, Api) {
        $scope.hamiltonBarcodeChange = function () {
            $timeout.cancel($scope.hamiltonBarcodeChangeTimeout);
            var barcode = $scope.hamiltonBarcode.trim();
            if (barcode != '' && barcode.length > 4) {
                $scope.hamiltonBarcodeChangeTimeout = $timeout(function () {
                    $scope.loadingHamilton = true;
                    var apiCall = Api.getHamiltonByBarcode(barcode).success(function (data) {
                        $scope.loadingHamilton = false;

                        //check to see if the scanned Hamilton is configured to run this step
                        if (!$scope.transformSpec.map.hamiltonDetails[data.barcode]) {
                            $scope.hamiltonBarcode = null;
                            $scope.hamiltonBarcodeErrorMessage = 'This step is not configured for Hamilton ' + data.label + '.';
                            $scope.hamiltonBarcodeErrorMessageVisible = -1;
                        } else {
                            $scope.flashHamiltonThumbsUp();
                            $scope.setSelectedHamilton(data);
                            $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_wizard', {
                                hamilton_info: $scope.selectedHamilton.barcode.toLowerCase() + '-' + Formatter.lowerCaseAndSpaceToDash(Formatter.dashToSpace($scope.selectedHamilton.label))
                            });
                        }
                    }).error(function (error) {
                        $scope.loadingHamilton = false;
                        $scope.hamiltonBarcode = null;
                        $scope.hamiltonBarcodeErrorMessage = 'The scanned barcode - <strong>' + barcode + '</strong> - was not found. Please re-scan.';
                        $scope.hamiltonBarcodeErrorMessageVisible = -1;
                    });
                }, 200);
            }
        };

        $scope.ignoreTab = function ($event) {
            if ($event.keyCode == 9) {
                $event.preventDefault();
                $event.stopPropagation();
                return false;
            }
        };

        $timeout(function () { jQuery('.twst-hamilton-wizard-hamilton-barcode-input').focus(); }, 0);
    }]
);
