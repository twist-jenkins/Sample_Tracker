var app;

app = angular.module('twist.app', ['ui.router', 'ui.bootstrap', 'ngSanitize', 'templates-main'])


.controller('rootController', ['$scope', '$state', 'User',
    function ($scope, $state, User) {
        $scope.user = User;
        $scope.current_year = (new Date).getFullYear();

        $scope.navTo = function (where) {
            $state.go(where);
        }

        $scope.$on('$stateChangeSuccess', function(event, toState) {
            $scope.currentNav = toState.name;
        });
    }]
)

.controller('loginController', ['$scope', '$state',  '$http',
    function ($scope, $state, $http) {

        $http({url: '/google-login'}).success(function (data) {
            $scope.googleLoginUrl = data.login_url;
        }).error(function () {
            $scope.loginPageError = true;
        });
    }]
)

.controller('trackStepController', ['$scope', '$state', 'Api', '$sce', '$timeout', 'Formatter', 'TypeAhead', 'Maps', 'Constants', 'TransferPlanner', 'FileParser', 
    function ($scope, $state, Api, $sce, $timeout, Formatter, TypeAhead, Maps, Constants, TransferPlanner, FileParser) {

        /* interface backing vars */
        var returnEmptyPlate = function () {
            return {text: '', title: ''};
        };

        $scope.stepTypeDropdownValue = Constants.STEP_TYPE_DROPDOWN_LABEL;

        $scope.transferPlan = TransferPlanner.newTransferPlan();
        $scope.getTypeAheadBarcodes = TypeAhead.getTypeAheadBarcodes;

        $scope.excel_template = 'excel_upload';
        $scope.standard_template = 'standard_template';

        $scope.excelFileStats = {};
        $scope.fileErrors = [];

        $scope.cachedFileData = null;

        $scope.selectStepType = function (option) {
            $scope.transferPlan.setTransferTypeDetails(option);

            var route = 'root.record_step.step_type_selected';

            if ($scope.transferPlan.map.type == Constants.USER_SPECIFIED_TRANSFER_TYPE) {
                $scope.templateTypeSelection = $scope.excel_template;
            } else {
                $scope.templateTypeSelection = $scope.standard_template;
            }

            route += '.' + $scope.templateTypeSelection;

            $state.go(route, {
                selected_step_type_id: option.id + '-' + Formatter.lowerCaseAndSpaceToDash(Formatter.stripNonAlphaNumeric(option.text, true, true).trim())
            });
        }

        $scope.setSelectedOption = function (optionId) {
            for (var i=0; i< $scope.stepTypeOptions.length;i++) {
                var option = $scope.stepTypeOptions[i];
                if (option.id == optionId) {
                    $scope.clearExcelUploadData();
                    $scope.submissionResultMessage = '';
                    $scope.submissionResultVisible = 0;
                    $scope.transferPlan.setTransferTypeDetails(option);
                    $scope.stepTypeDropdownValue = $scope.transferPlan.typeDetails.text;
                    if ($scope.cachedFileData) {
                        $scope.catchFile()
                    }
                    break;
                }
            }
        }

        /* refresh the current transfer plan based on changes to plates inputs or upload file */
        $scope.updateTransferPlan = function (val, which, itemIndex) {
            if (val.length > 5) {
                if (which == Constants.PLATE_SOURCE) {
                    $scope.transferPlan.addSourcePlate(itemIndex);
                } else if (which == Constants.PLATE_DESTINATION) {
                    $scope.transferPlan.addDestinationPlate(itemIndex);
                }
            }
        };

        $scope.sampleTrackFormReady = function () {

            if (!$scope.transferPlan.typeDetails) {
                return false;
            }

            if (!$scope.transferPlan.plateTransfers.length) {
                return false
            }

            return true;
        }

        $scope.clearForm = function () {
            $scope.stepTypeDropdownValue = Constants.STEP_TYPE_DROPDOWN_LABEL;
            $scope.transferPlan = TransferPlanner.newTransferPlan();
            $scope.clearExcelUploadData();
            $scope.templateTypeSelection = null;
            $scope.cachedFileData = null;
            $state.go('root.record_step');
        };

        $scope.selectTransferTemplateType = function (which) {
            var route = '';
            if (which == $scope.excel_template) {
                route = 'excel_upload';
                if ($scope.cachedFileData) {
                    $scope.transferPlan.setPlanFromFile(true);
                }
            } else if (which == $scope.standard_template) {
                route = 'standard_template';
                $scope.transferPlan.transferFromFile(false);
            } 
            $state.go('root.record_step.step_type_selected.' + route);
        };

        $scope.setTransferTemplate = function (which) {
            $scope.templateTypeSelection = which;
        };

        var getSampleTrackSubmitData = function () {
            var data = {
                sampleTransferTypeId: $scope.transferPlan.typeDetails.id
                ,sampleTransferTemplateId: $scope.transferPlan.typeDetails.transfer_template_id
            };

            data.transferMap = $scope.transferPlan.plateTransfers;

            return data;
        };

        $scope.submitStep = function () {

            var showError = function (data) {
                $scope.submissionResultMessage = 'Error: ' + data.errorMessage;
                $scope.submissionResultVisible = -1;
                $scope.submittingStep = false;
            }

            if (!$scope.submitting && $scope.sampleTrackFormReady() && !$scope.transferPlan.updating) {

                $scope.submittingStep = true;
                Api.submitSampleStep(getSampleTrackSubmitData()).success(function (data) {

                    if (data.success) {
                        $scope.submittingStep = false;
                        $scope.submissionResultMessage = 'This <span class="twst-step-text">' + $scope.transferPlan.typeDetails.text + '</span> step was successfully recorded.';
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
                });
            }
        };

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
                $scope.transferPlan.clearPlateTransfers();
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

                    FileParser.getTransferRowsFromFile(fileData, $scope.transferPlan).then(function (resultData) {
                        $scope.excelFileStats = resultData.stats;
                        $scope.fileErrors = resultData.errors;

                        if (!resultData.errors.length) {
                            $scope.transferPlan.transferFromFile(true, resultData.transferJSON);
                        } else {
                            $scope.transferPlan.clearPlateTransfers();
                        } 

                        $scope.parsingFile = false;

                    }, function (errorData) {
                        $scope.fileErrors = 'Error: Unknown error while parsing this file.';
                        $scope.parsingFile = false;
                    });
     
                }, 150);
            }
        };

        /* populate the sample types pulldown */
        Api.getSampleTransferTypes().success(function (data) {
            if (data.success) {
                $scope.stepTypeOptions = data.results;
            }
        });
    }]
)

