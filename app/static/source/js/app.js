var app;

app = angular.module('twist.app', ['ui.router', 'ui.bootstrap', 'ngSanitize', 'templates-main', 'LocalStorageModule'])


.controller('rootController', ['$scope', '$state', 'User', '$rootScope', 'localStorageService', '$location', '$timeout',  
    function ($scope, $state, User, $rootScope, localStorageService, $location, $timeout) {
        $scope.user = User;
        $scope.current_year = (new Date).getFullYear();

        $scope.navTo = function (where) {
            $state.go(where);
        }

        var loginStateName = 'root.login';

        $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState) {
            if (!User.data && toState.name != loginStateName) {
                event.preventDefault();
                $state.go(loginStateName);
            }
        });

        $rootScope.$on('$stateChangeSuccess', function(event, toState) {
            $scope.currentNav = toState.name;
        });

        $rootScope.$on('$locationChangeSuccess', function(event) {
            var url = document.location.href;
            var hashUrl = url.substring(url.indexOf('#') + 1);
            if (url != hashUrl && hashUrl != '/login') {
                localStorageService.set('loginTarget', hashUrl);
            }
        });

        $scope.currentNav = $state.current.name;
    }]
)

.controller('loginController', ['$scope', '$state',  '$http', 'localStorageService', 
    function ($scope, $state, $http, localStorageService) {
        $http({url: '/google-login'}).success(function (data) {
            $scope.googleLoginUrl = data.login_url;
        }).error(function () {
            $scope.loginPageError = true;
        });
    }]
)

.controller('trackStepController', ['$scope', '$state', 'Api', '$sce', '$timeout', 'Formatter', 'TypeAhead', 'Maps', 'Constants', 'TransformBuilder', 'FileParser', 
    function ($scope, $state, Api, $sce, $timeout, Formatter, TypeAhead, Maps, Constants, TransformBuilder, FileParser) {

        $scope.stepTypeDropdownValue = Constants.STEP_TYPE_DROPDOWN_LABEL;

        $scope.Constants = Constants;

        $scope.transformSpec = TransformBuilder.newTransformSpec();
        $scope.transformSpec.setPlateStepDefaults();

        $scope.selectStepType = function (option) {
            $scope.transformSpec.setTransformSpecDetails(option);
            $scope.transformSpec.setTitle(option.text);

            var route = 'root.record_transform.step_type_selected.tab_selected';

            var whichTab = Constants.STANDARD_TEMPLATE;

            if ($scope.transformSpec.map.type == Constants.USER_SPECIFIED_TRANSFER_TYPE) {
                whichTab = Constants.FILE_UPLOAD;
            } else if ($scope.transformSpec.map.type == Constants.HAMILTON_TRANSFER_TYPE) {
                whichTab = Constants.HAMILTON_OPERATION;
            }

            $state.go(route, {
                selected_step_type_id: option.id + '-' + Formatter.lowerCaseAndSpaceToDash(Formatter.stripNonAlphaNumeric(option.text, true, true).trim())
                ,selected_tab: whichTab
            });
        }

        $scope.setSelectedOption = function (optionId) {
            for (var i=0; i< $scope.stepTypeOptions.length;i++) {
                var option = $scope.stepTypeOptions[i];
                if (option.id == optionId) {
                    $scope.submissionResultMessage = '';
                    $scope.submissionResultVisible = 0;
                    $scope.transformSpec.setTransformSpecDetails(option);
                    $scope.transformSpec.setTitle(option.text)
                    $scope.stepTypeDropdownValue = $scope.transformSpec.details.text;
                    break;
                }
            }

            if ($scope.transformSpec.map.type == Constants.USER_SPECIFIED_TRANSFER_TYPE) {
                $scope.templateTypeSelection = Constants.FILE_UPLOAD;
            } else if ($scope.transformSpec.map.type == Constants.HAMILTON_TRANSFER_TYPE) {
                $scope.templateTypeSelection = Constants.HAMILTON_OPERATION;
            } else {
                $scope.templateTypeSelection = Constants.STANDARD_TEMPLATE;
            }
        }

        $scope.sampleTrackFormReady = function () {

            if (!$scope.transformSpec.details) {
                return false;
            }

            if (!$scope.transformSpec.operations || !$scope.transformSpec.operations.length) {
                return false
            }

            return true;
        }

        var getSampleTrackSubmitData = function () {
            var data = {
                sampleTransferTypeId: $scope.transformSpec.details.id
                ,sampleTransferTemplateId: $scope.transformSpec.details.transfer_template_id
            };

            data.transferMap = $scope.transformSpec.operations;

            return data;
        };

        $scope.submitStep = function () {

            var showError = function (data) {
                $scope.submissionResultMessage = 'Error: ' + data.errors;
                $scope.submissionResultVisible = -1;
                $scope.submittingStep = false;
            }

            var executeNow = true;

            //the newer specs are the ones that save the transform but do not execute it immediately
            if ($scope.transformSpec.details.transfer_template_id == 25 || 
                $scope.transformSpec.details.transfer_template_id == 26 || 
                $scope.transformSpec.details.transfer_template_id == 27 || 
                $scope.transformSpec.details.transfer_template_id == 28 || 
                $scope.transformSpec.details.transfer_template_id == 29 ||
                $scope.transformSpec.details.transfer_template_id == 30 ||
                $scope.transformSpec.details.transfer_template_id == 31) {
                executeNow = false;
            }

            if (!$scope.submitting && $scope.sampleTrackFormReady() && !$scope.transformSpec.updating) {

                $scope.submittingStep = true;

                Api.saveAndConditionallyExecuteTransformSpec($scope.transformSpec.serialize(), executeNow).success(function (data) {

                    if (!data.errors || !data.errors.length) {
                        $scope.submittingStep = false;
                        $scope.submissionResultMessage = 'This <span class="twst-step-text">' + $scope.transformSpec.details.text + '</span> step was successfully recorded.';
                        $scope.submissionResultVisible = 1;
                        $scope.clearForm();
                    } else {
                        showError(data);
                    }

                    $timeout(function () {
                        $scope.submissionResultVisible = 0;
                        $timeout(function () {
                            $scope.submissionResultMessage = null;
                        }, 400);
                    }, 5000);

                }).error(function (data) {
                    $scope.submittingStep = false;
                    showError(data);
                });;
            }
        };

        $scope.clearForm = function (skipGo) {
            $scope.stepTypeDropdownValue = Constants.STEP_TYPE_DROPDOWN_LABEL;
            $scope.transformSpec = TransformBuilder.newTransformSpec();
            $scope.transformSpec.setPlateStepDefaults();
            $scope.templateTypeSelection = null;
            if (!skipGo) {
                $state.go('root.record_transform');
            }
        };

        /* populate the sample types pulldown */
        $scope.initTransferTypes = Api.getSampleTransferTypes();
        $scope.initTransferTypes.success(function (data) {
            if (data.success) {
                $scope.stepTypeOptions = data.results;
            }
        });
    }]
)

