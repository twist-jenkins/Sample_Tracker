angular.module('twist.app').controller('stepTypeSelectedController', ['$scope', '$state',  '$stateParams', '$sce', '$timeout', 'Formatter', 'TypeAhead', 'Maps', 'Constants', 'TransformBuilder', 'FileParser',
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
            if ($state.current.url == 'record-transform') {
                $scope.clearForm(true);
            }
        });
    }]
);
