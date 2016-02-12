angular.module('twist.app').directive('twstSpinner', ['$interval',  
    function($interval) {
        return {
            restrict: 'C',
            scope: {
            },
            controller: ['$scope', '$element', 
                function($scope, $element) {

                    var dims =  [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
                     100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
                      100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
                       100, 100, 100, 100, 100, 100, 100, 94, 88, 82, 76, 70, 64, 58, 52, 47, 41, 35, 29, 23, 17, 11, 5, 0, 5,
                        11, 17, 23, 29, 35, 41, 47, 52, 58, 64, 70, 76, 82, 88, 94];
                    var block1Pos = 66;
                    var block2Pos = 50;
                    var block3Pos = 34;

                    var holder = angular.element('<div class="twst-spinner-blocks"></div>');

                    var block1 = angular.element('<span></span>');
                    var block2 = angular.element('<span></span>');
                    var block3 = angular.element('<span></span>');

                    var block1Outer = angular.element('<span class="twst-spinner-block-outer"></span>');
                    var block2Outer = angular.element('<span class="twst-spinner-block-outer"></span>');
                    var block3Outer = angular.element('<span class="twst-spinner-block-outer"></span>');
                    
                    holder.append(block1Outer.append(block1),
                                    block2Outer.append(block2),
                                    block3Outer.append(block3));

                    $element.append(holder);

                    $element.on('$destroy', function() {
                      $interval.cancel(interval);
                    });

                    var interval = $interval(function () {
                        var block1Dim = dims[(block1Pos++)%100];
                        block1.css({width: block1Dim + '%', height: block1Dim + '%'});
                        var block2Dim = dims[(block2Pos++)%100];
                        block2.css({width: block2Dim + '%', height: block2Dim + '%'});
                        var block3Dim = dims[(block3Pos++)%100];
                        block3.css({width: block3Dim + '%', height: block3Dim + '%'});
                    }, 11);

                    return $element;
                }
            ]
        };
    }
]);
