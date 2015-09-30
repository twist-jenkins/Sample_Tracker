app = angular.module("twist.app")

.directive('twistHeader', [ 
    function() {
        return {
            restrict: 'E'
            ,templateUrl: 'twist-header.html'
            , controller: ['$scope', 
                function ($scope) {
                    //...
                }
            ]
        };
    }
])
;