.controller('stepTypeSelectedController', ['$scope', '$state',  '$stateParams',
    function ($scope, $state, $stateParams) {
        //inherits scope from trackStepController
        var selectedTranferTypeId = $stateParams.selected_step_type_id.split('-')[0];
        $scope.setSelectedOption(selectedTranferTypeId);
    }]
)

.controller('customExcelUploadController', ['$scope', '$state', '$stateParams', 
    function ($scope, $state, $stateParams) {
        //inherits scope from trackStepController via stepTypeSelectedController
        $scope.setTransferTemplate($scope.excel_template);
    }]
)

.controller('standardTemplateController', ['$scope', '$state', '$stateParams', 
    function ($scope, $state, $stateParams) {
        //inherits scope from trackStepController via stepTypeSelectedController
        $scope.setTransferTemplate($scope.standard_template);
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

            Api.getPlateDetails(barcode).success(function (data) {
                $scope.fetchingDetails = false;
                $scope.plateDetails = data;
                $scope.retrievedPlateBarcode = $scope.plateBarcode + '';
            });
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

.run(['$state', 'User', '$location', '$timeout',
    function($state, User, $location, $timeout) {
        var routeUrl = window.location.hash.substr(1);

        var authChecked = false;

        User.init().success(function (data) {
            if (data.user) {
                authChecked = true;
                /* authorized! */
                $location.path((routeUrl == '' || routeUrl == '/' || routeUrl == '/login') ? '/track-step' : routeUrl);
            }
        });

        //redirect un-auth'd users to login but give the login check above a moment to engage
        $timeout(function () {
            if (!authChecked) {
                $state.go('root.login');
            }
        }, 200);

    }]
)

.config(['$httpProvider',
    function($httpProvider) {
        if (!$httpProvider.defaults.headers.get) {
            $httpProvider.defaults.headers.get = {};
        }
        //disable IE ajax request caching
        $httpProvider.defaults.headers.get['If-Modified-Since'] = 'Mon, 26 Jul 1997 05:00:00 GMT';
        // extra
        $httpProvider.defaults.headers.get['Cache-Control'] = 'no-cache';
        $httpProvider.defaults.headers.get['Pragma'] = 'no-cache';
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
        }).state('root.record_step', {
            url: 'track-step'
            ,templateUrl: 'twist-track-sample.html'
            ,controller: 'trackStepController'
        }).state('root.record_step.step_type_selected', {
            url: '/:selected_step_type_id'
            ,templateUrl: 'twist-track-sample-type-selected.html'
            ,controller: 'stepTypeSelectedController'
        }).state('root.record_step.step_type_selected.excel_upload', {
            url: '/custom-excel-upload'
            ,template: ''
            ,controller: 'customExcelUploadController'
        }).state('root.record_step.step_type_selected.standard_template', {
            url: '/standard-template'
            ,template: ''
            ,controller: 'standardTemplateController'
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
        })


        ;
    }
])

;
