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

        $scope.transformSpec = TransformBuilder.newTransformSpec();
        $scope.transformSpec.setPlateStepDefaults();

        $scope.selectStepType = function (option) {
            $scope.transformSpec.setTransformSpecDetails(option);
            $scope.transformSpec.setTitle(option.text);

            var route = 'root.record_transform.step_type_selected';

            if ($scope.transformSpec.map.type == Constants.USER_SPECIFIED_TRANSFER_TYPE) {
                route += '.' + Constants.FILE_UPLOAD;
            } else {
                route += '.' + Constants.STANDARD_TEMPLATE;
            }

            $state.go(route, {
                selected_step_type_id: option.id + '-' + Formatter.lowerCaseAndSpaceToDash(Formatter.stripNonAlphaNumeric(option.text, true, true).trim())
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
            if ($scope.transformSpec.details.transfer_template_id == 25 || $scope.transformSpec.details.transfer_template_id == 26 || $scope.transformSpec.details.transfer_template_id == 27 || $scope.transformSpec.details.transfer_template_id == 28 || $scope.transformSpec.details.transfer_template_id == 29) {
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
            $state.go('root.record_transform.step_type_selected.' + which);
        };

        $scope.setTransferTemplate = function (which) {
            $scope.templateTypeSelection = which;
        };

        $scope.initTransferTypes.success(function (data) {
            var selectedTranferTypeId = $stateParams.selected_step_type_id.split('-')[0];
            $scope.setSelectedOption(selectedTranferTypeId);
        });
    }]
)

.controller('customExcelUploadController', ['$scope', '$state', '$stateParams', 'Constants', 
    function ($scope, $state, $stateParams, Constants) {
        //inherits scope from trackStepController via stepTypeSelectedController
        $scope.setTransferTemplate(Constants.FILE_UPLOAD);
    }]
)

.controller('standardTemplateController', ['$scope', '$state', '$stateParams', 'Constants', 
    function ($scope, $state, $stateParams, Constants) {
        //inherits scope from trackStepController via stepTypeSelectedController
        $scope.setTransferTemplate(Constants.STANDARD_TEMPLATE);
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

        var deleteSuccess = function (plan) {
            $scope.specActionResultMessage = 'Spec <strong>' + plan.id + '</strong> was successfully deleted.' ;
            $scope.specActionResultVisible = 1;

            $timeout(function () {
                $scope.specActionResultVisible = 0;
                $timeout(function () {
                    $scope.specActionResultMessage = null;
                }, 400);
            }, 5000);
        };

        var deleteError = function (plan) {
            $scope.specActionResultMessage = 'An error occured while trying to delete spec <strong>' + plan.id + '</strong>.' ;
            $scope.specActionResultVisible = -1;

            $timeout(function () {
                $scope.specActionResultVisible = 0;
                $timeout(function () {
                    $scope.specActionResultMessage = null;
                }, 400);
            }, 5000);
        };

        $scope.deleteSpec = function (plan) {

            var deleteConfirmModal = $modal.open({
                templateUrl: 'twist-confirm-spec-delete-modal.html'
                ,size: 'md'
                ,controller: ['$scope', '$modalInstance', 'plan',  
                    function($scope, $modalInstance, plan) {

                        $scope.plan = plan;

                        $scope.clickCancel = function() {
                            $modalInstance.dismiss();
                        }
                        $scope.clickDelete = function() {

                            plan.deleting = true;
                            Api.deleteTransformSpec(plan.id).success(function (data) {
                                loadSpecs();
                                $modalInstance.close();
                                deleteSuccess(plan);
                            }).error(function () {
                                $modalInstance.close();
                                deleteError(plan); 
                            });
                        }
                    }
                ]
                ,resolve: {
                    plan: function() {
                        return plan;
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
                var thisSpec = data;
                thisSpec.plan = JSON.parse(thisSpec.data_json.plan);
                $scope.selectedSpec = thisSpec;
            });
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
        }).state('root.record_transform.step_type_selected.file_upload', {
            url: '/custom-file-upload'
            ,template: ''
            ,controller: 'customExcelUploadController'
        }).state('root.record_transform.step_type_selected.standard_template', {
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
