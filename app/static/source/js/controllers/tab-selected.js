angular.module('twist.app').controller('tabSelectedController', ['$scope', '$state', '$stateParams', '$element', '$sce', '$timeout', 'Formatter', 'TypeAhead', 'Maps', 'Constants', 'TransformBuilder', 'FileParser',
    function ($scope, $state, $stateParams, $element, $sce, $timeout, Formatter, TypeAhead, Maps, Constants, TransformBuilder, FileParser) {

        $scope.getTypeAheadBarcodes = TypeAhead.getTypeAheadBarcodes;

        $scope.excelFileStats = {};
        $scope.fileErrors = [];

        $scope.Constants = Constants;

        $scope.cachedFileData = null;

        /* refresh the current transform plan based on changes to plates inputs or upload file */
        $scope.updateTransformPlan = function (val, which, itemIndex) {
            if (val && val.length > 5) {

                /* prevent a source or destination from being entered more than once */
                if (checkDupeBarcode(val, which)) {
                    $scope.transformSpec.notReady(which);
                    var errMsg = 'A plate with barcode <strong>' + val + '</strong> is already a ' + which + ' plate.';
                    if (which == Constants.PLATE_SOURCE) {
                        $scope.transformSpec.sources[itemIndex].error = errMsg
                    } else if (which == Constants.PLATE_DESTINATION) {
                        $scope.transformSpec.destinations[itemIndex].error = errMsg;
                    }
                } else {
                    if (which == Constants.PLATE_SOURCE) {
                        $scope.transformSpec.addSource(itemIndex);
                    } else if (which == Constants.PLATE_DESTINATION) {
                        $scope.transformSpec.addDestination(itemIndex);
                    }
                }

            } else {
                if (which == Constants.PLATE_SOURCE) {
                    $scope.transformSpec.checkSourcesReady(true);
                } else if (which == Constants.PLATE_DESTINATION) {
                    $scope.transformSpec.checkDestinationsReady(true);
                }
            }
        };

        $scope.$watch('templateTypeSelection', function (newVal, oldVal) {
            if (newVal == Constants.FILE_UPLOAD && $scope.cachedFileData) {
                $scope.catchFile();
            } else if (newVal == Constants.STANDARD_TEMPLATE) {
                $scope.transformSpec.transformFromFile(false);
            }
        });

        /* not necessarily the most elegant code but it works for updating the UI when
         *  the responseCommand data items are changed */

        $scope.$watch('transformSpec.presentedDataItems.length', function (newVal, oldVal) {
            if (newVal) {
                $scope.setShowPresentedRequestedData(true);
            }
        });

        $scope.$watch('transformSpec.requestedDataItems.length', function (newVal, oldVal) {
            if (newVal) {
                $scope.setShowPresentedRequestedData(true);
            }
        });

        var checkDupeBarcode = function (barcode, which) {
            var plateArray = [];
            if (which == Constants.PLATE_SOURCE) {
                plateArray = $scope.transformSpec.sources;
            } else if (which == Constants.PLATE_DESTINATION) {
                plateArray = $scope.transformSpec.destinations;
            }
            var alreadyFound = false;
            for (var i=0; i< plateArray.length; i++) {
                var plate = plateArray[i];
                if (plate.details.id == barcode) {
                    if (alreadyFound) {
                        return true;
                    } else {
                        alreadyFound = true;
                    }
                }
            }
            return false;
        }

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

                    FileParser.getTransformRowsFromFile(fileData, $scope.transformSpec).then(function (resultData) {
                        $scope.excelFileStats = resultData.stats;
                        $scope.fileErrors = resultData.errors;

                        if (!resultData.errors.length) {
                            $scope.transformSpec.transformFromFile(true, resultData);
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

        $scope.startHamiltonSteps = function () {
            $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_select');
        }

        $scope.setSelectedHamilton = function (hamilton) {
            $scope.selectedHamilton = hamilton;
        }

        $scope.hamiltonThumbsUp = [];
        $scope.now = new Date();

        $scope.flashHamiltonThumbsUp = function () {
            $scope.hamiltonThumbsUp.push({id: $scope.now.toString(), index: $scope.hamiltonThumbsUp.length});
        };

        $scope.finishHamiltonThumbsUpFade = function (thumbsUp) {
            $scope.hamiltonThumbsUp.splice(thumbsUp.index, 1);
        }

        $scope.selected_tab = $stateParams.selected_tab;
        $scope.setTransformTemplate($scope.selected_tab);
    }]
)
