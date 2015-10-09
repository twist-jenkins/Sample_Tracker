var app;

app = angular.module('twist.app', ['ui.router', 'ui.bootstrap', 'ngSanitize', 'templates-main', 'ngSanitize'])


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

.controller('trackStepController', ['$scope', '$state', 'Api', '$sce', '$timeout', 'Formatter', 'TypeAhead', 
    function ($scope, $state, Api, $sce, $timeout, Formatter, TypeAhead) {

        /* interface backing vars */
        var returnEmptyPlate = function () {
            return {text: '', title: ''};
        }
        $scope.stepTypeDropdownValue = 'Select a Step';
        $scope.sourcePlates = [returnEmptyPlate()];      /* backs both the field interator and the entered data */
        $scope.destinationPlates = [returnEmptyPlate()]; /* backs both the field interator and the entered data */


        var setPlateArrays = function () {
            /* we need to expand or contract the plate arrays to match the selected step type */
            while ($scope.sourcePlates.length != $scope.selectedStepType.source_plate_count) {
                if ($scope.sourcePlates.length < $scope.selectedStepType.source_plate_count) {
                    $scope.sourcePlates.push(returnEmptyPlate());
                } else if ($scope.sourcePlates.length > $scope.selectedStepType.source_plate_count) {
                    $scope.sourcePlates.splice($scope.sourcePlates.length - ($scope.sourcePlates.length - $scope.selectedStepType.source_plate_count));
                }
            }
            while ($scope.destinationPlates.length != $scope.selectedStepType.destination_plate_count) {
                if ($scope.destinationPlates.length < $scope.selectedStepType.destination_plate_count) {
                    $scope.destinationPlates.push(returnEmptyPlate());
                } else if ($scope.destinationPlates.length > $scope.selectedStepType.destination_plate_count) {
                    $scope.destinationPlates.splice($scope.destinationPlates.length - ($scope.destinationPlates.length - $scope.selectedStepType.destination_plate_count));
                }
            }

            switch ($scope.selectedStepType.transfer_template_id) {
                case 1:
                    for (var i=0; i<$scope.destinationPlates.length; i++) {
                        $scope.destinationPlates[i].title = '';
                    }
                    break;
                case 13:
                    for (var i=0; i<$scope.destinationPlates.length; i++) {
                        $scope.destinationPlates[i].title = 'Quadrant&nbsp;' + (i + 1) + ':&nbsp;';
                    }
                    break;
                case 14:
                    $scope.destinationPlates[0].title = 'Left:&nbsp;&nbsp;';
                    $scope.destinationPlates[1].title = 'Right:&nbsp;';
                    break;
                case 18:
                    for (var i=0; i<$scope.sourcePlates.length; i++) {
                        $scope.sourcePlates[i].title = 'Quadrant&nbsp;' + (i + 1) + ':&nbsp;';
                    }
                    break;
                default :
                    /* do nothing */
                    break;
            }
        };

        $scope.selectStepType = function (option) {
            $state.go('root.record_step.step_type_selected', {
                selected_step_type_id: option.id + '-' + Formatter.stripNonAlphaNumeric(Formatter.lowerCaseAndSpaceToDash(option.text), true)
            });
        }

        $scope.setSelectedOption = function (optionId) {
            for (var i=0; i< $scope.stepTypeOptions.length;i++) {
                var option = $scope.stepTypeOptions[i];
                if (option.id == optionId) {
                    $scope.selectedStepType = option;
                    $scope.stepTypeDropdownValue = $scope.selectedStepType.text;
                    setPlateArrays();
                    break;
                }
            }
        }

        $scope.getTypeAheadBarcodes = TypeAhead.getTypeAheadBarcodes;

        $scope.sampleTrackFormReady = function () {

            if (!$scope.selectedStepType) {
                return false;
            }

            for (var i=0; i< $scope.sourcePlates.length; i++) {
                if ($scope.sourcePlates[i].text == '') {
                    return false;
                } else if ($scope.sourcePlates[i].text.length < 6) {
                    return false;
                }
            }

            for (var i=0; i< $scope.destinationPlates.length; i++) {
                if ($scope.destinationPlates[i].text == '') {
                    return false;
                } else if ($scope.destinationPlates[i].text.length < 6) {
                    return false;
                }
            }

            return true;
        }

        $scope.clearForm = function () {
            $scope.selectedStepType = null;
            $scope.stepTypeDropdownValue = 'Select a Step';
            $scope.sourcePlates = [returnEmptyPlate()];
            $scope.destinationPlates = [returnEmptyPlate()];
            $state.go('root.record_step');
        };

        var getSampleTrackSubmitData = function () {
            var data = {
                sampleTransferTypeId: $scope.selectedStepType.id
                ,sampleTransferTemplateId: $scope.selectedStepType.transfer_template_id
                ,sourcePlates: []
                ,destinationPlates: []
            };

            for (var i=0; i< $scope.sourcePlates.length; i++) {
                data.sourcePlates.push($scope.sourcePlates[i].text);
            }

            for (var i=0; i< $scope.destinationPlates.length; i++) {
                data.destinationPlates.push($scope.destinationPlates[i].text);
            }

            /* if this is a non-movement step (source=destinstion), add source as destination */
            if ($scope.selectedStepType.destination_plate_count == 0) {
                data.destinationPlates.push($scope.sourcePlates[0].text);
            }

            return data;
        };

        $scope.submitStep = function () {
            if (!$scope.submitting && $scope.sampleTrackFormReady()) {

                $scope.submittingStep = true;
                Api.submitSampleStep(getSampleTrackSubmitData()).success(function (data) {

                    if (data.success) {
                        $scope.submittingStep = false;
                        $scope.submissionResultMessage = 'This <span class="twst-step-text">' + $scope.selectedStepType.text + '</span> step was successfully recorded.';
                        $scope.submissionResultVisible = 1;
                        $scope.clearForm();
                    } else {
                        $scope.submissionResultMessage = 'Error: ' + data.errorMessage;
                        $scope.submissionResultVisible = -1;
                        $scope.submittingStep = false;
                    }

                    $timeout(function () {
                        $scope.submissionResultVisible = 0;
                        $timeout(function () {
                            $scope.submissionResultMessage = null;
                        }, 400);
                    }, 5000);
                    
                }).error(function (data) {
                    $scope.submittingStep = false;
                    console.log('ERROR!');
                });
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
        var selectedTranferTypeId = $stateParams.selected_step_type_id.split('-')[0];
        $scope.setSelectedOption(selectedTranferTypeId);
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
            Api.getPlateInfo($scope.plateId).then(function (resp) {
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
        Api.getPlateSteps().success(function (data) {
            $scope.plateSteps = data;
        });

    }]
)

.controller('plateDetailsController', ['$scope', '$state', 'Api', 'TypeAhead', 
    function ($scope, $state, Api, TypeAhead) {
        $scope.getTypeAheadBarcodes = TypeAhead.getTypeAheadBarcodes;
        $scope.plateBarcode = '';

        $scope.getDetailsClicked = function () {
            if ($scope.plateBarcode.length > 5) {
                $state.go('root.plate_details.barcode_entered', {
                    entered_barcode: $scope.plateBarcode
                });
            }
        };

        $scope.getPlateDetails = function (barcode) {
            $scope.plateBarcode = barcode;

            $scope.fetchingDetails = true;

            Api.getPlateDetails(barcode).success(function (data) {
                $scope.fetchingDetails = false;
                $scope.plateDetails = data;
            });
        }
    }]
)

.controller('plateDetailsBarcodeEnteredController', ['$scope', '$state',  '$stateParams', 
    function ($scope, $state, $stateParams) {
        var barcode = $stateParams.entered_barcode;
        $scope.getPlateDetails(barcode);
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
                $location.path((routeUrl == '/login' || routeUrl == '/') ? '/track-step' : routeUrl);
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
            ,template: ''
            ,controller: 'stepTypeSelectedController'
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
        })


        ;
    }
])

;