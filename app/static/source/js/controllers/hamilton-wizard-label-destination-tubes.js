angular.module('twist.app').controller('hamiltonWizardLabelDestinationTubesController', ['$scope', '$state',  '$http', 'Api', '$timeout', 'Constants',
    function ($scope, $state, $http, Api, $timeout, Constants) {
        $scope.setCurrentStepInstruction('Print and apply barcodes');
        $scope.setHighlightedPlate(null, null, true, true);
        $scope.safeBarcodeInputBlur();

        $scope.setTubeBarcodesFileDownloaded = function (val) {

            var columnTitles = [
                'COI'
                ,'itemName'
                ,'partNumber'
                ,'labelMass'
            ]

            var csvContents = columnTitles.join(',') + '\n';

            var shippingTubeBarcodeData = $scope.transformSpec.details.shippingTubeBarcodeData;

            for(var i = 0; i < shippingTubeBarcodeData.length; i++) {
                row = shippingTubeBarcodeData[i];
                var line = '';
                for (var j=0; j<columnTitles.length; j++) {
                    line += (j ? ',' : '') + row[columnTitles[j]]
                }
                csvContents += line + '\n';
            }

            var csvBlob = new Blob([csvContents], {type: "text/csv"});

            saveAs(csvBlob, "tube_barcodes.csv");

            $scope.tubeBarcodesFileDownloaded = val;
        }

        $scope.tubesLabeled = function () {
            if ($scope.tubeBarcodesFileDownloaded) {
                $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.destination_tubes_scan');
            }
        }
    }]
);
