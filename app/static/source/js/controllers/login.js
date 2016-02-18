angular.module('twist.app').controller('loginController', ['$scope', '$state',  '$http', 'localStorageService',
    function ($scope, $state, $http, localStorageService) {
        $http({url: '/google-login'}).success(function (data) {
            $scope.googleLoginUrl = data.login_url;
        }).error(function () {
            $scope.loginPageError = true;
        });
    }]
);
