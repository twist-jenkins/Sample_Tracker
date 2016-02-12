angular.module('twist.app').controller('hamiltonWizardCarrierScanController', ['$scope', '$state',  '$http', 'Api', '$timeout',
    function ($scope, $state, $http, Api, $timeout) {
        $scope.findNextCarrierForScan();
        $scope.restartCarrierScan = function () {
            for (var i=0; i<$scope.hamiltonDataObj.allCarriers.length;i++) {
                var carrier = $scope.hamiltonDataObj.allCarriers[i];
                carrier.barcode = null;
                carrier.scanSkipped = null;
            }
            $scope.findNextCarrierForScan();
        }

        $scope.skipCurrentCarrierScan = function () {

            var whichKind = '';

            for (var j=0; j<$scope.highlightedCarrier.plates.length; j++) {
                if (whichKind = $scope.highlightedCarrier.plates[j].plateFor) {
                    break;
                }
            }

            if (whichKind != '') {

                var scannedCarrierOfWhichKindCount = 0;
                var carriersLeftOfWhichKindCount = 0;
                /* we have to have at least 1 source and 1 destination carrier */
                for (var i=0; i<$scope.hamiltonDataObj.allCarriers.length;i++) {
                    var carrier = $scope.hamiltonDataObj.allCarriers[i];
                    // skip the current carrier
                    if ($scope.highlightedCarrier.index != carrier.index) {
                        if (carrier.plates[0].plateFor == whichKind) {
                            if (carrier.barcode) {
                                scannedCarrierOfWhichKindCount++;
                            } else if (carrier.index > $scope.highlightedCarrier.index) {
                                carriersLeftOfWhichKindCount++;
                            }
                        }
                    }
                }

                if (!scannedCarrierOfWhichKindCount && !carriersLeftOfWhichKindCount) {
                    $scope.showScannedItemErrorMessage('You must scan <strong>at least one ' + whichKind + ' carrier</strong>.');
                    $scope.setHighlightedCarrier($scope.highlightedCarrier);
                } else {
                    $scope.highlightedCarrier.scanSkipped = true;
                    for (var j=0; j<$scope.highlightedCarrier.plates.length; j++) {
                        $scope.highlightedCarrier.plates[j].unused = true;
                    }
                    $scope.findNextCarrierForScan();
                }

            } else {
                console.log('Highlighted carrier has no used plates.');
            }
        }
    }]
);
