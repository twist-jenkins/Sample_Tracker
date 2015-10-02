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

.controller('trackSampleController', ['$scope', '$state', 'Api', '$sce', 
    function ($scope, $state, Api, $sce) {

        /* interface backing vars */
        var returnEmptyPlate = function () {
            return {text: ''};
        }
        $scope.stepTypeDropdownValue = 'Select a Step';
        $scope.stepTypeOptions = [];
        $scope.sourcePlates = [returnEmptyPlate()];      /* backs both the field interator and the entered data */
        $scope.destinationPlates = [returnEmptyPlate()]; /* backs both the field interator and the entered data */

        $scope.selectStepType = function (option) {
            $scope.stepTypeDropdownValue = option.text;
            $scope.selectedStepType = option;
        }

        $scope.getTypeAheadBarcodes = function (queryText) {
            return Api.getBarcodes(queryText).then(function (resp) {
                return resp.data;
            });
        }

        $scope.sampleTrackFormReady = function () {
            var ready = true;

            for (var i=0; i< $scope.sourcePlates.length; i++) {
                if ($scope.sourcePlates[i].text == '') {
                    ready = false;
                    break;
                }
            }

            for (var i=0; i< $scope.destinationPlates.length; i++) {
                if ($scope.destinationPlates[i].text == '') {
                    ready = false;
                    break;
                }
            }

            return ready;
        }

        $scope.clearForm = function () {
            $scope.stepTypeDropdownValue = 'Select a Step';
            $scope.sourcePlates = [returnEmptyPlate()];
            $scope.destinationPlates = [returnEmptyPlate()];
        };

        var getSampleTrackSubmitData = function () {
            var data = {
                sampleTransferTypeId: $scope.selectedStepType.value
                ,sourceBarcodeId: $scope.sourcePlates[0].text
                ,destinationBarcodeId: $scope.destinationPlates[0].text
            };

            return data;
        };

        $scope.submitStep = function () {
            if ($scope.sampleTrackFormReady) {
                Api.submitSampleStep(getSampleTrackSubmitData()).success(function (data) {
                    $scope.submissionResultMessage = '<span class="twst-checkmark">&#x2713;</span> This <span class="twst-step-text">' + $scope.selectedStepType.text + '</span> step was successfully recorded.';
                }).error(function (data) {
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