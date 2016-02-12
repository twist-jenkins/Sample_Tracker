angular.module('twist.app').controller('hamiltonWizardDestinationPlacementAndScanController', ['$scope', '$state',  '$http', 'Api', '$timeout', 'Constants',
    function ($scope, $state, $http, Api, $timeout, Constants) {

        $scope.setGuidedPlacementMode(true);
        $scope.setHighlightedPlate(null, null, true, true);
        $scope.safeBarcodeInputBlur();

        $scope.promptForDestinationPlacementScan = function () {
            $scope.clearGuidedScanInput();
            $scope.setCurrentStepInstruction('Scan a destination plate for placement.');
            $timeout(function () {
                $scope.setBarcodeInputFocus(jQuery('.twst-hamilton-guided-scan-input'));
            }, 0);
        };

        $scope.restartDestinationPlacementScan = function () {
            for (var i=0; i<$scope.hamiltonDataObj.allDestinationPlates.length;i++) {
                var plate = $scope.hamiltonDataObj.allDestinationPlates[i];
                plate.barcode = null;
            }
            $scope.scannedPlateCount = 0;
            $scope.promptForDestinationPlacementScan();
        };

        $scope.checkAlreadyScannedPlate = function (plateBarcode) {
            var whichPlateArray = $scope.hamiltonDataObj.allDestinationPlates;

            for (var i=0; i<whichPlateArray.length;i++) {
                var thisPlate = whichPlateArray[i];
                if (thisPlate.barcode == plateBarcode) {
                    return true;
                }
            }
            return false;
        }

        var barcodeFinishedTimeout = null;

        $scope.destinationPlateScanned = function () {
            var itemBarcode = $scope.guidedScanInput.barcode;

            if (itemBarcode && itemBarcode.length) {
                $timeout.cancel(barcodeFinishedTimeout);
                if ($scope.checkAlreadyScannedPlate(itemBarcode)) {
                    $scope.clearScannedItemErrorMessage();
                    $scope.showScannedItemErrorMessage('You have already scanned and placed this destination plate.');
                    $scope.promptForDestinationPlacementScan();
                } else {
                    barcodeFinishedTimeout = $timeout(function () {
                        var guidedDestinationPlacementData = $scope.transformSpec.details.guidedDestinationPlacementData;

                        var found = false;

                        for(var i = 0; i < guidedDestinationPlacementData.length; i++) {
                            plate = guidedDestinationPlacementData[i];
                            if (plate['barcode'] == itemBarcode) {
                                found = plate;
                                break;
                            }
                        }

                        if (!found) {
                            $scope.clearScannedItemErrorMessage();
                            $scope.showScannedItemErrorMessage('This barcode in not an expected destination plate. Please rescan.');
                            $scope.guidedScanInput.barcode = '';
                        } else {
                            $scope.flashHamiltonThumbsUp();
                            for (var i=0; i<$scope.hamiltonDataObj.allDestinationPlates.length;i++) {
                                var thisPlate = $scope.hamiltonDataObj.allDestinationPlates[i];
                                if (thisPlate.dataIndex == found['forPosition']) {
                                    $scope.setHighlightedPlate(thisPlate);
                                    break;
                                }
                            }
                            $scope.safeBarcodeInputBlur();
                            $scope.clearScannedItemErrorMessage();
                            $scope.destinationTargetPosition = found['forPosition'];
                            $scope.setCurrentStepInstruction('Place the plate in destination position ' + $scope.destinationTargetPosition);
                        }

                    }, 200);
                }
            }
        };

        $scope.scannedPlateCount = 0;

        $scope.destinationPlaced = function () {
            $scope.highlightedPlate.barcode = $scope.guidedScanInput.barcode;
            $scope.clearScannedItemErrorMessage();
            $scope.flashHamiltonThumbsUp();
            $scope.scannedPlateCount++;
            $scope.setHighlightedPlate(null, null, true, true);
            if ($scope.scannedPlateCount != $scope.destinationPlatesNeedingScanCount) {
                $scope.promptForDestinationPlacementScan();
            } else {
                $scope.safeBarcodeInputBlur();
                $scope.setCurrentStepInstruction('You have finished placing destination plates');
            }
        }

        $scope.destinationPlacementComplete = function () {
            if ($scope.scannedPlateCount == $scope.destinationPlatesNeedingScanCount) {
                $scope.safeBarcodeInputBlur();
                $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.destination_placement_confirmation');
            }
        };

        $scope.promptForDestinationPlacementScan();

        $scope.$on('$destroy', function () {
            $scope.setGuidedPlacementMode(false);
        });

    }]
);
