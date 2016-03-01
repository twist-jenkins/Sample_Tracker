angular.module('twist.app').controller('hamiltonWizardDestinationPlacementConfirmationController', ['$scope', '$state', '$stateParams', 'Api', '$timeout',
    function ($scope, $state, $stateParams, Api, $timeout) {
        $scope.confirmedDestinationCount = 0;

        $scope.placementConfirmation = {value: ''};

        $scope.findNextDestinationForConfirmation = function () {
            for (var i=0; i<$scope.hamiltonDataObj.allDestinationPlates.length;i++) {
                var thisPlate = $scope.hamiltonDataObj.allDestinationPlates[i];
                if (!thisPlate.unused && !thisPlate.barcode) {
                    $scope.setHighlightedPlate(thisPlate);
                    $scope.setCurrentStepInstruction('Scan position ' + thisPlate.localIndex + ' on carrier ' + thisPlate.carrier.index);
                    $timeout(function () {
                        $scope.setBarcodeInputFocus(jQuery('.twst-hamilton-placement-confirmation-input'));
                    }, 0);
                }
            }
        };

        $scope.restartConfirmation = function () {
            $scope.confirmedDestinationCount = 0;
            $scope.readyPlatesForConfirmation();
            $scope.findNextDestinationForConfirmation();
        }

        $scope.readyPlatesForConfirmation = function () {
            for (var i=0; i<$scope.hamiltonDataObj.allDestinationPlates.length;i++) {
                var thisPlate = $scope.hamiltonDataObj.allDestinationPlates[i];
                if (!thisPlate.unused) {
                    thisPlate['confirm_barcode'] = thisPlate.barcode;
                    thisPlate.barcode = null;
                    delete thisPlate.positionScanned;
                }
            }
        }

        var scannedValFinishedTimeout = null;

        $scope.placementConfirmationScanned = function () {
            var scannedVal = $scope.placementConfirmation.value;

            if (scannedVal && scannedVal.length) {
                $timeout.cancel(scannedValFinishedTimeout);
                scannedValFinishedTimeout = $timeout(function () {
                    scannedVal = $scope.placementConfirmation.value;
                    if ($scope.highlightedPlate.positionScanned) {
                        //then we should confirm the plate's barcode
                        if ($scope.highlightedPlate.confirm_barcode == scannedVal) {
                            $scope.highlightedPlate.barcode = scannedVal;
                            $scope.flashHamiltonThumbsUp();
                            $scope.confirmedDestinationCount++;
                            $scope.placementConfirmation.value = '';
                            if ($scope.confirmedDestinationCount == $scope.destinationPlatesNeedingScanCount) {
                                $scope.setHighlightedPlate(null, null, true, true);
                                $scope.setCurrentStepInstruction('All destination positions confirmed');
                            } else {
                                $scope.findNextDestinationForConfirmation();
                            }

                        } else {
                            $scope.clearScannedItemErrorMessage();
                            $scope.placementConfirmation.value = '';
                            $scope.showScannedItemErrorMessage('Unexpected barcode. Please scan the <strong>plate</strong> in this position.');
                        }

                    } else {
                        if ($scope.highlightedPlate.carrier.positions[scannedVal] && $scope.highlightedPlate.carrier.positions[scannedVal].index == $scope.highlightedPlate.localIndex) {
                            $scope.clearScannedItemErrorMessage();
                            $scope.flashHamiltonThumbsUp();
                            $scope.highlightedPlate.positionScanned = true;
                            $scope.placementConfirmation.value = '';
                            $scope.setCurrentStepInstruction('Scan the plate in this position');
                        } else {
                            $scope.clearScannedItemErrorMessage();
                            $scope.placementConfirmation.value = '';
                            $scope.showScannedItemErrorMessage('Unexpected barcode. Please scan carrier ' + $scope.highlightedPlate.carrier.index + ' position ' + $scope.highlightedPlate.localIndex);
                        }
                    }

                }, 200);
            }
        }

        $scope.confirmationComplete = function () {
            $scope.safeBarcodeInputBlur();
            if ($scope.confirmedDestinationCount == $scope.destinationPlatesNeedingScanCount && !$scope.savingSourcesAndDestinations) {
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
        }

        $scope.readyPlatesForConfirmation();
        $scope.findNextDestinationForConfirmation();
    }]
);
