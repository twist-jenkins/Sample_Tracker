angular.module('twist.app').controller('editBarcodeController', ['$scope', '$state',  '$http', 'Api', '$timeout', 'TypeAhead',
    function ($scope, $state, $http, Api, $timeout, TypeAhead) {

        $scope.getTypeAheadPlateIds = TypeAhead.getTypeAheadPlateIds;

        $scope.plateInfoEntered = function () {
            if ($scope.plateId && $scope.plateId.length > 1) {
                $state.go('root.edit_barcode.plate_selected', {
                    selected_plate_id: $scope.plateId
                });
            }
        };

        $scope.getPlateInfo = function (plateId) {
            $scope.plateId = plateId;
            $scope.fetchingPlateForBarcodeEdit = true;
            Api.getPlateInfo($scope.plateId).then(function (resp) {
                $scope.fetchingPlateForBarcodeEdit = false;
                $scope.selectedPlate = resp.data;
                $scope.currentBarcode = $scope.selectedPlate.externalBarcode + '';
            });
        }

        $scope.plateInfoKeypress = function ($event) {
            if ($event.keyCode == 13) {
                $scope.plateInfoEntered();
            }
        };

        $scope.updateBarcode = function () {
            if ($scope.currentBarcode != $scope.selectedPlate.externalBarcode && $scope.selectedPlate.externalBarcode && $scope.selectedPlate.externalBarcode.length > 5) {

                $scope.updatingBarcode = true;

                Api.updateBarcode($scope.selectedPlate.sample_plate_id, $scope.selectedPlate.externalBarcode).success(function (data) {
                    if (data.success) {
                        $scope.updatingBarcode = false;
                        $scope.submissionResultMessage = 'The barcode for plate <span class="twst-step-text">' + $scope.selectedPlate.sample_plate_id + '</span> has been updated to <span class="twst-step-text">' + $scope.selectedPlate.externalBarcode + '</span>.';
                        $scope.submissionResultVisible = 1;
                        $scope.clearForm();
                    } else {
                        $scope.submissionResultMessage = 'Error: ' + data.errorMessage + '.';
                        $scope.submissionResultVisible = -1;
                        $scope.updatingBarcode = false;
                    }

                    $timeout(function () {
                        $scope.submissionResultVisible = 0;
                        $timeout(function () {
                            $scope.submissionResultMessage = null;
                        }, 400);
                    }, 5000);
                });
            }
        }

        $scope.barcodeChanged = function () {
            if (!$scope.selectedPlate) {
                return false
            } else {
                return $scope.currentBarcode != $scope.selectedPlate.externalBarcode && $scope.selectedPlate.externalBarcode && $scope.selectedPlate.externalBarcode.length > 5;
            }
        }

        $scope.clearForm = function () {
            $scope.plateId = null;
            $scope.selectedPlate = null;
            $scope.currentBarcode = null;
            $state.go('root.edit_barcode');
        }
    }]
);