.controller('stepTypeSelectedController', ['$scope', '$state',  '$stateParams', '$sce', '$timeout', 'Formatter', 'TypeAhead', 'Maps', 'Constants', 'TransformBuilder', 'FileParser', 
    function ($scope, $state, $stateParams, $sce, $timeout, Formatter, TypeAhead, Maps, Constants, TransformBuilder, FileParser) {

        $scope.Constants = Constants;

        $scope.selectTransferTemplateType = function (which, skipGo) {
            if (which == Constants.HAMILTON_OPERATION && !$scope.isHamiltonStep()) {
                return false;
            } else if (which != Constants.HAMILTON_OPERATION && $scope.isHamiltonStep()) {
                return false;
            } 
            if (!skipGo) {
                $state.go('root.record_transform.step_type_selected.tab_selected', {
                    selected_tab: which
                });
            }
        };

        $scope.setTransferTemplate = function (which) {
            $scope.templateTypeSelection = which;
        };

        $scope.isHamiltonStep = function () {
            if (selectedTranferTypeId == 39 || selectedTranferTypeId == 48 || selectedTranferTypeId == 51) {
                return true; 
            }
            return false;
        }

        var selectedTranferTypeId;
        $scope.initTransferTypes.success(function (data) {
            selectedTranferTypeId = $stateParams.selected_step_type_id.split('-')[0];
            $scope.setSelectedOption(selectedTranferTypeId);
        });

        $scope.$on('$destroy', function () {
            $scope.clearForm(true);
        });
    }]
)

.controller('tabSelectedController', ['$scope', '$state', '$stateParams', '$element', '$sce', '$timeout', 'Formatter', 'TypeAhead', 'Maps', 'Constants', 'TransformBuilder', 'FileParser', 
    function ($scope, $state, $stateParams, $element, $sce, $timeout, Formatter, TypeAhead, Maps, Constants, TransformBuilder, FileParser) {

        $scope.getTypeAheadBarcodes = TypeAhead.getTypeAheadBarcodes;

        $scope.excelFileStats = {};
        $scope.fileErrors = [];

        $scope.Constants = Constants;

        $scope.cachedFileData = null;

        /* refresh the current transfer plan based on changes to plates inputs or upload file */
        $scope.updateTransferPlan = function (val, which, itemIndex) {
            if (val && val.length > 5) {
                if (which == Constants.PLATE_SOURCE) {
                    $scope.transformSpec.addSource(itemIndex);
                } else if (which == Constants.PLATE_DESTINATION) {
                    $scope.transformSpec.addDestination(itemIndex);
                }
            } else {
                if (which == Constants.PLATE_SOURCE) {
                    $scope.transformSpec.checkSourcesReady();
                } else if (which == Constants.PLATE_DESTINATION) {
                    $scope.transformSpec.checkDestinationsReady();
                }
            }
        };

        $scope.$watch('templateTypeSelection', function (newVal, oldVal) {
            if (newVal == Constants.FILE_UPLOAD && $scope.cachedFileData) {
                $scope.catchFile();
            } else if (newVal == Constants.STANDARD_TEMPLATE) {
                $scope.transformSpec.transferFromFile(false);
            }
        });

        $scope.clearExcelUploadData = function () {
            $scope.excelFileStats = {};
            $scope.fileErrors = [];
        };

        $scope.catchFile = function (fileData, error) {
            $scope.parsingFile = true;

            if (error) {
                $scope.clearExcelUploadData();
                $scope.fileErrors.push(error);
                $scope.excelFileStats = {};
                $scope.transformSpec.clearOperationsList();
                $scope.parsingFile = false;
            } else {
                // called in timeout to give the spinner time to render
                $timeout(function () {
                    $scope.clearExcelUploadData();

                    if (!fileData) {
                        fileData = $scope.cachedFileData;
                    } else {
                        $scope.cachedFileData = fileData;
                    };

                    FileParser.getTransferRowsFromFile(fileData, $scope.transformSpec).then(function (resultData) {
                        $scope.excelFileStats = resultData.stats;
                        $scope.fileErrors = resultData.errors;

                        if (!resultData.errors.length) {
                            $scope.transformSpec.transferFromFile(true, resultData);
                        } else {
                            $scope.transformSpec.clearOperationsList();
                        } 

                        $scope.parsingFile = false;

                    }, function (errorData) {
                        $scope.fileErrors = 'Error: Unknown error while parsing this file.';
                        $scope.parsingFile = false;
                    });
     
                }, 150);
            }
        };

        $scope.startHamiltonSteps = function () {
            $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_select');
        }

        $scope.setSelectedHamilton = function (hamilton) {
            $scope.selectedHamilton = hamilton;
        }

        $scope.hamiltonThumbsUp = [];
        $scope.now = new Date();

        $scope.flashHamiltonThumbsUp = function () {
            $scope.hamiltonThumbsUp.push({id: $scope.now.toString(), index: $scope.hamiltonThumbsUp.length});
        };

        $scope.finishHamiltonThumbsUpFade = function (thumbsUp) {
            $scope.hamiltonThumbsUp.splice(thumbsUp.index, 1);
        }

        $scope.selected_tab = $stateParams.selected_tab;
        $scope.setTransferTemplate($scope.selected_tab);
    }]
)

