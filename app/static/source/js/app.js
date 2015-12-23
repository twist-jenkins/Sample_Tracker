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

        $scope.clearForm = function () {
            $scope.stepTypeDropdownValue = Constants.STEP_TYPE_DROPDOWN_LABEL;
            $scope.transformSpec = TransformBuilder.newTransformSpec();
            $scope.transformSpec.setPlateStepDefaults();
            $scope.templateTypeSelection = null;
            $state.go('root.record_transform');
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

        $scope.selectTransferTemplateType = function (which) {
            if (which == Constants.HAMILTON_OPERATION && !$scope.isHamiltonStep()) {
                return false;
            } else if (which != Constants.HAMILTON_OPERATION && $scope.isHamiltonStep()) {
                return false;
            } 
            $state.go('root.record_transform.step_type_selected.tab_selected', {
                selected_tab: which
            });
        };

        $scope.setTransferTemplate = function (which) {
            $scope.templateTypeSelection = which;
        };

        $scope.isHamiltonStep = function () {
            if (selectedTranferTypeId == 39 || selectedTranferTypeId == 48) {
                return true; 
            }
            return false;
        }

        var selectedTranferTypeId;
        $scope.initTransferTypes.success(function (data) {
            selectedTranferTypeId = $stateParams.selected_step_type_id.split('-')[0];
            $scope.setSelectedOption(selectedTranferTypeId);
        });
    }]
)

.controller('tabSelectedController', ['$scope', '$state', '$element', '$sce', '$timeout', 'Formatter', 'TypeAhead', 'Maps', 'Constants', 'TransformBuilder', 'FileParser', 
    function ($scope, $state, $element, $sce, $timeout, Formatter, TypeAhead, Maps, Constants, TransformBuilder, FileParser) {

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

    }]
)

