angular.module('twist.app').directive('twstTransformSpecDataRequestItem', ['$compile', 'Constants', '$timeout',   
    function($compile, Constants, $timeout) {
        return {
            scope: {
                transformSpec: '='
                ,item: '='
                ,readOnly: '=?'
            }
            ,restrict: 'E'
            ,link: function($scope, element, attrs) {

                var ml = '';

                $scope.itemData = $scope.item.item;

                /* IMPORTANT $scope.item.validData **MUST** be set true or false whenever input item data changes
                * (truthy & false-y values work too - so the initial value of 'undefined' works to start)
                *  $scope.item.validData for each requested data item will be checked to see
                *  if the submit transform button should be enabled
                */

                if (! $scope.transformSpec.details.requestedData) {
                    $scope.transformSpec.details.requestedData = {};
                    $scope.transformSpec.details.dataRequests = {};
                }

                $scope.transformSpec.details.dataRequests[$scope.itemData.forProperty] = $scope.item;

                if ($scope.itemData.title) {
                    ml += '<h4>{{itemData.title}}</h4>';
                }

                if ($scope.itemData.type.indexOf(Constants.DATA_TYPE_ARRAY) == 0) {

                    var arrayCount = $scope.itemData.type.split('.')[1] - 0;

                    $scope.transformSpec.details.requestedData[$scope.itemData.forProperty] = new Array(4);


                    $scope.validations = new Array(4);
                    $scope.errors = new Array(4);

                    for (var i=0; i < arrayCount; i++) {
                        if (!$scope.readOnly) {
                            ml +=   '<p>' +
                                        '<input type="text" class="form-control" ng-model="transformSpec.details.requestedData[\'' + $scope.itemData.forProperty + '\'][' + i + ']" ng-blur="validate(' + i + ', true);"/>' +
                                        '<twst-thumb-validation-icon validation="validations[' + i + ']" error="errors[' + i + ']"></twst-thumb-validation-icon>' +
                                    '</p>';
                        } else {
                            ml += '<p><strong>' + $scope.transformSpec.details.requestedData[$scope.itemData.forProperty][i] + '</strong></p>';
                        }
                        
                    }

                    $scope.validate = function (arrayIndex, errorOnEmpty) {

                        var returnValidate = function (arrInd) {

                            if ($scope.itemData.dataType = Constants.DATA_TYPE_BARCODE) {

                                var val = $scope.transformSpec.details.requestedData[$scope.itemData.forProperty][arrInd];

                                return function () {
                                    $scope.item.validData = 0;
                                    if (!val) {
                                        if (errorOnEmpty) {
                                            $scope.validations[arrInd] = false;
                                            $scope.errors[arrInd] = 'This item is required.';
                                        } else {
                                            $scope.validations[arrInd] = null;
                                            $scope.errors[arrInd] = null;
                                        }
                                    } else if (val.indexOf(Constants.BARCODE_PREFIX_PLATE) != 0) {
                                        $scope.validations[arrInd] = false;
                                        $scope.errors[arrInd] = 'Value is not a recognized plate barcode';
                                    } else if (val && val.length) {

                                        //check that we haven't already scanned this one
                                        var allVals = '|' + $scope.transformSpec.details.requestedData[$scope.itemData.forProperty].join('|') + '|';
                                        if (allVals.indexOf('|' + val + '|') != allVals.lastIndexOf('|' + val + '|')) {
                                            $scope.validations[arrInd] = false;
                                            $scope.errors[arrInd] = 'This barcode has already been entered.';
                                        } else {

                                            // TODO  We ALSO need to validate the PCA barcodes that were included against the db are real PCA plate barcodes
                                            // and supply this feedback to the user

                                            $scope.validations[arrInd] = 1;
                                            $scope.errors[arrInd] = null;
                                        }
                                    }

                                    /* ugly way to test if all validations for this array passed*/
                                    if ($scope.validations.join('').length == arrayCount) {
                                        $scope.item.validData = true;
                                    } else {
                                        $scope.item.validData = 0;
                                    }
                                    $scope.transformSpec.updateOperationsList(true);
                                }
                            }

                            return function () {
                                console.log('handle other requested item dataTypes!');
                                return false;
                            }

                            
                        }

                        $timeout.cancel($scope['validationTimeout' + arrayIndex]);
                        $scope['validationTimeout' + arrayIndex] = $timeout(returnValidate(arrayIndex), 200);
                    }

                    $scope.$watch('item.validateNow', function (newVal, oldVal) {
                        if (newVal) {
                            var array = $scope.transformSpec.details.requestedData[$scope.itemData.forProperty];
                            for (var i=0; i< array.length; i++) {
                                $scope.validate(i, true); 
                            }  
                        }
                    });
                } else if ($scope.itemData.type.indexOf(Constants.DATA_TYPE_BARCODE) == 0) {
                    $scope.validation = null;
                    $scope.error = null;

                    var barcodeType = $scope.itemData.type.split('.')[1];

                    if (!$scope.readOnly) {
                        ml +=   '<input type="text" class="form-control" ng-model="transformSpec.details.requestedData[\'' + $scope.itemData.forProperty + '\']" ng-blur="validate(true);"/>' +
                                '<twst-thumb-validation-icon validation="validation" error="error"></twst-thumb-validation-icon>';
                    } else {
                        ml += '<p><strong>' + $scope.transformSpec.details.requestedData[$scope.itemData.forProperty] + '</strong></p>';
                    }

                    $scope.validate = function (errorOnEmpty) {
                        var returnValidate = function () {
                            return function () {
                                var val = $scope.transformSpec.details.requestedData[$scope.itemData.forProperty];
                                $scope.item.validData = 0;
                                if (!val) {
                                    if (errorOnEmpty) {
                                        $scope.validation = false;
                                        $scope.error = 'This item is required.';
                                    } else {
                                        $scope.validation = null;
                                        $scope.error = null;
                                    }
                                } else if (val.indexOf(Constants.BARCODE_PREFIX_PLATE) != 0) {
                                    $scope.validation = false;
                                    $scope.error = 'Value is not a recognized plate barcode';
                                } else if (val && val.length) {
                                    $scope.validation = 1;
                                    $scope.error = null;
                                    $scope.item.validData = true;
                                }

                                $scope.transformSpec.updateOperationsList(true);
                            }
                        }

                        $timeout.cancel($scope.validationTimeout);
                        $scope.validationTimeout = $timeout(returnValidate(), 200);
                    }

                } else if ($scope.itemData.type.indexOf(Constants.DATA_TYPE_FILE_DATA) == 0) {
                    $scope.validation = null;
                    $scope.error = null;
                    if (!$scope.readOnly) {
                        ml +=   '<div class="twst-drag-n-drop-upload-area" twst-drop-target="catchFileUpload"> Drop a file here to upload ' +
                                '<twst-thumb-validation-icon validation="validation" error="error"></twst-thumb-validation-icon></div>';
                    } else {
                        ml += '<button class="twst-button twst-download-button">Download</button>';
                    }

                    $scope.downloadFile = function (fileData) {
                        var fileBlob = new Blob([fileData], {type: ""});
                        saveAs(fileBlob, $scope.itemData.fileName);
                    }
                    
                    $scope.catchFileUpload = function (data, error) {
                        if (error) {
                            $scope.validation = false;
                            $scope.error = error;
                            $scope.item.validData = 0;
                        } else {
                            if ($scope.itemData.fileType == 'quantification') {
                                /* check that filewriting was complete */
                                if (data.indexOf('##BLOCKS= 4' == 0)) {
                                    if (data.indexOf('Original Filename: ' + $scope.transformSpec.sources[0].details.id + ';') == -1) {
                                        $scope.validation = 0;
                                        $scope.error = 'The uploaded file is not quant data for plate #' + $scope.transformSpec.sources[0].details.id + '.';
                                    } else {
                                        $scope.validation = 1;
                                        $scope.error = null;
                                        $scope.transformSpec.details.requestedData[$scope.itemData.forProperty] = data;
                                        $scope.item.validData = true;
                                    }
                                } else {
                                    $scope.validation = 0;
                                    $scope.error = 'This uploaded file is incomplete or of an invalid type.';
                                }
                            }
                            
                        }
                    }

                } else if ($scope.itemData.type.indexOf(Constants.DATA_TYPE_TEXT) == 0) {
                    ml +=   '<p>' + $scope.itemData.type.data + '</p>';
                } else if ($scope.itemData.type.indexOf(Constants.DATA_TYPE_RADIO) == 0) {

                    $scope.validation = null;
                    $scope.error = null;

                    var options = $scope.itemData.data;

                    if (!$scope.readOnly) {

                        ml += '<div>';

                        for (var i=0; i < options.length; i++) {
                            ml +=   '<label><input type="radio" name="sequencerSelection" ng-mouseup="validate()" ng-model="transformSpec.details.requestedData[\'' + $scope.itemData.forProperty + '\']" value="' + options[i].option + '"> ' + (options[i].label ? options[i].label : options[i].option) + '</label>';
                        }

                        ml += '</div>';
                    } else {
                        ml += '<p><strong>' + $scope.transformSpec.details.requestedData[$scope.itemData.forProperty] + '</strong></p>';
                    }

                    $scope.validate = function (errorOnEmpty) {
                        $scope.item.validData = true;
                        $timeout(function () {
                            $scope.transformSpec.updateOperationsList(true)
                        }, 0);
                    }

                } else {
                    console.log('What? ' + $scope.itemData.type);
                }

                var el = angular.element(ml);
                compiler = $compile(el);
                element.append(el);
                compiler($scope);
            }
        };
    }
]);
