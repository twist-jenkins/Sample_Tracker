angular.module('twist.app').directive('viewBox', [ 
    function() {
        return {
            scope: {
                plate: '='
            }
            ,restrict: 'A'
            ,link: function($scope, element, attrs) {
                var getViewBox = function () {
                    return "0 0 " + ($scope.plate.rowLength*30 + 8*$scope.plate.rowLength + 56) + ' ' + ($scope.plate.wellCount/$scope.plate.rowLength*30 + 8*$scope.plate.wellCount/$scope.plate.rowLength + 56);
                }
                element.get(0).setAttribute("viewBox", getViewBox());
            }
        };
    }
]);
