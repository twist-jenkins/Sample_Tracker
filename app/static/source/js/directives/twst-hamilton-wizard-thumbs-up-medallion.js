angular.module('twist.app').directive('twstHamiltonWizardThumbsUpMedallion', ['$timeout',  
    function($timeout) {
        return {
            scope: {
                fadeFinish: '='
                ,thumbsUpIndex: '='
            }
            ,restrict: 'A'
            ,template: '<div class="twst-hamilton-wizard-thumbs-up-medallion-inner"><twst-thumb-validation-icon validation="1" error="0"></twst-thumb-validation-icon></div>'
            ,link: function($scope, element, attrs) {
                element.addClass('twst-hamilton-wizard-thumbs-up-medallion');
                $timeout(function () {
                    element.addClass('twst-hamilton-wizard-thumbs-up-medallion-rise');
                }, 0);

                var fader = $timeout(function () {
                    element.addClass('twst-hamilton-wizard-thumbs-up-transparent');
                    $timeout(function () {
                        $scope.fadeFinish($scope.thumbsUpIndex);
                    }, 200);
                }, 400);

                element.on('$destroy', function() {
                  $timeout.cancel(fader);
                });
            }
        };
    }
]);
