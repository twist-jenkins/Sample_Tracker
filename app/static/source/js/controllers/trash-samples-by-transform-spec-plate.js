angular.module('twist.app').controller('trashSamplesByTransformSpecPlateController', ['$scope', '$state', '$stateParams', 'Api', 'Maps',
    function ($scope, $state, $stateParams, Api, Maps) {
        $scope.plate_barcode = $stateParams.plate_barcode;
        $scope.setPlateBarcodeForEdit($scope.plate_barcode);

        $scope.selectedWellCount = 0;
        $scope.plateWellClicked = function (well) {
            if (well.highlighted) {
                $scope.selectedWellCount++;
            } else {
                $scope.selectedWellCount--;
            }
        };

        $scope.toggleSelectAll = function (forceNone) {
            if (forceNone || $scope.selectedWellCount == $scope.plate.wells.length) {
                //unselect all
                for (well in $scope.plate.wellMap) {
                    var well = $scope.plate.wellMap[well];
                    if (well.sampleId) {
                        well.highlighted = false;
                    }
                }
                $scope.selectedWellCount = 0;
            } else {
                //select all
                for (well in $scope.plate.wellMap) {
                    var well = $scope.plate.wellMap[well];
                    if (well.sampleId) {
                        well.highlighted = true;
                        $scope.plateWellClicked(well);
                    }
                }
                $scope.selectedWellCount = $scope.plate.wells.length;
            }
        };

        $scope.clearTrashSamplesErrorMessage = function () {
            $scope.trashSamplesErrorMessage = null;
            $scope.trashSamplesErrorMessageVisible = 0;
        }

        $scope.trashSelectedWells = function () {
            if ($scope.selectedWellCount && !$scope.trashingWells) {
                var trashIds = [];
                var trashedWells = [];

                for (well in $scope.plate.wellMap) {
                    var well = $scope.plate.wellMap[well];
                    if (well.highlighted) {
                        trashIds.push(well.sampleId);
                        trashedWells.push(well);
                    }
                }

                $scope.trashingWells = true;
                Api.trashSamples(trashIds).success(function (data) {
                    $scope.trashingWells = false;
                    $scope.toggleSelectAll(true);

                    $scope.trashSamplesErrorMessage = 'The selected samples have been trashed.';
                    $scope.trashSamplesErrorMessageVisible = 1;

                    for (var i=0; i<trashedWells.length;i++) {
                        trashedWells[i].trashed = true;
                    }
                }).error(function (data) {
                    $scope.trashingWells = false;
                    $scope.trashSamplesErrorMessage = 'Error trashing samples. Please try again.';
                    $scope.trashSamplesErrorMessageVisible = 11;
                });

                console.log(trashIds);
            }
        };

        $scope.loadingPlate = true;
        Api.getBasicPlateDetails($scope.plate_barcode).success(function (data) {
            $scope.loadingPlate = false;
            var thisPlate = new Maps.plateTemplates[data.plateDetails.type]();
            delete thisPlate.description;
            thisPlate.filledWellCount = data.wells.length;
            $.extend(thisPlate, data);

            for (var i=0; i< data.wells.length; i++) {
                var well = data.wells[i];
                thisPlate.addSampleId(well.column_and_row, well.sample_id);
            }
            thisPlate.plateDetails['barcode'] = $scope.plate_barcode;
            $scope.plate = thisPlate;
            console.log($scope.plate);
        }).error(function () {
            console.log('Error loading plate details.');
        });

        $scope.$on('$destroy', function () {
            $scope.setPlateBarcodeForEdit(null);
        });
    }]
)