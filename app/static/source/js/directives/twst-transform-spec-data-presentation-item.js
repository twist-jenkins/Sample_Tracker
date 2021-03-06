angular.module('twist.app').directive('twstTransformSpecDataPresentationItem', ['$compile', 'Constants', '$sce',   
    function($compile, Constants, $sce) {
        return {
            scope: {
                transformSpec: '='
                ,item: '='
            }
            ,restrict: 'E'
            ,link: function($scope, element, attrs) {

                var ml = '';

                $scope.itemData = $scope.item.item;

                if ($scope.itemData.title) {
                    ml += '<h4 ng-bind-html="itemData.title"></h4>';
                }

                switch ($scope.itemData.type) {
                    case Constants.DATA_TYPE_TEXT:
                        ml += '<p ng-bind-html="itemData.data"></p>';
                        break;
                    case Constants.DATA_TYPE_FILE_DATA:
                        // assemble the presented data
                        ml += '<button class="twst-button twst-download-button" ng-click="sendFile(itemData.data)"><div class="twst-button-icon"><ng-include src="\'static/images/download.svg\'"></ng-include></div>&nbsp;Download</button>';
                        break;
                    case Constants.DATA_TYPE_LINK:
                        // assemble the presented data
                        ml += '<a ng-href="{{itemData.data}}" target="_blank">{{itemData.data}}</a>';
                        break;
                    case Constants.DATA_TYPE_CSV:
                        var rows = $scope.itemData.data.split('\r\n');

                        ml += '<table class="twst-data-readout-table twst-smaller">';

                        for (var i=0; i< rows.length; i++) {
                            var thisRow = rows[i];
                            if (thisRow && thisRow != '') {
                                if (!i) {
                                    //header
                                    ml += '<tr><td class="twst-data-readout-table-header">' + thisRow.split(',').join('</td><td class="twst-data-readout-table-header">') + '</td></tr>';
                                } else {
                                    ml += '<tr><td>' + thisRow.split(',').join('</td><td>') + '</td></tr>';
                                }
                            }
                        }

                        ml += '</table>';

                        break;
                    
                    default :
                        console.log('Error: Unrecognized response command type = [' + $scope.itemData.type + ']');
                        break;
                }

                $scope.sendFile = function (fileData) {
                    var fileBlob = new Blob([fileData], {type: $scope.itemData.mimeType});
                    saveAs(fileBlob, $scope.itemData.fileName);
                }

                var el = angular.element(ml);
                compiler = $compile(el);
                element.append(el);
                compiler($scope);
            }
        };
    }
]);
