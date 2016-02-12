angular.module('twist.app').directive('twstCustomRadio', [ 
    function () {
        return {
            restrict: 'AC',
            controller: ['$scope', '$element',    
                function($scope, $element) {

                    var innerDiv = '<div><span>' + $element.attr('val') + '</span></div>';

                    if ($element.hasClass('twst-custom-radio-as-checkbox')) {
                        innerDiv = '<div><svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><line id="svg_1" y2="20.31755" x2="20.20392" y1="-0.44886" x1="-0.5625" stroke-width="2" stroke="#ffffff" fill="none" class="twst-custom-checkbox-x"/><line transform="rotate(90 9.820711135864258,9.93434524536133) " id="svg_2" y2="20.31755" x2="20.20392" y1="-0.44886" x1="-0.5625" stroke-width="2" stroke="#ffffff" fill="none" class="twst-custom-checkbox-x"/></svg></div>';
                    }

                    $element.prepend(innerDiv);

                    $element.on('focus', function () {
                        $element.addClass('twst-focused-true');
                    });

                    $element.on('blur', function () {
                        $element.removeClass('twst-focused-true');
                    });

                    $element.on('keydown', function ($event) {
                        if ($event.keyCode == 13) {
                            $element.trigger('click');
                        }
                    });
                }
            ]
        };
    }
]);
