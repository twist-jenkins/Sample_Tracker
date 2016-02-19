angular.module('twist.app').controller('hamiltonWizardController', ['$scope', '$state', '$stateParams', 'Constants', 'Maps', 'Formatter', '$timeout', 'Api', '$sce',
    function ($scope, $state, $stateParams, Constants, Maps, Formatter, $timeout, Api, $sce) {

        $scope.Formatter = Formatter;

        $scope.hamiltonColumns = [];
        for (var i=0; i<68; i++) {
            $scope.hamiltonColumns.push({id: i});
        }

        $scope.carriers = Maps.carriers;

        $scope.tubeRowColumnMap = Maps.rowColumnMaps['SPTT_0005'];

        $scope.setSelectedHamilton = function (hamilton) {
            $scope.selectedHamilton = hamilton;
            $scope.hamiltonDataObj = {
                deckRegions: angular.copy($scope.transformSpec.map.hamiltonDetails[$scope.selectedHamilton.barcode])
            };
            $scope.decorateHamiltonDataObj($scope.hamiltonDataObj);
            $scope.hamiltonColumns = $scope.hamiltonColumns.slice(0, $scope.selectedHamilton.trackCount);
            $timeout(function () {
                if (!$scope.showFinishRunControls) {
                    $scope.highlightedPlate = null;
                    $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.carrier_scan');
                }
            }, 0);
        };

        $scope.clearHamiltonBarcodeErrorMessage = function () {
            $scope.hamiltonBarcodeErrorMessage = null;
            $scope.hamiltonBarcodeErrorMessageVisible = 0;
        }

        $scope.getHamiltonByBarcode = function(barcode) {
            if (!$scope.selectedHamilton || $scope.selectedHamilton.barcode != barcode) {
                $scope.loadingHamilton = true;
                Api.getHamiltonByBarcode(barcode).success(function (data) {
                    $scope.clearHamiltonBarcodeErrorMessage();
                    $scope.loadingHamilton = false;
                    $scope.setSelectedHamilton(data);
                }).error(function (error) {
                    $scope.loadingHamilton = false;
                    $scope.hamiltonBarcode = null;
                    $scope.hamiltonBarcodeErrorMessage = 'The scanned barcode - <strong>' + barcode + '</strong> - was not found. Please re-scan.';
                    $scope.hamiltonBarcodeErrorMessageVisible = -1;
                });
            }
        };

        $scope.changeHamilton = function () {
            $scope.selectedHamilton = null;
            $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_select');
        }

        $scope.selectedHamiltonInfo = $stateParams.hamilton_info;

        $scope.ignoreTab = function ($event) {
            if ($event.keyCode == 9) {
                $event.preventDefault();
                $event.stopPropagation();
                return false;
            }
        };

        /* methods for finish hamilton run */
        $scope.showFinishRun = function () {
            $scope.showFinishRunControls = true;
        };

        /* this function adds ordered arrays that reference the carriers and plates in their position in the deckRegions
         * It also adds back refs from a plate to its carrier and from a carrier to the hamiltonDeckRegion matching its deckRegion in the transform map
         * We'll use the ordered arrays for the guidance when scanning barcodes for carrier, carrier position & plate.
         * By looping through these arrays, we're actually moving through the deckRegions object's carriers and plates that back the UI
         */
        $scope.decorateHamiltonDataObj = function (hamObj) {
            hamObj.allCarriers = [];
            hamObj.allSourcePlates = [];
            hamObj.allDestinationPlates = [];
            for (region in hamObj.deckRegions) {
                var thisDeckRegion = hamObj.deckRegions[region];
                var theseCarriers = thisDeckRegion.carriers;
                for (var i=0; i<theseCarriers.length;i++) {
                    var thisCarrier = theseCarriers[i];
                    thisCarrier["selectedHamiltonDeckRegion"] = $scope.selectedHamilton.deckRegions[region];
                    hamObj.allCarriers.push(thisCarrier);
                }
            }
            for (var i=0; i<hamObj.allCarriers.length;i++) {
                var thisCarrier = hamObj.allCarriers[i];
                for (var j=0; j<thisCarrier.plates.length; j++) {
                    var thisPlate = thisCarrier.plates[j];
                    thisPlate["carrier"] = thisCarrier;
                    if (thisPlate.plateFor == 'source') {
                        hamObj.allSourcePlates.push(thisPlate);
                    } else if (thisPlate.plateFor == 'destination') {
                        hamObj.allDestinationPlates.push(thisPlate);
                    }

                }
            }

            hamObj.allCarriers.sort(function (a,b) {
                if (a.index < b.index) {
                    return -1;
                } else if (a.index > b.index) {
                    return 1;
                } else {
                    return 0;
                }
            });

            hamObj.allSourcePlates.sort(function (a,b) {
                if (a.dataIndex < b.dataIndex) {
                    return -1;
                } else if (a.dataIndex > b.dataIndex) {
                    return 1;
                } else {
                    return 0;
                }
            });

            hamObj.allDestinationPlates.sort(function (a,b) {
                if (a.dataIndex < b.dataIndex) {
                    return -1;
                } else if (a.dataIndex > b.dataIndex) {
                    return 1;
                } else {
                    return 0;
                }
            });
        }

        /* barcode input focus is important! these methods try to properly handle focus and blur on these special inputs */
        $scope.barcodeInputFocusLost = false;
        $scope.focusedInput = null;

        $scope.alertBarcodeInputFocusLost = function (targetInput) {
            $scope.barcodeInputFocusLost = true;
            $timeout(function () {
                if ($scope.barcodeInputFocusLost && $scope.focusedInput) {
                    $scope.showBarcodeInputFocusLost = true;
                }
            }, 150);
        }

        $scope.resumeScan = function () {
            $scope.setBarcodeInputFocus($scope.focusedInput);
        }

        $scope.setBarcodeInputFocus = function (input) {
            $scope.barcodeInputFocusLost = false;
            $scope.showBarcodeInputFocusLost = false;
            $scope.safeBarcodeInputBlur();
            $scope.focusedInput = input;
            input.focus().on('blur', function (event) {
                input.off('blur');
                $scope.alertBarcodeInputFocusLost(event.target);
            });
        };

        $scope.safeBarcodeInputBlur = function () {
            if ($scope.focusedInput) {
                $scope.focusedInput.off('blur').blur();
                $scope.focusedInput = null;
                $scope.barcodeInputFocusLost = false;
                $scope.showBarcodeInputFocusLost = false;
            }
        };

        $scope.checkAlreadyScannedCarrier = function (carrierBarcode) {
            /* carrierBarcode should only be in the list once  */
            var alreadyFound = false;
            for (var i=0; i<$scope.hamiltonDataObj.allCarriers.length;i++) {
                var thisCarrier = $scope.hamiltonDataObj.allCarriers[i];
                if (thisCarrier.barcode == carrierBarcode) {
                    if (alreadyFound) {
                        return true;
                    } else {
                        alreadyFound = true;
                    }
                }
            }
            return false;
        }

        $scope.checkAlreadyScannedPlate = function (plate) {
            /* plateBarcode should only be in the list once  */
            var alreadyFound = false;
            var plateBarcode = plate.barcode;
            var whichPlateArray = (plate.plateFor == Constants.PLATE_SOURCE ? $scope.hamiltonDataObj.allSourcePlates : $scope.hamiltonDataObj.allDestinationPlates);

            for (var i=0; i<whichPlateArray.length;i++) {
                var thisPlate = whichPlateArray[i];
                if (thisPlate.barcode == plateBarcode) {
                    if (alreadyFound) {
                        return true;
                    } else {
                        alreadyFound = true;
                    }
                }
            }
            return false;
        }

        /*
         * Functions in this scope for UI highlighting from (children) Hamilton Step controllers
         */
        $scope.setHighlightedCarrier = function (carrier) {
            $scope.highlightedCarrier = carrier;
            $scope.setStepInstruction(Constants.HAMILTON_ELEMENT_CARRIER, carrier);
            $timeout(function () {
                $scope.setBarcodeInputFocus(angular.element(document).find('.twst-hamilton-wizard-carrier-' + carrier.index + ' .twst-hamilton-wizard-carrier-input'))
            }, 0);
        }
        $scope.setHighlightedPlate = function (plate, which, skipInstructionSet, skipFocus) {
            if (!which) {
                which = Constants.HAMILTON_ELEMENT_PLATE;
            }
            $scope.highlightedPlate = plate;
            if (!skipInstructionSet) {
                $scope.setStepInstruction(which, plate);
            }
            if (!skipFocus) {
                $timeout(function () {
                    $scope.setBarcodeInputFocus(angular.element(document).find('.twst-hamilton-wizard-plate-' + plate.dataIndex + ' .twst-hamilton-wizard-plate-input'));
                }, 0);
            }
        }
        $scope.scannedCarrierCount = 0;
        $scope.findNextCarrierForScan = function () {
            var firstFound = false;
            var scannedCarrierCount = 0;
            for (var i=0; i<$scope.hamiltonDataObj.allCarriers.length;i++) {
                var carrier = $scope.hamiltonDataObj.allCarriers[i];
                if (!carrier.scanSkipped && !carrier.barcode && !firstFound) {
                    $scope.setHighlightedCarrier(carrier);
                    carrier.nextToScan = true;
                    firstFound = true;
                } else {
                    carrier.nextToScan = false;
                    if (carrier.barcode || carrier.scanSkipped) {
                        scannedCarrierCount++;
                    }
                }
            }
            $scope.scannedCarrierCount = scannedCarrierCount;

            if ($scope.scannedCarrierCount == $scope.hamiltonDataObj.allCarriers.length) {
                $scope.finishCarrierScan();
            }
        };

        $scope.sourcePlatesNeedingScanCount = 0;
        $scope.destinationPlatesNeedingScanCount = 0;

        $scope.setDestinationPlatesNeedingScanCount = function (val) {
            $scope.destinationPlatesNeedingScanCount = val;
        }

        $scope.finishCarrierScan = function () {
            $scope.safeBarcodeInputBlur();
            $scope.highlightedCarrier = null;
            for (var i=0; i<$scope.hamiltonDataObj.allSourcePlates.length;i++) {
                var thisPlate = $scope.hamiltonDataObj.allSourcePlates[i];
                if (!thisPlate.unused) {
                    $scope.sourcePlatesNeedingScanCount++;
                }
            }

            $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.source_scan');
        }

        $scope.scannedCarrierBarcode;
        var barcodeFinishedTimeout = null;
        $scope.carrierBarcodeScanned = function () {
            if ($scope.highlightedCarrier.barcode && $scope.highlightedCarrier.barcode.length) {
                $timeout.cancel(barcodeFinishedTimeout);
                if ($scope.checkAlreadyScannedCarrier($scope.highlightedCarrier.barcode)) {
                    $scope.clearScannedItemErrorMessage();
                    $scope.showScannedItemErrorMessage('The scanned barcode has already been scanned. Please scan the highlighted carrier.');
                    $scope.loadingCarrier = false;
                    $scope.highlightedCarrier.barcode = null;
                } else {
                    barcodeFinishedTimeout = $timeout(function () {
                        $scope.loadingCarrier = true;
                        Api.getCarrierByBarcode($scope.highlightedCarrier.barcode, $scope.selectedHamilton.barcode).success(function (data) {
                            $scope.loadingCarrier = false;
                            $scope.clearScannedItemErrorMessage();
                            $scope.flashHamiltonThumbsUp();
                            $scope.highlightedCarrier.positions = data.positions;
                            $scope.findNextCarrierForScan();
                        }).error(function (error) {
                            $scope.clearScannedItemErrorMessage();
                            $scope.showScannedItemErrorMessage('The scanned barcode - <strong>' + $scope.highlightedCarrier.barcode + '</strong> - was not found. Please re-scan.');
                            $scope.loadingCarrier = false;
                            $scope.highlightedCarrier.barcode = null;
                        });
                    }, 200);
                }
            }
        };
        $scope.clearScannedItemErrorMessage = function () {
            $scope.scannedItemErrorMessage = null;
            $scope.scannedItemErrorMessageVisible = 0;
        }
        $scope.showScannedItemErrorMessage = function (msg) {
            $scope.scannedItemErrorMessage = msg;
            $scope.scannedItemErrorMessageVisible = -1;
        }

        $scope.scannedSourcePlateCount = 0;
        $scope.scannedDestinationPlateCount = 0;
        $scope.findNextPlateForScan = function (plateFor, positionOrPlate) {
            var firstFound = false;
            var scannedPlateCount = 0;
            var whichPlateArray = (plateFor == Constants.PLATE_SOURCE ? $scope.hamiltonDataObj.allSourcePlates : $scope.hamiltonDataObj.allDestinationPlates);
            for (var i=0; i<whichPlateArray.length;i++) {
                var plate = whichPlateArray[i];
                if (!plate.barcode && !firstFound && !plate.unused) {
                    $scope.setHighlightedPlate(plate, positionOrPlate);
                    plate.nextToScan = true;
                    firstFound = true;
                } else {
                    plate.nextToScan = false;
                    if (plate.barcode && plateFor == plate.plateFor) {
                        scannedPlateCount++;
                    }
                }
            }
            if (plateFor == Constants.PLATE_SOURCE) {
                $scope.scannedSourcePlateCount = scannedPlateCount;
                if ($scope.scannedSourcePlateCount == $scope.sourcePlatesNeedingScanCount) {
                    $scope.highlightedPlate = null;
                    $scope.safeBarcodeInputBlur();
                }
            } else if (plateFor == Constants.PLATE_DESTINATION) {
                $scope.scannedDestinationPlateCount = scannedPlateCount;
                if ($scope.scannedDestinationPlateCount == $scope.destinationPlatesNeedingScanCount) {
                    $scope.highlightedPlate = null;
                    $scope.safeBarcodeInputBlur();
                }

            }
        };

        $scope.setActiveDeckRegion = function (region) {
            $scope.activeDeckRegion = region;
        }

        $scope.clearGuidedScanInput = function () {
            $scope.guidedScanInput = {barcode: ''};
        };
        $scope.clearGuidedScanInput();

        $scope.plateBarcodeScanned = function () {
            if ($scope.highlightedPlate.barcode && $scope.highlightedPlate.barcode.length) {
                $timeout.cancel(barcodeFinishedTimeout);
                /* Scanning plates is more complicated than carriers sincer we also scan carrier positions for plates
                 *  A plate can only be scanned after a carrier position, in pairwise fashion, for all 32 source plates
                 */

                /* if the plate's carrier position was already scanned, this should be a plate barcode
                 * otherwise it should be a carrier position barcode
                 */
                if ($scope.highlightedPlate.positionScanned) {
                    /* This should be a plate barcode. */
                    if ($scope.checkAlreadyScannedPlate($scope.highlightedPlate)) {
                        $scope.clearScannedItemErrorMessage();
                        $scope.showScannedItemErrorMessage('This plate has already been scanned. Please scan the <strong>barcode</strong> for ' + $scope.highlightedPlate.plateFor + ' plate ' + $scope.highlightedPlate.dataIndex);
                        $scope.highlightedPlate.barcode = null;
                    } else {
                        barcodeFinishedTimeout = $timeout(function () {
                            $scope.confirmingPlate = true;
                            if ($scope.highlightedPlate.plateFor == Constants.PLATE_SOURCE) {
                                Api.confirmPlateReadyForTransform($scope.highlightedPlate.barcode, $scope.transformSpec.details.transform_type_id).success(function (data) {
                                    $scope.confirmingPlate = false;
                                    $scope.clearScannedItemErrorMessage();
                                    $scope.flashHamiltonThumbsUp();
                                    $scope.findNextPlateForScan($scope.highlightedPlate.plateFor, Constants.HAMILTON_ELEMENT_CARRIER_POSITION);
                                }).error(function (error) {
                                    $scope.clearScannedItemErrorMessage();
                                    $scope.showScannedItemErrorMessage('The plate barcode was not found. Please scan the <strong>barcode</strong> for ' + $scope.highlightedPlate.plateFor + ' plate ' + $scope.highlightedPlate.dataIndex);
                                    $scope.confirmingPlate = false;
                                    $scope.highlightedPlate.barcode = null;
                                });
                            } else if ($scope.highlightedPlate.plateFor == Constants.PLATE_DESTINATION) {
                                Api.checkDestinationPlatesAreNew([$scope.highlightedPlate.barcode]).success(function (data) {
                                    if (!data.success) {
                                        /* plate already exists - error */
                                        $scope.clearScannedItemErrorMessage();
                                        $scope.showScannedItemErrorMessage('A plate already exists in the database with the scanned barcode.');
                                        $scope.confirmingPlate = false;
                                        $scope.highlightedPlate.barcode = null;
                                    } else {
                                        /* plate is new */
                                        $scope.confirmingPlate = false;
                                        $scope.clearScannedItemErrorMessage();
                                        $scope.flashHamiltonThumbsUp();
                                        $scope.findNextPlateForScan($scope.highlightedPlate.plateFor, Constants.HAMILTON_ELEMENT_CARRIER_POSITION);
                                    }
                                }).error(function (data) {
                                    $scope.clearScannedItemErrorMessage();
                                    $scope.showScannedItemErrorMessage('An error occured in checking this barcode. Please re-scan.');
                                    $scope.confirmingPlate = false;
                                    $scope.highlightedPlate.barcode = null;
                                });
                            }
                        }, 200);
                    }
                } else {
                    /* This should be a position barcode. Check the plate's carrier to see if this is a valid barcode and its the barcode for this position */
                    barcodeFinishedTimeout = $timeout(function () {
                        var positionBarcode = $scope.highlightedPlate.barcode;
                        var positionInCarrier = $scope.highlightedPlate.carrier.positions[positionBarcode];
                        if (positionInCarrier) {
                            if (positionInCarrier.index == $scope.highlightedPlate.localIndex) {
                                /* then we're ready for the plate barcode */
                                $scope.highlightedPlate.positionScanned = true;
                                $scope.highlightedPlate.barcode = null;
                                $scope.flashHamiltonThumbsUp();
                                $scope.findNextPlateForScan($scope.highlightedPlate.plateFor, Constants.HAMILTON_ELEMENT_PLATE);
                            } else {
                                /* right carrier but prompt operator to scan correct position barcode */
                                delete $scope.highlightedPlate.positionScanned;
                                $scope.showScannedItemErrorMessage('<strong>Incorrect position scanned:</strong> Please scan carrier ' + $scope.highlightedPlate.carrier.index + ' position ' + $scope.highlightedPlate.localIndex);
                                $scope.highlightedPlate.barcode = null;
                            }
                        } else {
                            /* scanned barcode is not a position on this carrier */
                            delete $scope.highlightedPlate.positionScanned;
                            $scope.showScannedItemErrorMessage('<strong>Invalid position barcode:</strong> Please scan carrier ' + $scope.highlightedPlate.carrier.index + ' position ' + $scope.highlightedPlate.localIndex);
                            $scope.highlightedPlate.barcode = null;
                        }
                    }, 200);
                }
            }
        };

        $scope.setCurrentStepInstruction = function (instruction) {
            $scope.currentStepInstruction = instruction;
        }
        $scope.setCurrentStepInstruction('Scan carriers from left to right');

        $scope.setStepInstruction = function (elementType, element) {
            if (elementType == Constants.HAMILTON_ELEMENT_CARRIER) {
                $scope.setCurrentStepInstruction('Scan the barcode for carrier ' + element.index);
            } else if (elementType == Constants.HAMILTON_ELEMENT_CARRIER_POSITION) {
                $scope.setCurrentStepInstruction('Scan the barcode for carrier ' + element.carrier.index + ' position ' + element.localIndex);
            } else if (elementType == Constants.HAMILTON_ELEMENT_PLATE) {
                $scope.setCurrentStepInstruction('Scan the barcode for ' + element.plateFor + ' plate ' + element.dataIndex);
            }
        };

        $scope.guidedPlacementMode = false;

        $scope.setGuidedPlacementMode = function (mode) {
            $scope.guidedPlacementMode = mode;
        };

        if ($scope.selectedHamiltonInfo) {
            if ($scope.selectedHamilton) {
                $scope.setSelectedHamilton($scope.selectedHamilton);
            } else {
                $scope.getHamiltonByBarcode($scope.selectedHamiltonInfo.split('-')[0].toUpperCase());
            }
        } else {
            $timeout(function () { jQuery('.twst-hamilton-wizard-hamilton-barcode-input').focus(); }, 0);
        }
    }]
);
