angular.module('twist.app').controller('trashSamplesController', ['$scope', '$state', '$stateParams', 'TypeAhead', '$timeout',
    function ($scope, $state, $stateParams, TypeAhead, $timeout) {
        $scope.getTransformSpecIds = TypeAhead.getTransformSpecIds;

        $scope.transformSpec = {};

        $scope.transformIdSelected = function () {
            $state.go('root.trash_samples.by_transform_spec', {
                spec_id: $scope.transformSpec.id
            });
        }
    }]
)
