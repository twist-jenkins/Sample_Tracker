angular.module('twist.app').directive('twstMessage', ['$sce', '$timeout',  
    function($sce, $timeout) {
        return {
            restrict: 'E'
            ,scope: {
                message: '='
                ,visibleAndValid: '='
                ,clearParentData: '='
            }
            ,template: '<div class="twst-message" ng-class="{\'twst-message-visible\':visibleAndValid, \'twst-success\': visibleAndValid > 0, \'twst-error\': visibleAndValid < 0}"><span class="twst-message-text" ng-bind-html="message"></span></div>'
            ,controller: ['$scope', '$element',    
                function($scope, $element) {
                    $scope.$watch('visibleAndValid', function(newValue, oldValue) {
                        if (newValue != 0) {
                            $timeout(function () {
                                $scope.visibleAndValid = 0;
                                $timeout(function () {
                                    if ($scope.clearParentData) {
                                        $scope.clearParentData();
                                    }
                                }, 800);
                            }, 5000);
                        };
                    }) 
                }
            ]
        };
    }
]);
