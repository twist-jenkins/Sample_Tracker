angular.module('twist.app').directive('twistHeader', [ 
    function() {
        return {
            restrict: 'E'
            ,templateUrl: 'twist-header.html'
            , controller: ['$scope', 'localStorageService', 
                function ($scope, localStorageService) {
                    $scope.logout = function () {
                        localStorageService.remove('loginTarget');
                        document.location.href = '/logout';
                    }
                }
            ]
        };
    }
]);
