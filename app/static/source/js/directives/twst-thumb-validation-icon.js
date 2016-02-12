angular.module('twist.app').directive('twstThumbValidationIcon', ['$sce', 
    function($sce) {
        return {
            restrict: 'E'
            ,scope: {
                validation: '='
                ,error: '='
                ,errorsInvisible: '='
            }
            ,template: '<div class="twst-thumbs-validation-icon" ng-class="{\'twst-thumbs-validation-icon-valid\': validation, \'twst-thumbs-validation-icon-error\': error}"><ng-include src="\'static/images/thumbs-up.svg\'"></ng-include><span ng-if="!errorsInvisible" class="twst-thumbs-validation-error" ng-bind-html="formatErrors(error)"></span></div>'
            ,controller: ['$scope', 
                function ($scope) {
                    $scope.formatErrors = function (errors) {

                        if (!errors) {
                            errors = '';
                        }

                        if (errors.toString() === errors) {
                            /* one error */
                            return errors.toString();
                        } else {
                            /* multiple errors */
                            var list = '<ul>';
                            for (var i=0; i< errors.length; i++) {
                                list += '<li>' + errors[i] + '</li>';
                            }
                            list += '</ul>';
                            return list;
                        }
                    }
                }
            ]
        };
    }
]);
