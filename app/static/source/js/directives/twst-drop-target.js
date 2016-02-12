angular.module('twist.app').directive('twstDropTarget', [ 
    /* adds a drop event listener to an element and returns the read file data to the onDrop method */
    function () {
        return {
            restrict: 'AC'
            ,scope: {
                twstDropTarget: '='
            }
            ,controller: ['$scope', '$element', 
                function ($scope, $element) {

                    $element.on('dragover', function ($event) {
                        $event.preventDefault();
                        $event.stopPropagation();
                        $element.addClass('twst-file-drag-over');
                    });

                     $element.on('dragleave', function ($event) {
                        $element.removeClass('twst-file-drag-over');
                    });

                    $element.on('drop', function ($event) {
                        $event.preventDefault();
                        $event.stopPropagation();
                        $element.removeClass('twst-file-drag-over');

                        var f = $event.originalEvent.dataTransfer.files[0];

                        var reader = new FileReader();
                        reader.onload = function(e) {
                            var data = e.target.result;
                            $scope.twstDropTarget(data);
                            $scope.$apply(); // must call manually since the onload event is not angularized
                        };
                        if (f.type.indexOf('spreadsheet') != -1) {
                            reader.readAsBinaryString(f);
                        } else if (f.type.indexOf('csv') != -1) {
                            reader.readAsText(f);
                        } else if (f.type.indexOf('text/plain') != -1) {
                            reader.readAsText(f);
                        } else {
                            $scope.twstDropTarget({}, 'Unrecognized upload file type: ' + f.type);
                            $scope.$apply(); // must call manually since the onload event is not angularized
                        }
                        
                    });
                }
            ]
        };
    }
]);
