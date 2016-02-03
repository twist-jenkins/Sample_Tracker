app = angular.module("twist.app")

.directive('twistHeader', [ 
    function() {
        return {
            restrict: 'E'
            ,templateUrl: 'twist-header.html'
            , controller: ['$scope', 'localStorageService', 
                function ($scope, localStorageService) {
                    $scope.logout = function () {
                        localStorageService.remove('loginTarget');
                        document.location.href = '/logout';
                    }
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
                        {text: 'Record Transform', link: 'root.record_transform'}
                        ,{text: 'Plate Details', link: 'root.plate_details'}
                        ,{text: 'Edit Plate Barcode', link: 'root.edit_barcode'}
                        ,{text: 'Transform Specs', link: 'root.transform_specs.view_manage', match: 'root.transform_specs'}
                        ,{text: 'View Steps', link: 'root.view_steps'} 
                        ,{text: 'Sample Details', link: 'root.sample_details'}
                        ,{text: 'Trash Samples', link: 'root.trash_samples'}
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

.directive('twstMessage', ['$sce', '$timeout',  
    function($sce, $timeout) {
        return {
            restrict: 'E'
            ,scope: {
                message: '='
                ,visibleAndValid: '='
                ,clearParentData: '='
            }
            ,template: '<div class="twst-message" ng-class="{\'twst-message-visible\':visibleAndValid, \'twst-success\': visibleAndValid > 0, \'twst-error\': visibleAndValid < 0}"><span class="twst-message-text" ng-bind-html="message"></span></div>'
            ,controller: ['$scope', '$element',    
                function($scope, $element) {
                    $scope.$watch('visibleAndValid', function(newValue, oldValue) {
                        if (newValue != 0) {
                            $timeout(function () {
                                $scope.visibleAndValid = 0;
                                $timeout(function () {
                                    if ($scope.clearParentData) {
                                        $scope.clearParentData();
                                    }
                                }, 800);
                            }, 5000);
                        };
                    }) 
                }
            ]
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
])

.directive('twstDragOutLink', [ 
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
])

.directive('barcodeSvg', [ 
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
])

.directive('viewBox', [ 
    function() {
        return {
            scope: {
                plate: '='
            }
            ,restrict: 'A'
            ,link: function($scope, element, attrs) {
                var getViewBox = function () {
                    return "0 0 " + ($scope.plate.rowLength*30 + 8*$scope.plate.rowLength + 56) + ' ' + ($scope.plate.wellCount/$scope.plate.rowLength*30 + 8*$scope.plate.wellCount/$scope.plate.rowLength + 56);
                }
                element.get(0).setAttribute("viewBox", getViewBox());
            }
        };
    }
])

.directive('plateView', [ 
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
])

.directive('twstHamiltonWizardThumbsUpMedallion', ['$timeout',  
    function($timeout) {
        return {
            scope: {
                fadeFinish: '='
                ,thumbsUpIndex: '='
            }
            ,restrict: 'A'
            ,template: '<div class="twst-hamilton-wizard-thumbs-up-medallion-inner"><twst-thumb-validation-icon validation="1" error="0"></twst-thumb-validation-icon></div>'
            ,link: function($scope, element, attrs) {
                element.addClass('twst-hamilton-wizard-thumbs-up-medallion');
                $timeout(function () {
                    element.addClass('twst-hamilton-wizard-thumbs-up-medallion-rise');
                }, 0);

                var fader = $timeout(function () {
                    element.addClass('twst-hamilton-wizard-thumbs-up-transparent');
                    $timeout(function () {
                        $scope.fadeFinish($scope.thumbsUpIndex);
                    }, 200);
                }, 400);

                element.on('$destroy', function() {
                  $timeout.cancel(fader);
                });
            }
        };
    }
])

.directive('twstTransformSpecDataPresentationItem', ['$compile', 'Constants',   
    function($compile, Constants) {
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
                    ml += '<h4>{{itemData.title}}</h4>';
                }

                switch ($scope.itemData.type) {
                    case Constants.DATA_TYPE_TEXT:
                        ml += '<p>{{itemData.data}}</p>';
                        break;
                    case Constants.DATA_TYPE_FILE_DATA:
                        // assemble the presented data
                        ml += '<button class="twst-button twst-download-button" ng-click="sendFile(itemData.data)"><div class="twst-button-icon"><ng-include src="\'static/images/download.svg\'"></ng-include></div>&nbsp;Download</button>';
                        break;
                    case Constants.DATA_TYPE_LINK:
                        // assemble the presented data
                        ml += '<a ng-href="{{itemData.data}}" target="_blank">{{itemData.data}}</a>';
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
])

.directive('twstTransformSpecDataRequestItem', ['$compile', 'Constants', '$timeout',   
    function($compile, Constants, $timeout) {
        return {
            scope: {
                transformSpec: '='
                ,item: '='
            }
            ,restrict: 'E'
            ,link: function($scope, element, attrs) {

                console.log($scope.transformSpec);

                var ml = '';

                $scope.itemData = $scope.item.item;

                /* IMPORTANT $scope.item.validData **MUST** be set true or false whenever input item data changes
                * (truthy & false-y values work too - so the initial value of 'undefined' works to start)
                *  $scope.item.validData for each requested data item will be checked to see
                *  if the submit transform button should be enabled
                */

                if (! $scope.transformSpec.details.requestedData) {
                    $scope.transformSpec.details.requestedData = {};
                }

                if ($scope.itemData.title) {
                    ml += '<h4>{{itemData.title}}</h4>';
                }

                if ($scope.itemData.type.indexOf(Constants.DATA_TYPE_ARRAY) == 0) {

                    var arrayCount = $scope.itemData.type.split('.')[1];

                    $scope.transformSpec.details.requestedData[$scope.itemData.forProperty] = new Array(4);

                    $scope.validations = new Array(4);
                    $scope.errors = new Array(4);

                    for (var i=0; i < arrayCount; i++) {
                        ml +=   '<p>' +
                                    '<input type="text" class="form-control" ng-model="transformSpec.details.requestedData[\'' + $scope.itemData.forProperty + '\'][' + i + ']" ng-change="validate(' + i + ', true);"/>' +
                                    '<twst-thumb-validation-icon validation="validations[' + i + ']" error="errors[' + i + ']"></twst-thumb-validation-icon>' +
                                '</p>';
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
                                        var allVals = $scope.transformSpec.details.requestedData[$scope.itemData.forProperty].join('|');
                                        if (allVals.indexOf(val) != allVals.lastIndexOf(val)) {
                                            $scope.validations[arrInd] = false;
                                            $scope.errors[arrInd] = 'This barcode has already been entered.';
                                        } else {
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
                    ml +=   '<input type="text" class="form-control" ng-model="transformSpec.details.requestedData[\'' + $scope.itemData.forProperty + '\']" ng-change="validate(true);"/>' +
                            '<twst-thumb-validation-icon validation="validation" error="error"></twst-thumb-validation-icon>';


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
                            }
                        }

                        $timeout.cancel($scope.validationTimeout);
                        $scope.validationTimeout = $timeout(returnValidate(), 200);
                    }

                } else if ($scope.itemData.type.indexOf(Constants.DATA_TYPE_FILE_DATA) == 0) {
                    $scope.validation = null;
                    $scope.error = null;
                    ml +=   '<div class="twst-drag-n-drop-upload-area" twst-drop-target="catchFileUpload"> Drop a file here to upload ' +
                            '<twst-thumb-validation-icon validation="validation" error="error"></twst-thumb-validation-icon></div>';
                    
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
])

;