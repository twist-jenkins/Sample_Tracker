angular.module('twist.app').controller('stepTypeSelectedController', ['$scope', '$state',  '$stateParams', '$sce', '$timeout', 'Formatter', 'TypeAhead', 'Maps', 'Constants', 'TransformBuilder', 'FileParser',
    function ($scope, $state, $stateParams, $sce, $timeout, Formatter, TypeAhead, Maps, Constants, TransformBuilder, FileParser) {

        $scope.Constants = Constants;

        $scope.selectTransformTemplateType = function (which, skipGo) {
            if (which == Constants.HAMILTON_OPERATION && !$scope.isHamiltonStep(selectedTransformTypeId)) {
                return false;
            } else if (which != Constants.HAMILTON_OPERATION && $scope.isHamiltonStep(selectedTransformTypeId)) {
                return false;
            }
            if (!skipGo) {
                $state.go('root.record_transform.step_type_selected.tab_selected', {
                    selected_tab: which
                });
            }
        };

        $scope.setTransformTemplate = function (which) {
            $scope.templateTypeSelection = which;
        };

        $scope.isHamiltonStep = function () {
            if (selectedTransformTypeId == 39 || 
                selectedTransformTypeId == 48 || 
                selectedTransformTypeId == 51 || 
                selectedTransformTypeId == 70 || 
                selectedTransformTypeId == 72) {
                return true;
            }
            return false;
        };

        var selectedTransformTypeId;
        $scope.initTransformTypes.success(function (data) {
            selectedTransformTypeId = $stateParams.selected_step_type_id.split('-')[0];
            $scope.setSelectedOption(selectedTransformTypeId);
        });

        $scope.$on('$destroy', function () {
            if ($state.current.url == 'record-transform') {
                $scope.clearForm(true);
            }
        });
    }]
);
