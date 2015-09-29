var app;

app = angular.module('twst.app', ['ui.router'])


.controller('rootController', ['$scope', '$state', '$location', 
	function ($scope, $state, $location) { 
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
            ,template: '<p>Angular is IN DA HOUSE!</p>'
            ,controller: 'rootController'
        });
    }
])

;