.controller('hamiltonSelectController', ['$scope', '$state', '$stateParams', 'Constants', 'Maps', 'Formatter', '$timeout', 'Api', 
    function ($scope, $state, $stateParams, Constants, Maps, Formatter, $timeout, Api) {
        $scope.hamiltonBarcodeChange = function () {
            $timeout.cancel($scope.hamiltonBarcodeChangeTimeout);
            var barcode = $scope.hamiltonBarcode.trim();
            if (barcode != '' && barcode.length > 4) {
                $scope.hamiltonBarcodeChangeTimeout = $timeout(function () {
                    $scope.loadingHamilton = true;
                    var apiCall = Api.getHamiltonByBarcode(barcode).success(function (data) {
                        $scope.loadingHamilton = false;
                        $scope.flashHamiltonThumbsUp();
                        $scope.setSelectedHamilton(data);
                        $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_wizard', {
                            hamilton_info: $scope.selectedHamilton.barcode.toLowerCase() + '-' + Formatter.lowerCaseAndSpaceToDash(Formatter.dashToSpace($scope.selectedHamilton.label))
                        });
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
)

.controller('hamiltonWizardController', ['$scope', '$state', '$stateParams', 'Constants', 'Maps', 'Formatter', '$timeout', 'Api', '$sce', 
    function ($scope, $state, $stateParams, Constants, Maps, Formatter, $timeout, Api, $sce) {

        $scope.Formatter = Formatter;

        $scope.hamiltonColumns = [];
        for (var i=0; i<68; i++) {
            $scope.hamiltonColumns.push({id: i});
        }

        $scope.carriers = Maps.carriers;

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
                    $scope.setSelectedHamilton(data)
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
            $scope.setCurrentStepInstruction(Constants.HAMILTON_ELEMENT_CARRIER, carrier);
            $timeout(function () {
                jQuery('.twst-hamilton-wizard-carrier-' + carrier.index + ' .twst-hamilton-wizard-carrier-input').focus();
            }, 0);
        }
        $scope.setHighlightedPlate = function (plate, which, skipInstructionSet, skipFocus) {
            if (!which) {
                which = Constants.HAMILTON_ELEMENT_PLATE;
            }
            $scope.highlightedPlate = plate;
            if (!skipInstructionSet) {
                $scope.setCurrentStepInstruction(which, plate);
            }
            if (!skipFocus) {
                $timeout(function () {
                    jQuery('.twst-hamilton-wizard-plate-' + plate.dataIndex + ' .twst-hamilton-wizard-plate-input').focus();
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
            } else if (plateFor == Constants.PLATE_DESTINATION) {
                $scope.scannedDestinationPlateCount = scannedPlateCount;
                if ($scope.scannedDestinationPlateCount == $scope.hamiltonDataObj.allDestinationPlates.length) {
                    $scope.highlightedPlate = null;
                    jQuery('input:focus').trigger('blur');
                }

            }
        };

        $scope.setActiveDeckRegion = function (region) {
            $scope.activeDeckRegion = region;
        }

        $scope.setScannedTubeCount = function (val) {
            $scope.scannedTubeCount = val;
        };

        $scope.setScannedTubeCount(0);
        
        $scope.shippingTubeScanInput = {barcode: ''};

        $scope.promptForDestinationTubeScan = function () {
            $scope.shippingTubeScanInput = {barcode: ''};
            $scope.currentStepInstruction = 'Scan a barcoded tube for placement.';
            $timeout(function () {
                jQuery('.twst-hamilton-shipping-tube-scan-input').focus();
            }, 0);
        };

        $scope.tubePlaced = function () {
            $scope.highlightedPlate.barcode = $scope.shippingTubeScanInput.barcode;
            $scope.highlightedPlate['tubeRackRowColumn'] = $scope.tubeTargetWell;
            $scope.clearScannedItemErrorMessage();
            $scope.flashHamiltonThumbsUp();
            $scope.scannedTubeCount++;
            $scope.highlightedPlate = null;
            if ($scope.scannedTubeCount != $scope.destinationPlatesNeedingScanCount) {
                $scope.promptForDestinationTubeScan();
            } else {
                jQuery('input:focus').trigger('blur');
                $scope.currentStepInstruction = 'You have finished placing tubes';
            }
        }

        $scope.tubeTargetWell = null;

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

        $scope.shippingTubeScanned = function () {
            var tubeBarcode = $scope.shippingTubeScanInput.barcode;

            if (tubeBarcode && tubeBarcode.length) {
                $timeout.cancel(barcodeFinishedTimeout);
                if ($scope.checkAlreadyScannedTube(tubeBarcode)) {
                    $scope.clearScannedItemErrorMessage();
                    $scope.showScannedItemErrorMessage('You have already scanned and placed a tube with this barcode.');
                    $scope.promptForDestinationTubeScan();
                } else {
                    barcodeFinishedTimeout = $timeout(function () {
                        var shippingTubeBarcodeData = $scope.transformSpec.details.shippingTubeBarcodeData;

                        var found = false;

                        for(var i = 0; i < shippingTubeBarcodeData.length; i++) {
                            tube = shippingTubeBarcodeData[i];
                            if (tube["COI"] == tubeBarcode) {
                                found = tube;
                                break;
                            }
                        }

                        if (!found) {
                            $scope.clearScannedItemErrorMessage();
                            $scope.showScannedItemErrorMessage('The scanned barcode does not match this batch. Please rescan.');
                            $scope.shippingTubeScanInput.barcode = '';
                        } else {
                            $scope.tubeTargetWell = Maps.rowColumnMaps['SPTT_0005'][found["forWellNumber"]].row + Maps.rowColumnMaps['SPTT_0005'][found["forWellNumber"]].column;
                            $scope.clearScannedItemErrorMessage();
                            $scope.flashHamiltonThumbsUp();
                            $scope.setHighlightedPlate($scope.hamiltonDataObj.allDestinationPlates[found["forWellNumber"] - 1]);
                            jQuery('input:focus').trigger('blur');
                            $scope.currentStepInstruction = 'Place the tube in rack position ' + $scope.tubeTargetWell;
                        }

                    }, 200);
                }
            }
        };

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
                                Api.confirmPlateReadyForTransform($scope.highlightedPlate.barcode, $scope.transformSpec.details.transfer_type_id).success(function (data) {
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

        $scope.currentStepInstruction = 'Scan carriers from left to right';

        $scope.setCurrentStepInstruction = function (elementType, element) {
            if (elementType == Constants.HAMILTON_ELEMENT_CARRIER) {
                $scope.currentStepInstruction = 'Scan the barcode for carrier ' + element.index;  
            } else if (elementType == Constants.HAMILTON_ELEMENT_CARRIER_POSITION) {
                $scope.currentStepInstruction = 'Scan the barcode for carrier ' + element.carrier.index + ' position ' + element.localIndex;  
            } else if (elementType == Constants.HAMILTON_ELEMENT_PLATE) {
                $scope.currentStepInstruction = 'Scan the barcode for ' + element.plateFor + ' plate ' + element.dataIndex;  
            }
        };

        $scope.tubeDestinationsMode = false;

        $scope.setTubeDestinationsMode = function (mode) {
            $scope.tubeDestinationsMode = mode;
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
)

.controller('hamiltonWizardCarrierScanController', ['$scope', '$state',  '$http', 'Api', '$timeout', 
    function ($scope, $state, $http, Api, $timeout) {
        $scope.findNextCarrierForScan();
        console.log($scope.hamiltonDataObj);
        $scope.restartCarrierScan = function () {
            for (var i=0; i<$scope.hamiltonDataObj.allCarriers.length;i++) {
                var carrier = $scope.hamiltonDataObj.allCarriers[i];
                carrier.barcode = null;
                carrier.scanSkipped = null;
            }
            $scope.findNextCarrierForScan();
        }

        $scope.skipCurrentCarrierScan = function () {

            var whichKind = '';

            for (var j=0; j<$scope.highlightedCarrier.plates.length; j++) {
                if (whichKind = $scope.highlightedCarrier.plates[j].plateFor) {
                    break;
                }
            }

            if (whichKind != '') {

                var scannedCarrierOfWhichKindCount = 0;
                var carriersLeftOfWhichKindCount = 0;
                /* we have to have at least 1 source and 1 destination carrier */
                for (var i=0; i<$scope.hamiltonDataObj.allCarriers.length;i++) {
                    var carrier = $scope.hamiltonDataObj.allCarriers[i];
                    // skip the current carrier
                    if ($scope.highlightedCarrier.index != carrier.index) {
                        if (carrier.plates[0].plateFor == whichKind) {
                            if (carrier.barcode) {
                                scannedCarrierOfWhichKindCount++;
                            } else if (carrier.index > $scope.highlightedCarrier.index) {
                                carriersLeftOfWhichKindCount++;
                            }
                        }
                    }
                }

                if (!scannedCarrierOfWhichKindCount && !carriersLeftOfWhichKindCount) {
                    $scope.showScannedItemErrorMessage('You must scan <strong>at least one ' + whichKind + ' carrier</strong>.');
                    $scope.setHighlightedCarrier($scope.highlightedCarrier);
                } else {
                    $scope.highlightedCarrier.scanSkipped = true;
                    for (var j=0; j<$scope.highlightedCarrier.plates.length; j++) {
                        $scope.highlightedCarrier.plates[j].unused = true;
                    }
                    $scope.findNextCarrierForScan();
                }

            } else {
                console.log('Highlighted carrier has no used plates.');
            }
        }
    }]
)

.controller('hamiltonWizardSourceScanController', ['$scope', '$state',  '$http', 'Api', '$timeout', 'Constants', 
    function ($scope, $state, $http, Api, $timeout, Constants) {
        $scope.findNextPlateForScan(Constants.PLATE_SOURCE, Constants.HAMILTON_ELEMENT_CARRIER_POSITION);
        
        $scope.restartSourcePlateScan = function () {
            for (var i=0; i<$scope.hamiltonDataObj.allSourcePlates.length;i++) {
                var plate = $scope.hamiltonDataObj.allSourcePlates[i];
                plate.barcode = null;
                plate.positionScanned = null;
            }
            $scope.findNextPlateForScan(Constants.PLATE_SOURCE, Constants.HAMILTON_ELEMENT_CARRIER_POSITION);
        };

        $scope.sourcePlateScanComplete = function () {
            if ($scope.scannedSourcePlateCount && !$scope.processingSources) {

                /* TODO: api call to submit source plates and get # of destination plates        */

                var scannedPlateBarcodes = [];

                for (var i=0; i<$scope.hamiltonDataObj.allSourcePlates.length;i++) {
                    var plate = $scope.hamiltonDataObj.allSourcePlates[i];
                    if (plate.barcode) {
                        scannedPlateBarcodes.push(plate.barcode);
                    } else {
                        plate.unused = true;
                    }
                }

                $scope.processingSources = true;

                Api.processHamiltonSources(scannedPlateBarcodes, $scope.transformSpec.details.transfer_type_id).success(function (data) {
                    console.log(data);
                    $scope.processingSources = false;
                    var responseCommands =  data.responseCommands;

                    if (!responseCommands.length) {
                        $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.destination_scan');
                    } else {

                        for (var i=0; i< responseCommands.length; i++) {
                            var command = responseCommands[i];

                            var commandType = command.type

                            switch (commandType) {
                                case Constants.RESPONSE_COMMANDS_SET_DESTINATIONS:
                                    var destinationPlateCount = command.plates.length;

                                    var newAllDestinationPlates = [];

                                    var skippedCarrierPlatesCount = 0;

                                    $scope.setDestinationPlatesNeedingScanCount(0);

                                    var destinationPlatesNeedingScanCount = 0;

                                    for (var j=0; j<$scope.hamiltonDataObj.allDestinationPlates.length;j++) {
                                        var plate = $scope.hamiltonDataObj.allDestinationPlates[j];

                                        if (plate.carrier.scanSkipped) {
                                            skippedCarrierPlatesCount += plate.carrier.plates.length;
                                        } else {
                                            plate.optional = false;
                                            if (plate.dataIndex - skippedCarrierPlatesCount > destinationPlateCount) {
                                                plate.unused = true;
                                            } else {
                                                newAllDestinationPlates.push(plate);
                                            }
                                        }

                                        if (!plate.unused) {
                                            destinationPlatesNeedingScanCount++;
                                        }
                                    }
                                    $scope.setDestinationPlatesNeedingScanCount(destinationPlatesNeedingScanCount);

                                    $scope.hamiltonDataObj.allDestinationPlates = newAllDestinationPlates;
                                    break;
                                case Constants.RESPONSE_COMMANDS_ADD_TRANSFORM_SPEC_DETAIL:
                                    $scope.transformSpec.details[command.detail.key] = command.detail.value;
                                    break;
                                default :
                                    console.log('Error: Unrecognized command type = [' + command.type + ']');
                                    break;
                            }
                        }

                        switch ($scope.transformSpec.details.transfer_type_id) {
                            case 39:
                            case 48:
                                $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.destination_scan');
                                break;
                            case 51:
                                $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.label_destination_tubes');
                                break;
                            default:
                                console.log('Unexpected transfer_type_id = [' + $scope.transformSpec.details.transfer_type_id + ']');
                                break;

                        }

                    }

                }).error(function (error) {
                    $scope.processingSources = false;
                    $scope.clearScannedItemErrorMessage();
                    $scope.showScannedItemErrorMessage('There was an error processing these sources. Please try again.');
                });
            }
        };
    }]
)

.controller('hamiltonWizardDestinationScanController', ['$scope', '$state',  '$http', 'Api', '$timeout', 'Constants', 
    function ($scope, $state, $http, Api, $timeout, Constants) {
        $scope.findNextPlateForScan(Constants.PLATE_DESTINATION, Constants.HAMILTON_ELEMENT_CARRIER_POSITION);
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
            /* TODO save transform spec show worklist download link */
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
    }]
)

.controller('hamiltonWizardLabelDestinationTubesController', ['$scope', '$state',  '$http', 'Api', '$timeout', 'Constants', 
    function ($scope, $state, $http, Api, $timeout, Constants) {
        $scope.currentStepInstruction = 'Print and apply barcodes';
        $scope.setHighlightedPlate(null, null, true, true);
        jQuery('input:focus').trigger('blur');

        $scope.setTubeBarcodesFileDownloaded = function (val) {

            var columnTitles = [
                'COI'
                ,'itemName'
                ,'partNumber'
                ,'labelMass'
            ]

            var csvContents = columnTitles.join(',') + '\n';

            var shippingTubeBarcodeData = $scope.transformSpec.details.shippingTubeBarcodeData;

            for(var i = 0; i < shippingTubeBarcodeData.length; i++) {
                row = shippingTubeBarcodeData[i];
                var line = '';
                for (var j=0; j<columnTitles.length; j++) {
                    line += (j ? ',' : '') + row[columnTitles[j]]
                }
                csvContents += line + '\n';
            }

            var csvBlob = new Blob([csvContents], {type: "text/csv"});

            saveAs(csvBlob, "tube_barcodes.csv");

            $scope.tubeBarcodesFileDownloaded = val;
        }

        $scope.tubesLabeled = function () {
            if ($scope.tubeBarcodesFileDownloaded) {
                $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.destination_tubes_scan');
            }
        }
    }]
)

.controller('hamiltonWizardDestinationTubesScanController', ['$scope', '$state',  '$http', 'Api', '$timeout', 'Constants', 
    function ($scope, $state, $http, Api, $timeout, Constants) {
        $scope.setTubeDestinationsMode(true);

        $scope.promptForDestinationTubeScan();

        $scope.setActiveDeckRegion($scope.hamiltonDataObj.allDestinationPlates[0].carrier.selectedHamiltonDeckRegion);

        $scope.restartDestinationPlateScan = function () {
            for (var i=0; i<$scope.hamiltonDataObj.allDestinationPlates.length;i++) {
                var plate = $scope.hamiltonDataObj.allDestinationPlates[i];
                plate.barcode = null;
            }
            $scope.setScannedTubeCount(0);
            $scope.promptForDestinationTubeScan();
        };

        $scope.tubePlacementComplete = function () {
            /* TODO save transform spec show worklist download link */
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
                });;
            }
            
        };

        $scope.$on('$destroy', function () {
            $scope.setTubeDestinationsMode(false);
        });
    }]
)

.controller('hamiltonWizardFinishRunController', ['$scope', '$state', '$stateParams', 'Api', '$timeout',  
    function ($scope, $state, $stateParams, Api, $timeout) {

        $scope.savedSpecIdToFinish = $stateParams.saved_spec_id;
        $scope.currentStepInstruction = 'Click "Run Finished" once the Hamilton run is complete.';

        $scope.getPrettySpecDate = function (dateString) {
            var date = new Date(dateString);
            return date.toLocaleString();
        }
        $scope.runFinished = function () {
            if (!$scope.finishiningRun) {
                $scope.finishiningRun = true;
                Api.executeTransformSpec($scope.savedSpecIdToFinish).success(function (data) {
                    $scope.finishiningRun = false;
                    $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.run_complete', {
                        saved_spec_id: $scope.savedSpecIdToFinish
                    });
                }).error(function (error) {
                    $scope.finishiningRun = false;
                    $scope.clearScannedItemErrorMessage();
                    $scope.showScannedItemErrorMessage('This Hamilton run could not be finished. Please try again.');
                });
            }
        };

        Api.getTransformSpec($scope.savedSpecIdToFinish).success(function (data) {
            $scope.clearScannedItemErrorMessage();
            $scope.savedSpecToFinish = data.data;
        }).error(function (data) {
            $scope.savedSpecToFinish = null;
        });
        $scope.showFinishRun();
    }]
)

.controller('hamiltonWizardRunCompleteController', ['$scope', '$state', '$stateParams', 'Api', '$timeout',  
    function ($scope, $state, $stateParams, Api, $timeout) {
        /* TO DO:  retrieve saved spec so's we know what to mark as executed */
        $scope.savedSpecId = $stateParams.saved_spec_id;
        $scope.currentStepInstruction = 'Trash any bad wells or plates now.';
        $scope.showFinishRun();

        $scope.hamiltonDone = function () {
            $scope.clearForm();
        };

        $scope.trashSamples = function (transformSpecId) {
            $state.go('root.trash_samples.by_transform_spec', {
                spec_id: transformSpecId
            });
        }

    }]
)

.controller('editBarcodeController', ['$scope', '$state',  '$http', 'Api', '$timeout', 'TypeAhead', 
    function ($scope, $state, $http, Api, $timeout, TypeAhead) {
        
        $scope.getTypeAheadPlateIds = TypeAhead.getTypeAheadPlateIds;

        $scope.plateInfoEntered = function () {
            if ($scope.plateId && $scope.plateId.length > 1) {
                $state.go('root.edit_barcode.plate_selected', {
                    selected_plate_id: $scope.plateId
                });
            }
        };

        $scope.getPlateInfo = function (plateId) {
            $scope.plateId = plateId;
            $scope.fetchingPlateForBarcodeEdit = true;
            Api.getPlateInfo($scope.plateId).then(function (resp) {
                $scope.fetchingPlateForBarcodeEdit = false;
                $scope.selectedPlate = resp.data;
                $scope.currentBarcode = $scope.selectedPlate.externalBarcode + '';
            });
        }

        $scope.plateInfoKeypress = function ($event) {
            if ($event.keyCode == 13) {
                $scope.plateInfoEntered();
            }
        };

        $scope.updateBarcode = function () {
            if ($scope.currentBarcode != $scope.selectedPlate.externalBarcode && $scope.selectedPlate.externalBarcode && $scope.selectedPlate.externalBarcode.length > 5) {

                $scope.updatingBarcode = true;

                Api.updateBarcode($scope.selectedPlate.sample_plate_id, $scope.selectedPlate.externalBarcode).success(function (data) {
                    if (data.success) {
                        $scope.updatingBarcode = false;
                        $scope.submissionResultMessage = 'The barcode for plate <span class="twst-step-text">' + $scope.selectedPlate.sample_plate_id + '</span> has been updated to <span class="twst-step-text">' + $scope.selectedPlate.externalBarcode + '</span>.';
                        $scope.submissionResultVisible = 1;
                        $scope.clearForm();
                    } else {
                        $scope.submissionResultMessage = 'Error: ' + data.errorMessage + '.';
                        $scope.submissionResultVisible = -1;
                        $scope.updatingBarcode = false;
                    }

                    $timeout(function () {
                        $scope.submissionResultVisible = 0;
                        $timeout(function () {
                            $scope.submissionResultMessage = null;
                        }, 400);
                    }, 5000);
                });
            }
        }

        $scope.barcodeChanged = function () {
            if (!$scope.selectedPlate) {
                return false
            } else {
                return $scope.currentBarcode != $scope.selectedPlate.externalBarcode && $scope.selectedPlate.externalBarcode && $scope.selectedPlate.externalBarcode.length > 5;
            }
        }

        $scope.clearForm = function () {
            $scope.plateId = null;
            $scope.selectedPlate = null;
            $scope.currentBarcode = null;
            $state.go('root.edit_barcode');
        }
    }]
)

.controller('editBarcodePlateSelectedController', ['$scope', '$state',  '$stateParams',
    function ($scope, $state, $stateParams) {
        var plateId = $stateParams.selected_plate_id;
        $scope.getPlateInfo(plateId);
    }]
)

.controller('viewStepsController', ['$scope', '$state', 'Api',
    function ($scope, $state, Api) {
        /* populate the sample types pulldown */
        $scope.fetchingSteps = true;
        Api.getPlateSteps().success(function (data) {
            $scope.fetchingSteps = false;
            $scope.plateSteps = data;
        });

    }]
)

.controller('plateDetailsController', ['$scope', '$state', 'Api', 'TypeAhead', 
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
)

.controller('plateDetailsBarcodeEnteredController', ['$scope', '$state', '$stateParams', 
    function ($scope, $state, $stateParams) {
        var barcode = decodeURIComponent($stateParams.entered_barcode);
        $scope.getPlateDetails(barcode);
    }]
)

.controller('sampleDetailsController', ['$scope', '$state', 'Api',  
    function ($scope, $state, Api) {
        
    }]
)

.controller('sampleDetailsSampleIdEnteredController', ['$scope', '$state', '$stateParams', 
    function ($scope, $state, $stateParams) {
        
    }]
)

.controller('transformSpecsController', ['$scope', '$state', '$stateParams', 
    function ($scope, $state, $stateParams) {

        $scope.view_manage = 'view_manage';
        $scope.edit = 'edit';

        $scope.selectPlanTab = function (which) {
            if ($scope.isEditing) {
                alert('Editing!');
            } else {
                $scope.selectedPlanTab = which;
                $state.go('root.transform_specs.' + which);
            }
        };

        $scope.setSelectedPlanTab = function (which) {
            $scope.selectedPlanTab = which;
        }

        $scope.newTransformSpec = function () {
            $state.go('root.transform_specs.edit.new');
        }

        $scope.editTransformSpec = function (spec) {
            $state.go('root.transform_specs.edit.spec', {
                spec_id: spec.id
            });
        }

        $scope.editing = function () {
            $scope.isEditing = true;
        }

        $scope.cancelEdit = function () {
            $scope.isEditing = false;
        }

        if ($state.current.name.indexOf('root.transform_specs') == -1) {
            $state.go('root.transform_specs.view_manage');   
        }
    }]
)

.controller('viewManageTransformSpecsController', ['$scope', '$state', '$stateParams', 'Api', '$modal', '$timeout', 'Formatter', 
    function ($scope, $state, $stateParams, Api, $modal, $timeout, Formatter) {

        $scope.transformSpecs = [];
        $scope.selectedSpec = null;

        var announceSuccess = function (spec, action) {
            $scope.specActionResultMessage = 'Spec <strong>' + spec.spec_id + '</strong> was successfully  ' + action + 'd.' ;
            $scope.specActionResultVisible = 1;

            $timeout(function () {
                $scope.specActionResultVisible = 0;
                $timeout(function () {
                    $scope.specActionResultMessage = null;
                }, 400);
            }, 5000);
        };

        var announceError = function (spec, action) {
            $scope.specActionResultMessage = 'An error occured while trying to ' + action + ' spec <strong>' + spec.spec_id + '</strong>.' ;
            $scope.specActionResultVisible = -1;

            $timeout(function () {
                $scope.specActionResultVisible = 0;
                $timeout(function () {
                    $scope.specActionResultMessage = null;
                }, 400);
            }, 5000);
        };

        $scope.deleteSpec = function (spec) {

            var deleteConfirmModal = $modal.open({
                templateUrl: 'twist-confirm-spec-delete-modal.html'
                ,size: 'md'
                ,controller: ['$scope', '$modalInstance', 'spec',  
                    function($scope, $modalInstance, spec) {

                        $scope.spec = spec;

                        $scope.clickCancel = function() {
                            $modalInstance.dismiss();
                        }
                        $scope.clickDelete = function() {

                            spec.updating = true;
                            Api.deleteTransformSpec(spec.spec_id).success(function (data) {
                                loadSpecs();
                                $modalInstance.close();
                                announceSuccess(spec, 'delete');
                            }).error(function () {
                                spec.updating = false;
                                $modalInstance.close();
                                announceError(spec, 'delete'); 
                            });
                        }
                    }
                ]
                ,resolve: {
                    spec: function() {
                        return spec;
                    }
                }
            });

        };

        $scope.executeSpec = function (spec) {

            var deleteConfirmModal = $modal.open({
                templateUrl: 'twist-confirm-spec-execute-modal.html'
                ,size: 'md'
                ,controller: ['$scope', '$modalInstance', 'spec',  
                    function($scope, $modalInstance, spec) {

                        $scope.spec = spec;

                        $scope.clickCancel = function() {
                            $modalInstance.dismiss();
                        }
                        $scope.clickExecute = function() {

                            spec.updating = true;
                            Api.executeTransformSpec(spec.spec_id).success(function (data) {
                                loadSpecs();
                                $modalInstance.close();
                                announceSuccess(spec, 'execute');
                            }).error(function () {
                                spec.updating = false;
                                $modalInstance.close();
                                announceError(spec, 'execute'); 
                            });
                        }
                    }
                ]
                ,resolve: {
                    spec: function() {
                        return spec;
                    }
                }
            });

        };

        $scope.viewSpec = function (spec) {
            $scope.selectedSpec = spec;
            $state.go('root.transform_specs.view_manage.view_spec', {
                spec_id: spec.spec_id
            });
        }

        $scope.getPrettyDateString = Formatter.getPrettyDateString;

        var loadSpecs = function () {
            $scope.fetchingSpecs = true;
            Api.getTransformSpecs().success(function (data) {
                $scope.fetchingSpecs = false;
                
                var specs = [];

                var theData = data.data;

                for (var i=0; i<theData.length;i++) {

                    var thisSpec = theData[i];
                    if (thisSpec.data_json.operations) {
                        thisSpec.plan = thisSpec.data_json;
                    } else {
                        thisSpec.plan = JSON.parse(thisSpec.data_json);
                    }
                    
                    specs.push(thisSpec);
                }

                $scope.transformSpecs = specs;
                $scope.fetchingSpecs = false;

            });
        };


        var init = function () {
            $scope.setSelectedPlanTab($scope.view_manage);
            $scope.fetchingSpecs = true;
            loadSpecs();
        }

        init();
    }]
)

.controller('transformSpecViewSpecController', ['$scope', '$state', '$stateParams', 'TransformBuilder', 'Api', 'Formatter', '$location', 
    function ($scope, $state, $stateParams, TransformBuilder, Api, Formatter, $location) {

        $scope.backToSpecList = function () {
            $state.go('root.transform_specs.view_manage');
        }

        $scope.continueHamilton = function () {
            $location.path('/record-transform/' + $scope.selectedSpec.plan.details.transfer_type_id + '-' + Formatter.lowerCaseAndSpaceToDash($scope.selectedSpec.plan.title) + '/hamilton_operation/' + $scope.selectedSpec.plan.details.hamilton.barcode.toLowerCase() + '-' + Formatter.lowerCaseAndSpaceToDash(Formatter.dashToSpace($scope.selectedSpec.plan.details.hamilton.label)) + '/finish-run/' + $scope.selectedSpec.spec_id)
        };

        $scope.trashSamples = function (spec_id) {
            $state.go('root.trash_samples.by_transform_spec', {
                spec_id: spec_id
            });
        }

        var specId = $stateParams.spec_id;
        if (!$scope.selectedSpec) {
            $scope.specLoading = true;
            Api.getTransformSpec(specId).success(function (data) {
                $scope.specLoading = false;
                var thisSpec = data.data;
                thisSpec.plan = thisSpec.data_json;
                $scope.selectedSpec = thisSpec;
            });
        } else {
            console.log($scope.selectedSpec);
        }
    }]
)

.controller('editTransformSpecsController', ['$scope', '$state', '$stateParams', 
    function ($scope, $state, $stateParams) {
        $scope.transformSpec = null;
        $scope.setSelectedPlanTab($scope.edit);
    }]
)

.controller('transformSpecEditorController', ['$scope', '$state', '$stateParams', 'TransformBuilder', 'Api', 
    function ($scope, $state, $stateParams, TransformBuilder, Api) {
        
        var specId = $stateParams.spec_id;

        $scope.specLoading = true;

        $scope.selectedSpecText = "Select a Transform Type";

        $scope.specTypes = [
            { text: 'Rebatching for Transformation', id: 'SPEC_01'}
        ];

        $scope.selectSpecType = function (option) {
            $scope.selectedSpecText = option.text;

        }

        if (specId) {
            Api.getTransformSpec(specId).success(function (data) {
                $scope.transformSpec = JSON.parse(data.plan);
                $scope.transformSpec.id = specId;
                $scope.specLoading = false;
                console.log($scope.transformSpec);
            });
        } else {
            var plan = TransformBuilder.newTransformSpec();
            plan.setCreateEditDefaults();
            $scope.transformSpec = plan;
            $scope.specLoading = false;
            $scope.editing();
            console.log($scope.transformSpec);
        }
    }]
)

.controller('trashSamplesController', ['$scope', '$state', '$stateParams', 'TypeAhead', '$timeout',  
    function ($scope, $state, $stateParams, TypeAhead, $timeout) {
        $scope.getTransformSpecIds = TypeAhead.getTransformSpecIds;

        $scope.transformSpec = {};

        $scope.transformIdSelected = function () {
            $state.go('root.trash_samples.by_transform_spec', {
                spec_id: $scope.transformSpec.id
            });
        }
    }]
)

.controller('trashSamplesByTransformSpecController', ['$scope', '$state', '$stateParams', 'Api', 
    function ($scope, $state, $stateParams, Api) {
        $scope.spec_id = $stateParams.spec_id;

        $scope.openTrashPlateEditor = function (plateBarcode) {
            $scope.setPlateBarcodeForEdit(plateBarcode);
            $state.go('root.trash_samples.by_transform_spec.for_plate', {
                plate_barcode: plateBarcode
            });
        }

        $scope.setPlateBarcodeForEdit = function (plateBarcode) {
            $scope.plateBarcodeForEdit = plateBarcode;
        };

        $scope.backToSpec = function () {
            $state.go('root.trash_samples.by_transform_spec', {
                spec_id: $scope.spec_id
            });
        };

        $scope.specLoading = true;
        Api.getTransformSpec($scope.spec_id).success(function (data) {
            $scope.specLoading = false;
            var thisSpec = data.data;
            thisSpec.plan = thisSpec.data_json;
            $scope.selectedSpec = thisSpec;
            $scope.executedDateString = (new Date($scope.selectedSpec.date_executed)).toLocaleString();
            console.log($scope.selectedSpec);
        }).error(function () {
            console.log('Error loading spec.');
        });
    }]
)

.controller('trashSamplesByTransformSpecPlateController', ['$scope', '$state', '$stateParams', 'Api', 'Maps', 
    function ($scope, $state, $stateParams, Api, Maps) {
        $scope.plate_barcode = $stateParams.plate_barcode;
        $scope.setPlateBarcodeForEdit($scope.plate_barcode);
        
        $scope.selectedWellCount = 0;
        $scope.plateWellClicked = function (well) {
            if (well.highlighted) {
                $scope.selectedWellCount++;
            } else {
                $scope.selectedWellCount--;
            }  
        };

        $scope.toggleSelectAll = function (forceNone) {
            if (forceNone || $scope.selectedWellCount == $scope.plate.wells.length) {
                //unselect all
                for (well in $scope.plate.wellMap) {
                    var well = $scope.plate.wellMap[well];
                    if (well.sampleId) {
                        well.highlighted = false;
                    }
                }
                $scope.selectedWellCount = 0;
            } else {
                //select all
                for (well in $scope.plate.wellMap) {
                    var well = $scope.plate.wellMap[well];
                    if (well.sampleId) {
                        well.highlighted = true;
                        $scope.plateWellClicked(well);
                    }
                }
                $scope.selectedWellCount = $scope.plate.wells.length;
            }
        };

        $scope.clearTrashSamplesErrorMessage = function () {
            $scope.trashSamplesErrorMessage = null;
            $scope.trashSamplesErrorMessageVisible = 0;  
        }

        $scope.trashSelectedWells = function () {
            if ($scope.selectedWellCount && !$scope.trashingWells) {
                var trashIds = [];
                var trashedWells = [];

                for (well in $scope.plate.wellMap) {
                    var well = $scope.plate.wellMap[well];
                    if (well.highlighted) {
                        trashIds.push(well.sampleId);
                        trashedWells.push(well);
                    }
                }

                $scope.trashingWells = true;
                Api.trashSamples(trashIds).success(function (data) {
                    $scope.trashingWells = false;
                    $scope.toggleSelectAll(true);

                    $scope.trashSamplesErrorMessage = 'The selected samples have been trashed.';
                    $scope.trashSamplesErrorMessageVisible = 1;

                    for (var i=0; i<trashedWells.length;i++) {
                        trashedWells[i].trashed = true;
                    }
                }).error(function (data) {
                    $scope.trashingWells = false;
                    $scope.trashSamplesErrorMessage = 'Error trashing samples. Please try again.';
                    $scope.trashSamplesErrorMessageVisible = 11;
                });

                console.log(trashIds);
            }
        };

        $scope.loadingPlate = true;
        Api.getBasicPlateDetails($scope.plate_barcode).success(function (data) {
            $scope.loadingPlate = false;
            var thisPlate = new Maps.plateTemplates[data.plateDetails.type]();
            delete thisPlate.description;
            thisPlate.filledWellCount = data.wells.length;
            $.extend(thisPlate, data);

            for (var i=0; i< data.wells.length; i++) {
                var well = data.wells[i];
                thisPlate.addSampleId(well.column_and_row, well.sample_id);
            }
            thisPlate.plateDetails['barcode'] = $scope.plate_barcode;
            $scope.plate = thisPlate;
            console.log($scope.plate);
        }).error(function () {
            console.log('Error loading plate details.');
        });

        $scope.$on('$destroy', function () {
            $scope.setPlateBarcodeForEdit(null);
        });
    }]
)

.run(['$state', 'User', '$location', '$timeout', 'localStorageService', 
    function($state, User, $location, $timeout, localStorageService) {
        var authChecked = false;

        var setHashUrl = function () {
            var url = document.location.href;
            var hashUrl = url.substring(url.indexOf('#') + 1);
            if (url != hashUrl) {
                localStorageService.set('loginTarget', hashUrl);
            }
        }

        User.init().success(function (data) {
            if (data.user) {
                authChecked = true;
                /* authorized! */
                var loginTarget = localStorageService.get('loginTarget');
                if (loginTarget == null || loginTarget == '/login') {
                    setHashUrl();
                }
                var loginTarget = localStorageService.get('loginTarget');
                if (!loginTarget || loginTarget == '/login') {
                    loginTarget = '/record-transform';
                }
                $location.path(loginTarget);
            } else {
                setHashUrl();
                $state.go('root.login');
            }
        });

    }]
)

.config(['$httpProvider', 'localStorageServiceProvider', 
    function($httpProvider, localStorageServiceProvider) {
        if (!$httpProvider.defaults.headers.get) {
            $httpProvider.defaults.headers.get = {};
        }
        //disable IE ajax request caching
        $httpProvider.defaults.headers.get['If-Modified-Since'] = 'Mon, 26 Jul 1997 05:00:00 GMT';
        // extra
        $httpProvider.defaults.headers.get['Cache-Control'] = 'no-cache';
        $httpProvider.defaults.headers.get['Pragma'] = 'no-cache';

        localStorageServiceProvider.setPrefix('twistBio').setStorageType('sessionStorage');
    }]
)

.config(['$stateProvider',
    function($stateProvider) {
        return $stateProvider.state('root', {
            url: '/'
            ,templateUrl: 'twist-base.html'
            ,controller: 'rootController'
        }).state('root.login', {
            url: 'login'
            ,templateUrl: 'twist-login.html'
            ,controller: 'loginController'
        }).state('root.record_transform', {
            url: 'record-transform'
            ,templateUrl: 'twist-record-transform.html'
            ,controller: 'trackStepController'
        }).state('root.record_transform.step_type_selected', {
            url: '/:selected_step_type_id'
            ,templateUrl: 'twist-record-transform-type-selected.html'
            ,controller: 'stepTypeSelectedController'
        }).state('root.record_transform.step_type_selected.tab_selected', {
            url: '/:selected_tab'
            ,templateUrl: 'twist-record-transform-tab-selected.html'
            ,controller: 'tabSelectedController'
        })
        /*.state('root.record_transform.step_type_selected.file_upload', {
            url: '/custom-file-upload'
            ,views: {
                "transformTypePlaceholderView@root.record_transform.step_type_selected": {
                    template: ''
                    ,controller: 'customExcelUploadController'
                }
            }
        }).state('root.record_transform.step_type_selected.standard_template', {
            url: '/standard-template'
            ,views: {
                "transformTypePlaceholderView@root.record_transform.step_type_selected": {
                    template: ''
                    ,controller: 'standardTemplateController'
                }
            }
        }).state('root.record_transform.step_type_selected.hamilton_operation', {
            url: '/hamilton-wizard'
            ,views: {
                "transformTypePlaceholderView@root.record_transform.step_type_selected": {
                    template: ''
                    ,controller: 'hamiltonOperationController'
                }
            }
        })*/
        .state('root.record_transform.step_type_selected.tab_selected.hamilton_select', {
            url: '/select'
            ,views: {
                "hamiltonWizard@root.record_transform.step_type_selected.tab_selected": {
                    templateUrl: 'twist-hamilton-select.html'
                    ,controller: 'hamiltonSelectController'
                }
            }
        }).state('root.record_transform.step_type_selected.tab_selected.hamilton_wizard', {
            url: '/:hamilton_info'
            ,views: {
                "hamiltonWizard@root.record_transform.step_type_selected.tab_selected": {
                    templateUrl: 'twist-hamilton-wizard.html'
                    ,controller: 'hamiltonWizardController'
                }
            }
        }).state('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.carrier_scan', {
            url: '/carrier-scan'
            ,views: {
                "hamiltonStep@root.record_transform.step_type_selected.tab_selected.hamilton_wizard": {
                    templateUrl: 'twist-hamilton-step-carrier-scan.html'
                    ,controller: 'hamiltonWizardCarrierScanController'
                }
            }
        }).state('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.source_scan', {
            url: '/source-scan'
            ,views: {
                "hamiltonStep@root.record_transform.step_type_selected.tab_selected.hamilton_wizard": {
                    templateUrl: 'twist-hamilton-step-source-scan.html'
                    ,controller: 'hamiltonWizardSourceScanController'
                }
            }
        }).state('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.destination_scan', {
            url: '/destination-scan'
            ,views: {
                "hamiltonStep@root.record_transform.step_type_selected.tab_selected.hamilton_wizard": {
                    templateUrl: 'twist-hamilton-step-destination-scan.html'
                    ,controller: 'hamiltonWizardDestinationScanController'
                }
            }
        }).state('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.label_destination_tubes', {
            url: '/label-destination-tubes'
            ,views: {
                "hamiltonStep@root.record_transform.step_type_selected.tab_selected.hamilton_wizard": {
                    templateUrl: 'twist-hamilton-step-label-destination-tubes.html'
                    ,controller: 'hamiltonWizardLabelDestinationTubesController'
                }
            }
        }).state('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.destination_tubes_scan', {
            url: '/destination-tubes-scan'
            ,views: {
                "hamiltonStep@root.record_transform.step_type_selected.tab_selected.hamilton_wizard": {
                    templateUrl: 'twist-hamilton-step-destination-tubes-scan.html'
                    ,controller: 'hamiltonWizardDestinationTubesScanController'
                }
            }
        }).state('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.finish_run', {
            url: '/finish-run/:saved_spec_id'
            ,views: {
                "hamiltonFinish@root.record_transform.step_type_selected.tab_selected.hamilton_wizard": {
                    templateUrl: 'twist-hamilton-step-finish-run.html'
                    ,controller: 'hamiltonWizardFinishRunController'
                }
            }
        }).state('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.run_complete', {
            url: '/run-complete/:saved_spec_id'
            ,views: {
                "hamiltonFinish@root.record_transform.step_type_selected.tab_selected.hamilton_wizard": {
                    templateUrl: 'twist-hamilton-step-run-complete.html'
                    ,controller: 'hamiltonWizardRunCompleteController'
                }
            }
        }).state('root.edit_barcode', { 
            url: 'edit-barcode'
            ,templateUrl: 'twist-edit-barcode.html'
            ,controller: 'editBarcodeController'
        }).state('root.edit_barcode.plate_selected', {
            url: '/:selected_plate_id'
            ,template: ''
            ,controller: 'editBarcodePlateSelectedController'
        }).state('root.view_steps', {
            url: 'view-steps'
            ,templateUrl: 'twist-view-steps.html'
            ,controller: 'viewStepsController'
        }).state('root.plate_details', {
            url: 'plate-details'
            ,templateUrl: 'twist-plate-details.html'
            ,controller: 'plateDetailsController'
        }).state('root.plate_details.barcode_entered', {
            url: '/:entered_barcode'
            ,template: ''
            ,controller: 'plateDetailsBarcodeEnteredController'
        }).state('root.sample_details', {
            url: 'sample-details'
            ,templateUrl: 'twist-sample-details.html'
            ,controller: 'sampleDetailsController'
        }).state('root.sample_details.sample_id_entered', {
            url: '/:entered_sample_id'
            ,template: ''
            ,controller: 'sampleDetailsSampleIdEnteredController'
        }).state('root.transform_specs', {
            url: 'transform-specs'
            ,templateUrl: 'twist-transform-specs.html'
            ,controller: 'transformSpecsController'
        }).state('root.transform_specs.view_manage', {
            url: '/view-manage'
            ,templateUrl: 'twist-view-manage-transform-specs.html'
            ,controller: 'viewManageTransformSpecsController'
        }).state('root.transform_specs.view_manage.view_spec', {
            url: '/spec/:spec_id'
            ,templateUrl: 'twist-transform-specs-view-spec.html'
            ,controller: 'transformSpecViewSpecController'
        }).state('root.transform_specs.edit', {
            url: '/edit'
            ,templateUrl: 'twist-edit-transform-specs.html'
            ,controller: 'editTransformSpecsController'
        }).state('root.transform_specs.edit.new', {
            url: '/new'
            ,templateUrl: 'twist-transform-specs-editor.html'
            ,controller: 'transformSpecEditorController'
        }).state('root.transform_specs.edit.spec', {
            url: '/spec/:spec_id'
            ,templateUrl: 'twist-transform-specs-editor.html'
            ,controller: 'transformSpecEditorController'
        }).state('root.trash_samples', {
            url: 'trash-samples'
            ,templateUrl: 'twist-trash-samples.html'
            ,controller: 'trashSamplesController'
        }).state('root.trash_samples.by_transform_spec', {
            url: '/transform-spec/:spec_id'
            ,templateUrl: 'twist-trash-samples-by-transform-spec.html'
            ,controller: 'trashSamplesByTransformSpecController'
        }).state('root.trash_samples.by_transform_spec.for_plate', {
            url: '/plate/:plate_barcode'
            ,templateUrl: 'twist-trash-samples-by-transform-spec-plate.html'
            ,controller: 'trashSamplesByTransformSpecPlateController'
        })
        ;
    }
])

;
