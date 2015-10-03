var app;

app = angular.module('twist.app', ['ui.router', 'ui.bootstrap', 'ngSanitize', 'templates-main', 'ngSanitize'])


.controller('rootController', ['$scope', '$state', 'User', 
    function ($scope, $state, User) {
        $scope.user = User;
        $scope.current_year = (new Date).getFullYear();
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

.controller('trackSampleController', ['$scope', '$state', 'Api', '$sce', '$timeout', 
    function ($scope, $state, Api, $sce, $timeout) {

        /* interface backing vars */
        var returnEmptyPlate = function () {
            return {text: ''};
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
        };

        $scope.selectStepType = function (option) {
            $scope.selectedStepType = option;
            $scope.stepTypeDropdownValue = $scope.selectedStepType.text;
            setPlateArrays();
        }

        $scope.getTypeAheadBarcodes = function (queryText) {
            return Api.getBarcodes(queryText).then(function (resp) {
                return resp.data;
            });
        }

        $scope.sampleTrackFormReady = function () {

            if (!$scope.selectedStepType) {
                return false;
            }

            for (var i=0; i< $scope.sourcePlates.length; i++) {
                if ($scope.sourcePlates[i].text == '') {
                    return false;
                }
            }

            for (var i=0; i< $scope.destinationPlates.length; i++) {
                if ($scope.destinationPlates[i].text == '') {
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
        };

        var getSampleTrackSubmitData = function () {
            var data = {
                sampleTransferTypeId: $scope.selectedStepType.id
                ,sourceBarcodeId: $scope.sourcePlates[0].text
                ,destinationBarcodeId: $scope.destinationPlates[0].text
            };

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
                        $scope.submissionResultMessage = 'Error: ' + data.errorMessage + '.';
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
        }).state('root.content', {
            url: 'track-step'
            ,templateUrl: 'twist-track-sample.html'
            ,controller: 'trackSampleController'
        });
    }
])

;