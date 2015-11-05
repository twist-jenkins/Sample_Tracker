app = angular.module("twist.app")

.directive('twistHeader', [ 
    function() {
        return {
            restrict: 'E'
            ,templateUrl: 'twist-header.html'
            , controller: ['$scope', 
                function ($scope) {
                    //...
                }
            ]
        };
    }
])

.directive('twistMainNav', [ 
    function() {
        return {
            restrict: 'E'
            ,templateUrl: 'twist-main-nav.html'
            ,controller: ['$scope', 
                function ($scope) {
                    $scope.navItems = [
                        {text: 'Record Step', link: 'root.record_step'}
                        ,{text: 'Plate Details', link: 'root.plate_details'}
                        ,{text: 'Edit Plate Barcode', link: 'root.edit_barcode'}
                        ,{text: 'Transform Specs', link: 'root.transform_specs.view_manage', match: 'root.transform_specs'}
                        ,{text: 'View Steps', link: 'root.view_steps'} 
                        ,{text: 'Sample Details', link: 'root.sample_details'}
                    ];
                }
            ]
        };
    }
])

.directive('twstSpinner', ['$interval',  
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
])

.directive('twstThumbValidationIcon', ['$sce', 
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
])

.directive('twstMessage', ['$sce',  
    function($sce) {
        return {
            restrict: 'E'
            ,scope: {
                message: '='
                ,visibleAndValid: '='
            }
            ,template: '<div class="twst-message" ng-class="{\'twst-message-visible\':visibleAndValid, \'twst-success\': visibleAndValid > 0, \'twst-error\': visibleAndValid < 0}"><span class="twst-message-text" ng-bind-html="message"></span></div>'
        };
    }
])

.directive('twstCustomRadio', [ 
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
])

.directive('twstDropTarget', [ 
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
                        } else {
                            $scope.twstDropTarget({}, 'Unrecognized upload file type: ' + f.type);
                            $scope.$apply(); // must call manually since the onload event is not angularized
                        }
                        
                    });
                }
            ]
        };
    }
])

.directive('twstTransformBuilderForm', [ 
    function() {
        return {
            restrict: 'E'
            ,scope: {
                transformSpec: '='
                ,templateTypeSelection: '=?'
            }
            ,templateUrl: 'twist-transform-builder-form.html'
            ,controller: ['$scope', '$element', '$sce', '$timeout', 'Formatter', 'TypeAhead', 'Maps', 'Constants', 'TransformBuilder', 'FileParser', 
                function ($scope, $element, $sce, $timeout, Formatter, TypeAhead, Maps, Constants, TransformBuilder, FileParser) {

                    $scope.getTypeAheadBarcodes = TypeAhead.getTypeAheadBarcodes;

                    $scope.excelFileStats = {};
                    $scope.fileErrors = [];

                    $scope.Constants = Constants;

                    $scope.cachedFileData = null;

                    /* refresh the current transfer plan based on changes to plates inputs or upload file */
                    $scope.updateTransferPlan = function (val, which, itemIndex) {
                        if (val.length > 5) {
                            if (which == Constants.PLATE_SOURCE) {
                                $scope.transformSpec.addSource(itemIndex);
                            } else if (which == Constants.PLATE_DESTINATION) {
                                $scope.transformSpec.addDestination(itemIndex);
                            }
                        } else {
                            if (which == Constants.PLATE_SOURCE) {
                                $scope.transformSpec.checkSourcesReady();
                            } else if (which == Constants.PLATE_DESTINATION) {
                                $scope.transformSpec.checkDestinationsReady();
                            }
                        }
                    };

                    $scope.$watch('templateTypeSelection', function (newVal, oldVal) {
                        if (newVal == Constants.FILE_UPLOAD && $scope.cachedFileData) {
                            $scope.catchFile();
                        } else if (newVal == Constants.STANDARD_TEMPLATE) {
                            $scope.transformSpec.transferFromFile(false);
                        }
                    });

                    $scope.clearExcelUploadData = function () {
                        $scope.excelFileStats = {};
                        $scope.fileErrors = [];
                    };

                    $scope.catchFile = function (fileData, error) {
                        $scope.parsingFile = true;

                        if (error) {
                            $scope.clearExcelUploadData();
                            $scope.fileErrors.push(error);
                            $scope.excelFileStats = {};
                            $scope.transformSpec.clearOperationsList();
                            $scope.parsingFile = false;
                        } else {
                            // called in timeout to give the spinner time to render
                            $timeout(function () {
                                $scope.clearExcelUploadData();

                                if (!fileData) {
                                    fileData = $scope.cachedFileData;
                                } else {
                                    $scope.cachedFileData = fileData;
                                };

                                FileParser.getTransferRowsFromFile(fileData, $scope.transformSpec).then(function (resultData) {
                                    $scope.excelFileStats = resultData.stats;
                                    $scope.fileErrors = resultData.errors;

                                    if (!resultData.errors.length) {
                                        $scope.transformSpec.transferFromFile(true, resultData);
                                    } else {
                                        $scope.transformSpec.clearOperationsList();
                                    } 

                                    $scope.parsingFile = false;

                                }, function (errorData) {
                                    $scope.fileErrors = 'Error: Unknown error while parsing this file.';
                                    $scope.parsingFile = false;
                                });
                 
                            }, 150);
                        }
                    };

                }
            ]
        };
    }
])

;