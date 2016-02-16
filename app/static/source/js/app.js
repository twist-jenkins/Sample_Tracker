var app;

app = angular.module('twist.app', ['ui.router', 'ui.bootstrap', 'ngSanitize', 'templates-main', 'LocalStorageModule'])

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
        }).state('root.record_transform.step_type_selected.tab_selected.hamilton_select', {
            url: '/select'
            ,views: {
                "hamiltonWizard@root.record_transform.step_type_selected.tab_selected": {
                    templateUrl: 'twist-hamilton-select.html'
                    ,controller: 'hamiltonSelectController'
                }
            }
        }).state('root.record_transform.step_type_selected.tab_selected.hamilton_wizard', {
            url: '/wizard/:hamilton_info'
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
        }).state('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.destination_placement_and_scan', {
            url: '/destination-placement-and-scan'
            ,views: {
                "hamiltonStep@root.record_transform.step_type_selected.tab_selected.hamilton_wizard": {
                    templateUrl: 'twist-hamilton-step-destination-placement-and-scan.html'
                    ,controller: 'hamiltonWizardDestinationPlacementAndScanController'
                }
            }
        }).state('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.destination_placement_confirmation', {
            url: '/destination-placement-confirmation'
            ,views: {
                "hamiltonStep@root.record_transform.step_type_selected.tab_selected.hamilton_wizard": {
                    templateUrl: 'twist-hamilton-step-destination-placement-confirmation.html'
                    ,controller: 'hamiltonWizardDestinationPlacementConfirmationController'
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
