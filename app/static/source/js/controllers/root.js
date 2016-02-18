angular.module('twist.app').controller('rootController', ['$scope', '$state', 'User', '$rootScope', 'localStorageService', '$location', '$timeout',
    function ($scope, $state, User, $rootScope, localStorageService, $location, $timeout) {
        $scope.user = User;
        $scope.current_year = (new Date).getFullYear();

        $scope.navTo = function (where) {
            $state.go(where);
        }

        var loginStateName = 'root.login';

        $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState) {
            if (!User.data && toState.name != loginStateName) {
                event.preventDefault();
                $state.go(loginStateName);
            }
        });

        $rootScope.$on('$stateChangeSuccess', function(event, toState) {
            $scope.currentNav = toState.name;
        });

        $rootScope.$on('$locationChangeSuccess', function(event) {
            var url = document.location.href;
            var hashUrl = url.substring(url.indexOf('#') + 1);
            if (url != hashUrl && hashUrl != '/login') {
                localStorageService.set('loginTarget', hashUrl);
            }
        });

        $scope.currentNav = $state.current.name;
    }]
);
