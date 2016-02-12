angular.module('twist.app').directive('barcodeSvg', [ 
    function() {
        return {
            scope: {
                barcode: '='
            }
            ,restrict: 'E'
            ,template: '<svg xmlns="http://www.w3.org/2000/svg"></svg>'
            ,controller: ['$scope', '$element', '$attrs', 'User', 
                function($scope, $element, $attrs, User) {

                    if (!$scope.barcode) {
                        $scope.barcode = "INVALID"
                    };

                    var bc = $("<div></div>").barcode($scope.barcode, "code128", {barWidth: 2, barHeight: 100, output: 'svg'});

                    bc.html(bc.html().substring(bc.html().indexOf('&lt;'), bc.html().lastIndexOf('</object>')));

                    bc = bc.html(bc.get(0).childNodes[0].nodeValue.substring(0, bc.get(0).childNodes[0].nodeValue.length-2));

                    var viewBoxDims = '0 0 ' + $(bc.children(0).children(0)[0]).attr('width') + ' ' + $(bc.children(0).children(0)[0]).attr('height');
                    $element.children().get(0).setAttribute("viewBox", viewBoxDims);

                    jQuery($element.children()[0]).html(bc.children(0).html());
                }
            ]
        };
    }
]);
