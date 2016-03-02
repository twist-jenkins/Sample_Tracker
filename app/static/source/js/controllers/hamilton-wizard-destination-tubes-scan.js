angular.module('twist.app').controller('hamiltonWizardDestinationTubesScanController', ['$scope', '$state',  '$http', 'Api', '$timeout', 'Constants', 'Maps',
    function ($scope, $state, $http, Api, $timeout, Constants, Maps) {
        $scope.setGuidedPlacementMode(true);

        $scope.promptForTubePlacementScan = function () {
            $scope.clearGuidedScanInput();
            $scope.setCurrentStepInstruction('Scan a barcoded tube for placement.');
            $timeout(function () {
                $scope.setBarcodeInputFocus(jQuery('.twst-hamilton-guided-scan-input'));
            }, 0);
        };

        $scope.promptForTubePlacementScan();

        $scope.setActiveDeckRegion($scope.hamiltonDataObj.allDestinationPlates[0].carrier.selectedHamiltonDeckRegion);

        $scope.scannedTubeCount = 0;

        $scope.restartDestinationPlateScan = function () {
            for (var i=0; i<$scope.hamiltonDataObj.allDestinationPlates.length;i++) {
                var plate = $scope.hamiltonDataObj.allDestinationPlates[i];
                plate.barcode = null;
            }
            $scope.scannedTubeCount = 0;
            $scope.promptForTubePlacementScan();
        };

        $scope.tubePlacementComplete = function () {
            $scope.safeBarcodeInputBlur();
            if ($scope.scannedTubeCount == $scope.destinationPlatesNeedingScanCount && !$scope.savingSourcesAndDestinations) {
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
                                ,position: thisPlate.tubeRackRowColumn
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
                });
            }

        };

        $scope.checkAlreadyScannedTube = function (tubeBarcode) {
            var whichPlateArray = $scope.hamiltonDataObj.allDestinationPlates;

            for (var i=0; i<whichPlateArray.length;i++) {
                var thisPlate = whichPlateArray[i];
                if (thisPlate.barcode == tubeBarcode) {
                    return true;
                }
            }
            return false;
        }

        var barcodeFinishedTimeout = null;
        $scope.tubeScanned = function () {
            var itemBarcode = $scope.guidedScanInput.barcode;

            if (itemBarcode && itemBarcode.length) {
                $timeout.cancel(barcodeFinishedTimeout);
                if ($scope.checkAlreadyScannedTube(itemBarcode)) {
                    $scope.clearScannedItemErrorMessage();
                    $scope.showScannedItemErrorMessage('You have already scanned and placed a tube with this barcode.');
                    $scope.promptForTubePlacementScan();
                } else {
                    barcodeFinishedTimeout = $timeout(function () {
                        var shippingTubeBarcodeData = $scope.transformSpec.details.shippingTubeBarcodeData;

                        var found = false;

                        for(var i = 0; i < shippingTubeBarcodeData.length; i++) {
                            tube = shippingTubeBarcodeData[i];
                            if (tube["COI"] == itemBarcode) {
                                found = tube;
                                break;
                            }
                        }

                        if (!found) {
                            $scope.clearScannedItemErrorMessage();
                            $scope.showScannedItemErrorMessage('The scanned barcode does not match this batch. Please rescan.');
                            $scope.guidedScanInput.barcode = '';
                        } else {
                            $scope.tubeTargetWell = Maps.rowColumnMaps['SPTT_0005'][found["forWellNumber"]].row + Maps.rowColumnMaps['SPTT_0005'][found["forWellNumber"]].column;
                            $scope.clearScannedItemErrorMessage();
                            $scope.flashHamiltonThumbsUp();
                            $scope.setHighlightedPlate($scope.hamiltonDataObj.allDestinationPlates[found["forWellNumber"] - 1]);
                            $scope.safeBarcodeInputBlur();
                            $scope.setCurrentStepInstruction('Place the tube in rack position ' + $scope.tubeTargetWell);
                        }

                    }, 200);
                }
            }
        };

        $scope.tubePlaced = function () {
            $scope.highlightedPlate.barcode = $scope.guidedScanInput.barcode;
            $scope.highlightedPlate['tubeRackRowColumn'] = $scope.tubeTargetWell;
            $scope.clearScannedItemErrorMessage();
            $scope.flashHamiltonThumbsUp();
            $scope.scannedTubeCount++;
            $scope.setHighlightedPlate(null, null, true, true);
            if ($scope.scannedTubeCount != $scope.destinationPlatesNeedingScanCount) {
                $scope.promptForTubePlacementScan();
            } else {
                $scope.safeBarcodeInputBlur();
                $scope.setCurrentStepInstruction('You have finished placing tubes');
            }
        }

        $scope.tubeTargetWell = null;

        $scope.$on('$destroy', function () {
            $scope.setGuidedPlacementMode(false);
        });
    }]
);
