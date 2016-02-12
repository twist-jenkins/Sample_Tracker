angular.module('twist.app').directive('plateView', [ 
    function() {
        return {
            scope: {
                plate: '='
                ,clickFunc: '=?'
            }
            ,templateUrl: 'twist-plate-view.html'
            ,controller: ['$scope', '$sce', function ($scope, $sce) {

                $scope.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

                $scope.getLetter = function (ind) {
                    return $scope.alphabet.charAt(Math.floor(ind/$scope.plate.rowLength))
                };

                $scope.getX = function (well) {
                    return (well.col)*30 + 8*well.col + 15;
                };

                $scope.getTooltip = function (well) {
                    return '<div class="twst-plate-view-well-tooltip"><div class="twst-plate-view-well-tooltip-inner"><h3>' + $scope.alphabet.charAt(well.row - 1) + well.col + '</h3><div>' + (well.trashed ? '<span class="twst-plate-view-well-trashed">TRASHED</span>' : '') + 'Sample Id:<br/><strong>' + well.sampleId + '</strong></div></div></div>';
                };

                $scope.getY = function (well) {
                    return (well.row)*30 + 8*well.row + 20;
                };

                $scope.wellClicked = function (well) {
                    if (well.sampleId) {
                        well.highlighted = !well.highlighted;

                        if ($scope.clickFunc) {
                            $scope.clickFunc(well)
                        }
                    }
                };
            }]
        };
    }
]);
