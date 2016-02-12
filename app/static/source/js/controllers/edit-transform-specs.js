angular.module('twist.app').controller('editTransformSpecsController', ['$scope', '$state', '$stateParams',
    function ($scope, $state, $stateParams) {
        $scope.transformSpec = null;
        $scope.setSelectedPlanTab($scope.edit);
    }]
);
