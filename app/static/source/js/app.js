var app;

app = angular.module('twist.app', ['ui.router', 'ui.bootstrap', 'ngSanitize', 'templates-main'])


.controller('rootController', ['$scope', '$state', '$location', 
    function ($scope, $state, $location) { 
        $scope.current_year = (new Date).getFullYear();
    }]
)

.run(['$state', 
    function($state) {
        $state.go('root');
    }]
)

.config(['$stateProvider', 
    function($stateProvider) {
        return $stateProvider.state('root', {
            url: '/'
            ,templateUrl: 'twist-base.html'
            ,controller: 'rootController'
        });
    }
])

;