angular.module('twist.app').controller('hamiltonWizardSourceScanController', ['$scope', '$state',  '$http', 'Api', '$timeout', 'Constants',
    function ($scope, $state, $http, Api, $timeout, Constants) {
        $scope.findNextPlateForScan(Constants.PLATE_SOURCE, Constants.HAMILTON_ELEMENT_CARRIER_POSITION);

        $scope.restartSourcePlateScan = function () {
            for (var i=0; i<$scope.hamiltonDataObj.allSourcePlates.length;i++) {
                var plate = $scope.hamiltonDataObj.allSourcePlates[i];
                plate.barcode = null;
                plate.positionScanned = null;
            }
            $scope.findNextPlateForScan(Constants.PLATE_SOURCE, Constants.HAMILTON_ELEMENT_CARRIER_POSITION);
        };

        $scope.sourcePlateScanComplete = function () {
            $scope.safeBarcodeInputBlur();
            if ($scope.scannedSourcePlateCount && !$scope.processingSources) {

                /* TODO: api call to submit source plates and get # of destination plates        */

                var scannedPlateBarcodes = [];

                for (var i=0; i<$scope.hamiltonDataObj.allSourcePlates.length;i++) {
                    var plate = $scope.hamiltonDataObj.allSourcePlates[i];
                    if (plate.barcode) {
                        scannedPlateBarcodes.push(plate.barcode);
                    } else {
                        plate.unused = true;
                    }
                }

                $scope.processingSources = true;

                Api.processHamiltonSources(scannedPlateBarcodes, $scope.transformSpec.details.transform_type_id).success(function (data) {
                    console.log(data);
                    $scope.processingSources = false;
                    var responseCommands =  data.responseCommands;

                    if (!responseCommands.length) {
                        $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.destination_scan');
                    } else {

                        for (var i=0; i< responseCommands.length; i++) {
                            var command = responseCommands[i];

                            var commandType = command.type

                            switch (commandType) {
                                case Constants.RESPONSE_COMMANDS_SET_DESTINATIONS:


                                    /* the backend responds with the total destinations in a single list
                                    *  which does NOT take into account skipped carriers or unused carrier positions
                                    *  thus we need to set destinations only in used positions on non-skipped carriers
                                    */

                                    var destPlateCount = command.plates.length;

                                    outerLoop:
                                        for (var j=0; j<destPlateCount; j++) {
                                            var setPlate = command.plates[j];
                                            innerLoop: 
                                                for (var h=0; h<$scope.hamiltonDataObj.allDestinationPlates.length;h++) {
                                                    var destPlate = $scope.hamiltonDataObj.allDestinationPlates[h];
                                                    if (!destPlate.carrier.scanSkipped && !destPlate.unused && !destPlate.set) {
                                                        destPlate.optional = false;
                                                        destPlate.set = true;
                                                        break innerLoop;
                                                    } 
                                                }

                                        }

                                    /* there may be fewer set destinations than possible destinations
                                    *  so loop through all destinations and set any unset destination to usused
                                    */

                                    for (var h=0; h<$scope.hamiltonDataObj.allDestinationPlates.length;h++) {
                                        var destPlate = $scope.hamiltonDataObj.allDestinationPlates[h];
                                        if (!destPlate.set) {
                                            destPlate.unused = true;
                                        }
                                    }

                                    $scope.setDestinationPlatesNeedingScanCount(destPlateCount);
                                    
                                    break;
                                case Constants.RESPONSE_COMMANDS_ADD_TRANSFORM_SPEC_DETAIL:
                                    $scope.transformSpec.details[command.detail.key] = command.detail.value;
                                    break;
                                default :
                                    console.log('Error: Unrecognized command type = [' + command.type + ']');
                                    break;
                            }
                        }

                        switch ($scope.transformSpec.details.transform_type_id) {
                            case 9:
                            case 39:
                            case 48:
                            case 72:
                                $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.destination_scan');
                                break;
                            case 51:
                                $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.label_destination_tubes');
                                break;
                            case 58:
                            case 70:
                                $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.destination_placement_and_scan');
                                break;
                            default:
                                console.log('Unexpected transform_type_id = [' + $scope.transformSpec.details.transform_type_id + ']');
                                break;

                        }

                    }

                }).error(function (error) {
                    $scope.processingSources = false;
                    $scope.clearScannedItemErrorMessage();
                    $scope.showScannedItemErrorMessage('There was an error processing these sources. Please try again.');
                });
            }
        };
    }]
);
