angular.module('twist.app').controller('viewManageTransformSpecsController', ['$scope', '$state', '$stateParams', 'Api', '$modal', '$timeout', 'Formatter',
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
