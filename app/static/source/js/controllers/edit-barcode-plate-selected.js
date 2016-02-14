angular.module('twist.app').controller('editBarcodePlateSelectedController', ['$scope', '$state',  '$stateParams',
    function ($scope, $state, $stateParams) {
        var plateId = $stateParams.selected_plate_id;
        $scope.getPlateInfo(plateId);
    }]
);
