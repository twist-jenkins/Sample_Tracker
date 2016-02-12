angular.module('twist.app').controller('transformSpecEditorController', ['$scope', '$state', '$stateParams', 'TransformBuilder', 'Api',
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
