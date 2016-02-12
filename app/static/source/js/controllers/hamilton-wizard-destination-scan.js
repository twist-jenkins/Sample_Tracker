angular.module('twist.app').controller('hamiltonWizardDestinationScanController', ['$scope', '$state',  '$http', 'Api', '$timeout', 'Constants',
    function ($scope, $state, $http, Api, $timeout, Constants) {
        console.log($scope.hamiltonDataObj);
        $scope.restartDestinationPlateScan = function () {
            for (var i=0; i<$scope.hamiltonDataObj.allDestinationPlates.length;i++) {
                var plate = $scope.hamiltonDataObj.allDestinationPlates[i];
                plate.barcode = null;
                plate.positionScanned = null;
            }
            $scope.findNextPlateForScan(Constants.PLATE_DESTINATION, Constants.HAMILTON_ELEMENT_CARRIER_POSITION);
        };

        $scope.destinationPlateScanComplete = function () {
            $scope.safeBarcodeInputBlur();
            if ($scope.scannedDestinationPlateCount == $scope.destinationPlatesNeedingScanCount && !$scope.savingSourcesAndDestinations) {
                $scope.transformSpec.sources = [];
                $scope.transformSpec.destinations = [];


                for (var i=0; i<$scope.hamiltonDataObj.allSourcePlates.length; i++) {
                    var thisPlate = $scope.hamiltonDataObj.allSourcePlates[i];
                    if (thisPlate.barcode) {
                        $scope.transformSpec.sources.push({
                            details: {
                                id: thisPlate.barcode
                                ,dataIndex: thisPlate.dataIndex
                                ,position: 'C' + thisPlate.carrier.index + 'P' + thisPlate.localIndex
                            }
                        });
                    }
                }
                for (var i=0; i<$scope.hamiltonDataObj.allDestinationPlates.length; i++) {
                    var thisPlate = $scope.hamiltonDataObj.allDestinationPlates[i];
                    if (thisPlate.barcode) {
                        $scope.transformSpec.destinations.push({
                            details: {
                                id: thisPlate.barcode
                                ,dataIndex: thisPlate.dataIndex
                                ,position: 'C' + thisPlate.carrier.index + 'P' + thisPlate.localIndex
                            }
                        });
                    }
                }

                $scope.transformSpec.details.source_plate_count = $scope.sourcePlatesNeedingScanCount;
                $scope.transformSpec.details.destination_plate_count = $scope.destinationPlatesNeedingScanCount;
                $scope.transformSpec.details.hamilton = $scope.selectedHamilton;

                $scope.savingSourcesAndDestinations = true;

                Api.saveAndConditionallyExecuteTransformSpec($scope.transformSpec.serialize(), false).success(function (data) {
                    $scope.savingSourcesAndDestinations = false;
                    var savedSpecId = data.data.spec_id;
                    $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.finish_run', {
                        saved_spec_id: savedSpecId
                    });

                }).error(function (data) {
                    $scope.savingSourcesAndDestinations = false;
                    console.log(data);
                });;
            }

        };

        if ($scope.hamiltonDataObj.allSourcePlates.length && !$scope.hamiltonDataObj.allDestinationPlates.length) {
            $scope.destinationPlateScanComplete();
        } else {
            $scope.findNextPlateForScan(Constants.PLATE_DESTINATION, Constants.HAMILTON_ELEMENT_CARRIER_POSITION);
        }
    }]
);
