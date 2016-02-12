angular.module('twist.app').directive('twstDragOutLink', [ 
    /* adds a drop event listener to an element and returns the read file data to the onDrop method */
    function () {
        return {
            restrict: 'AC'
            ,scope: {
                twstDragOutLink: '='
                ,onDrag: '=?'
            }
            ,controller: ['$scope', '$element', 
                function ($scope, $element) {
                    $element[0].draggable = true;

                    $element[0].addEventListener('dragstart', function ($event) {
                        $event.dataTransfer.setData("DownloadURL", $scope.twstDragOutLink.split('|').join(':'));
                        if ($scope.onDrag) {
                            $scope.onDrag();
                        }
                    }, false);

                    /* 

                    TO DO: add an click event listener to trigger a saveAs blob file download from the Hamilton worklist in the transform spec

                    */

                }
            ]
        };
    }
]);
