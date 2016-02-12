angular.module('twist.app').controller('transformSpecsController', ['$scope', '$state', '$stateParams',
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
