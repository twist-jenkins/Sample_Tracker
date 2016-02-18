angular.module('twist.app').controller('transformSpecViewSpecController', ['$scope', '$state', '$stateParams', 'TransformBuilder', 'Api', 'Formatter', '$location',
    function ($scope, $state, $stateParams, TransformBuilder, Api, Formatter, $location) {

        $scope.backToSpecList = function () {
            $state.go('root.transform_specs.view_manage');
        }

        $scope.continueHamilton = function () {
            $location.path('/record-transform/' + $scope.selectedSpec.plan.details.transfer_type_id + '-' + Formatter.lowerCaseAndSpaceToDash($scope.selectedSpec.plan.title) + '/hamilton/wizard/' + $scope.selectedSpec.plan.details.hamilton.barcode.toLowerCase() + '-' + Formatter.lowerCaseAndSpaceToDash(Formatter.dashToSpace($scope.selectedSpec.plan.details.hamilton.label)) + '/finish-run/' + $scope.selectedSpec.spec_id)
        };

        $scope.trashSamples = function (spec_id) {
            $state.go('root.trash_samples.by_transform_spec', {
                spec_id: spec_id
            });
        }

        var specId = $stateParams.spec_id;
        if (!$scope.selectedSpec) {
            $scope.specLoading = true;
            Api.getTransformSpec(specId).success(function (data) {
                $scope.specLoading = false;
                var thisSpec = data.data;
                thisSpec.plan = thisSpec.data_json;
                $scope.selectedSpec = thisSpec;
            });
        } else {
            console.log($scope.selectedSpec);
        }
    }]
)