.controller('hamiltonSelectController', ['$scope', '$state', '$stateParams', 'Constants', 'Maps', 'Formatter', '$timeout', 'Api', 
    function ($scope, $state, $stateParams, Constants, Maps, Formatter, $timeout, Api) {
        $scope.hamiltonBarcodeChange = function () {
            $timeout.cancel($scope.hamiltonBarcodeChangeTimeout);
            var barcode = $scope.hamiltonBarcode.trim();
            if (barcode != '' && barcode.length > 4) {
                $scope.hamiltonBarcodeChangeTimeout = $timeout(function () {
                    var apiCall = Api.getHamiltonByBarcode(barcode).success(function (data) {
                        $scope.loadingHamilton = false;
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
            $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_wizard', {
                hamilton_info: hamilton.barcode.toLowerCase() + '-' + Formatter.lowerCaseAndSpaceToDash(Formatter.dashToSpace(hamilton.label))
            }, {notify: false});
            $scope.hamiltonDataObj = {
                deckRegions: angular.copy($scope.transformSpec.map.hamiltonDetails[$scope.selectedHamilton.barcode])
            };
            $scope.decorateHamiltonDataObj($scope.hamiltonDataObj);
            $timeout(function () {
                $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.carrier_scan');
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

        /* this function adds ordered arrays that reference the carriers and plates in their position in the deckRegions
         * We'll use the ordered arrays for the guidance when scanning barcodes for carrier, carrier position & plate.
         * By looping through these arrays, we're actually moving through the deckRegions object's carriers and plates that back the UI
         */
        $scope.decorateHamiltonDataObj = function (hamObj) {
            hamObj.allCarriers = [];
            hamObj.allSourcePlates = [];
            hamObj.allDestinationPlates = [];
            for (region in hamObj.deckRegions) {
                var theseCarriers = hamObj.deckRegions[region].carriers;
                for (var i=0; i<theseCarriers.length;i++) {
                    hamObj.allCarriers.push(theseCarriers[i]);
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
        $scope.setHighlightedPlate = function (plate, which) {
            if (!which) {
                which = Constants.HAMILTON_ELEMENT_PLATE;
            }
            $scope.highlightedPlate = plate;
            $scope.setCurrentStepInstruction(which, plate);
            $timeout(function () {
                jQuery('.twst-hamilton-wizard-plate-' + plate.dataIndex + ' .twst-hamilton-wizard-plate-input').focus();
            }, 0);
        }
        $scope.scannedCarrierCount = 0;
        $scope.findNextCarrierForScan = function () {
            var firstFound = false;
            var scannedCarrierCount = 0;
            for (var i=0; i<$scope.hamiltonDataObj.allCarriers.length;i++) {
                var carrier = $scope.hamiltonDataObj.allCarriers[i];
                if (!carrier.barcode && !firstFound) {
                    $scope.setHighlightedCarrier(carrier);
                    carrier.nextToScan = true;
                    firstFound = true;
                } else {
                    carrier.nextToScan = false;
                    if (carrier.barcode) {
                        scannedCarrierCount++;
                    }
                }
            }
            $scope.scannedCarrierCount = scannedCarrierCount;
            
            if ($scope.scannedCarrierCount == $scope.hamiltonDataObj.allCarriers.length) {
                $scope.highlightedCarrier = null;
                $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.source_scan');
            }
        };
        $scope.scannedCarrierBarcode;
        var barcodeFinishedTimeout = null;
        $scope.carrierBarcodeScanned = function () {
            if ($scope.highlightedCarrier.barcode && $scope.highlightedCarrier.barcode.length) {
                $timeout.cancel(barcodeFinishedTimeout);
                if ($scope.checkAlreadyScannedCarrier($scope.highlightedCarrier.barcode)) {
                    $scope.clearScannedItemErrorMessage();
                    $scope.scannedItemErrorMessage = 'The scanned barcode has already been scanned. Please scan the highlighted carrier.';
                    $scope.loadingCarrier = false;
                    $scope.highlightedCarrier.barcode = null;
                    $scope.scannedItemErrorMessageVisible = -1;
                } else {
                    barcodeFinishedTimeout = $timeout(function () {
                        $scope.loadingCarrier = true;
                        Api.getCarrierByBarcode($scope.highlightedCarrier.barcode, $scope.selectedHamilton.barcode).success(function (data) {
                            $scope.loadingCarrier = false;
                            $scope.clearScannedItemErrorMessage();
                            $scope.highlightedCarrier.positions = data.positions;
                            $scope.findNextCarrierForScan();
                        }).error(function (error) {
                            $scope.clearScannedItemErrorMessage();
                            $scope.scannedItemErrorMessage = 'The scanned barcode - <strong>' + $scope.highlightedCarrier.barcode + '</strong> - was not found. Please re-scan.';
                            $scope.loadingCarrier = false;
                            $scope.highlightedCarrier.barcode = null;
                            $scope.scannedItemErrorMessageVisible = -1;
                        });
                    }, 200);
                }   
            }
        };
        $scope.clearScannedItemErrorMessage = function () {
            $scope.scannedItemErrorMessage = null;
            $scope.scannedItemErrorMessageVisible = 0;  
        }
        $scope.scannedSourcePlateCount = 0;
        $scope.scannedDestinationPlateCount = 0;
        $scope.findNextPlateForScan = function (plateFor, positionOrPlate) {
            var firstFound = false;
            var scannedPlateCount = 0;
            var whichPlateArray = (plateFor == 'source' ? $scope.hamiltonDataObj.allSourcePlates : $scope.hamiltonDataObj.allDestinationPlates);
            for (var i=0; i<whichPlateArray.length;i++) {
                var plate = whichPlateArray[i];
                if (!plate.barcode && !firstFound && !plate.unused) {
                    $scope.setHighlightedPlate(plate, positionOrPlate);
                    plate.nextToScan = true;
                    firstFound = true;
                } else {
                    plate.nextToScan = false;
                    if (plate.barcode) {
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
                        $scope.scannedItemErrorMessage = 'This plate has already been scanned. Please scan the <strong>barcode</strong> for ' + $scope.highlightedPlate.plateFor + ' plate ' + $scope.highlightedPlate.dataIndex;
                        $scope.highlightedPlate.barcode = null;
                        $scope.scannedItemErrorMessageVisible = -1;
                    } else {
                        barcodeFinishedTimeout = $timeout(function () {
                            $scope.confirmingPlate = true;
                            if ($scope.highlightedPlate.plateFor == Constants.PLATE_SOURCE) {
                                Api.confirmPlateReadyForTransform($scope.highlightedPlate.barcode, $scope.transformSpec.details.transfer_type_id).success(function (data) {
                                    $scope.confirmingPlate = false;
                                    $scope.clearScannedItemErrorMessage();
                                    $scope.findNextPlateForScan($scope.highlightedPlate.plateFor, Constants.HAMILTON_ELEMENT_CARRIER_POSITION);
                                }).error(function (error) {
                                    $scope.clearScannedItemErrorMessage();
                                    $scope.scannedItemErrorMessage = 'The plate barcode was not found. Please scan the <strong>barcode</strong> for ' + $scope.highlightedPlate.plateFor + ' plate ' + $scope.highlightedPlate.dataIndex;
                                    $scope.confirmingPlate = false;
                                    $scope.highlightedPlate.barcode = null;
                                    $scope.scannedItemErrorMessageVisible = -1;
                                });
                            } else if ($scope.highlightedPlate.plateFor == Constants.PLATE_DESTINATION) {
                                Api.checkDestinationPlatesAreNew([$scope.highlightedPlate.barcode]).success(function (data) {
                                    if (!data.success) {
                                        /* plate already exists - error */
                                        $scope.clearScannedItemErrorMessage();
                                        $scope.scannedItemErrorMessage = 'A plate already exists in the database with the scanned barcode.';
                                        $scope.confirmingPlate = false;
                                        $scope.highlightedPlate.barcode = null;
                                        $scope.scannedItemErrorMessageVisible = -1;
                                    } else {
                                        /* plate is new */
                                        $scope.confirmingPlate = false;
                                        $scope.clearScannedItemErrorMessage();
                                        $scope.findNextPlateForScan($scope.highlightedPlate.plateFor, Constants.HAMILTON_ELEMENT_CARRIER_POSITION);
                                    }
                                }).error(function (data) {
                                    $scope.clearScannedItemErrorMessage();
                                    $scope.scannedItemErrorMessage = 'An error occured in checking this barcode. Please re-scan.';
                                    $scope.confirmingPlate = false;
                                    $scope.highlightedPlate.barcode = null;
                                    $scope.scannedItemErrorMessageVisible = -1;
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
                                $scope.findNextPlateForScan($scope.highlightedPlate.plateFor, Constants.HAMILTON_ELEMENT_PLATE);
                            } else {
                                /* right carrier but prompt operator to scan correct position barcode */
                                delete $scope.highlightedPlate.positionScanned;

                                $scope.scannedItemErrorMessage = '<strong>Incorrect position scanned:</strong> Please scan carrier ' + $scope.highlightedPlate.carrier.index + ' position ' + $scope.highlightedPlate.localIndex;
                                $scope.scannedItemErrorMessageVisible = -1;

                                $scope.highlightedPlate.barcode = null;
                            }
                        } else {
                            /* scanned barcode is not a position on this carrier */
                            delete $scope.highlightedPlate.positionScanned;

                            $scope.scannedItemErrorMessage = '<strong>Invalid position barcode:</strong> Please scan carrier ' + $scope.highlightedPlate.carrier.index + ' position ' + $scope.highlightedPlate.localIndex;
                            $scope.scannedItemErrorMessageVisible = -1;

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
                $scope.findNextCarrierForScan();
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
                $scope.findNextPlateForScan(Constants.PLATE_SOURCE, Constants.HAMILTON_ELEMENT_CARRIER_POSITION);
            }
        };

        $scope.sourcePlateScanComplete = function () {
            if ($scope.scannedSourcePlateCount && !$scope.processingSources) {

                /* TODO: api call to submit source plates and get # of destination plates        */

                var scannedPlateBarcodes = [];

                for (var i=0; i<$scope.hamiltonDataObj.allSourcePlates.length;i++) {
                    var plate = $scope.hamiltonDataObj.allSourcePlates[i];
                    if (plate.barcode) {
                        scannedPlateBarcodes.push(plate.barcode);
                    }
                }

                $scope.processingSources = true;

                Api.processHamiltonSources(scannedPlateBarcodes, $scope.transformSpec.details.transfer_type_id).success(function (data) {
                    console.log(data);
                    $scope.processingSources = false;
                    var destinationPlateCount = data.required_destination_plate_count;

                    var newAllDestinationPlates = [];

                    for (var i=0; i<$scope.hamiltonDataObj.allDestinationPlates.length;i++) {
                        var plate = $scope.hamiltonDataObj.allDestinationPlates[i];
                        plate.optional = false;
                        if (plate.dataIndex > destinationPlateCount) {
                            plate.unused = true;
                        } else {
                            newAllDestinationPlates.push(plate);
                        }
                    }

                    $scope.hamiltonDataObj.allDestinationPlates = newAllDestinationPlates;

                    $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.destination_scan');
                }).error(function (error) {
                    $scope.processingSources = false;
                    $scope.clearScannedItemErrorMessage();
                    $scope.scannedItemErrorMessage = 'There was an error processing these sources. Please try again.';
                    $scope.scannedItemErrorMessageVisible = -1;
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
                $scope.findNextPlateForScan(Constants.PLATE_DESTINATION, Constants.HAMILTON_ELEMENT_CARRIER_POSITION);
            }
        };

        $scope.desinationPlateScanComplete = function () {
            
        };
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

.controller('transformSpecViewSpecController', ['$scope', '$state', '$stateParams', 'TransformBuilder', 'Api', 
    function ($scope, $state, $stateParams, TransformBuilder, Api) {

        $scope.backToSpecList = function () {
            $state.go('root.transform_specs.view_manage');
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
        })
        ;
    }
])

;
