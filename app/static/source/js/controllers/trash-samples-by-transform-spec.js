angular.module('twist.app').controller('trashSamplesByTransformSpecController', ['$scope', '$state', '$stateParams', 'Api',
    function ($scope, $state, $stateParams, Api) {
        $scope.spec_id = $stateParams.spec_id;

        $scope.openTrashPlateEditor = function (plateBarcode) {
            $scope.setPlateBarcodeForEdit(plateBarcode);
            $state.go('root.trash_samples.by_transform_spec.for_plate', {
                plate_barcode: plateBarcode
            });
        }

        $scope.setPlateBarcodeForEdit = function (plateBarcode) {
            $scope.plateBarcodeForEdit = plateBarcode;
        };

        $scope.backToSpec = function () {
            $state.go('root.trash_samples.by_transform_spec', {
                spec_id: $scope.spec_id
            });
        };

        $scope.specLoading = true;
        Api.getTransformSpec($scope.spec_id).success(function (data) {
            $scope.specLoading = false;
            var thisSpec = data.data;
            thisSpec.plan = thisSpec.data_json;
            $scope.selectedSpec = thisSpec;
            $scope.executedDateString = (new Date($scope.selectedSpec.date_executed)).toLocaleString();
            console.log($scope.selectedSpec);
        }).error(function () {
            console.log('Error loading spec.');
        });
    }]
)
