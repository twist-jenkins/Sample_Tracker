var api_base_url = '/api/v1/';
var server_url = twist_api_url;

angular.module('twist.app').factory('Api',['ApiRequestObj', '$http',
    function (ApiRequestObj, $http) {

        return {
            getSampleTransferTypes: function () {
                var userReq = ApiRequestObj.getGet('sample-transfer-types');
                return $http(userReq);
            }
            ,getBarcodes: function () {
                var userReq = ApiRequestObj.getGet('sample-plate-barcodes');
                return $http(userReq);
            }
            ,getSamplePlatesList: function () {
                var plateListReq = ApiRequestObj.getGet('sample-plates-list');
                return $http(plateListReq);
            }
            ,getPlateInfo: function (plateId) {
                var plateListReq = ApiRequestObj.getGet('plate-info/' +  plateId);
                return $http(plateListReq);
            }
            ,updateBarcode: function (plateId, plateBarcode) {
                var updatePlateReq = ApiRequestObj.getPost('update-barcode');
                updatePlateReq.data = {
                    plateId: plateId
                    ,barcode: plateBarcode
                }
                return $http(updatePlateReq);
            }
            ,getPlateSteps: function () {
                var transfersReq = ApiRequestObj.getGet('sample-transfers');
                return $http(transfersReq);
            }
            ,getPlateDetails: function (barcode, format) {
                var plateDetailsReq = ApiRequestObj.getGet('plate-barcodes/' + barcode + (format ? '/' + format : ''));
                return $http(plateDetailsReq);
            }
            ,getBasicPlateDetails: function (barcode) {
                var plateDetailsReq = ApiRequestObj.getGet('basic-plate-info/' + barcode);
                return $http(plateDetailsReq);
            }
            ,getSourcePlateWellData: function (barcodes) {
                var wellDatasReq = ApiRequestObj.getPost('source-plate-well-data');
                wellDatasReq.data = {
                    plateBarcodes: barcodes
                }
                return $http(wellDatasReq);
            }
            ,checkDestinationPlatesAreNew: function (barcodes) {
                var checkReq = ApiRequestObj.getPost('check-plates-are-new');
                checkReq.data = {
                    plateBarcodes: barcodes
                }
                return $http(checkReq);
            }
            ,getTransformSpecs: function () {
                var transReq = ApiRequestObj.getGet('rest/transform-specs');
                return $http(transReq);
            }
            ,saveNewTransformSpec: function (planData) {
                var saveReq = ApiRequestObj.getPost('rest/transform-specs');
                saveReq.data = {
                    plan: planData
                }
                return $http(saveReq);
            }
            ,deleteTransformSpec: function (specId) {
                var deleteReq = ApiRequestObj.getDelete('rest/transform-specs/' + specId);
                return $http(deleteReq);
            }
            ,getTransformSpec: function (specId) {
                var specReq = ApiRequestObj.getGet('rest/transform-specs/' + specId);
                return $http(specReq);
            }
            ,executeTransformSpec: function (specId) {
                var executeReq = ApiRequestObj.getPut('rest/transform-specs/' + specId);
                executeReq.headers = {
                    'Transform-Execution': 'Immediate'
                }
                return $http(executeReq);
            }
            ,saveAndConditionallyExecuteTransformSpec: function (planData, executeNow) {
                var saveAndExReq = ApiRequestObj.getPost('rest/transform-specs');
                saveAndExReq.data = {
                    plan: planData
                }
                if (executeNow) {
                    saveAndExReq.headers = {
                        'Transform-Execution': 'Immediate'
                    }
                }
                return $http(saveAndExReq);
            }
            ,previewTransformation: function(sources, destinations, details ) {
                // kieran
                var preview = ApiRequestObj.getPost('transfer-preview');
                preview.data = {
                    sources: sources,
                    destinations: destinations,
                    details: details
                }
                return $http(preview);
            }

            //hamilton calls
            ,getHamiltonByBarcode: function (hamBarcode) {
                var hamReq = ApiRequestObj.getGet('rest-ham/hamiltons/' + hamBarcode);
                return $http(hamReq);
            }
            ,getCarrierByBarcode: function (carrierBarcode, hamBarcode) {
                var carrierReq = ApiRequestObj.getGet('rest-ham/hamiltons/' + hamBarcode + '/carriers/' + carrierBarcode);
                return $http(carrierReq);
            }
            ,confirmPlateReadyForTransform: function (plateBarcode, transformTypeId) {
                var plateReq = ApiRequestObj.getGet('rest-ham/hamilton-plates/' + plateBarcode + '/transform/' + transformTypeId);
                return $http(plateReq);
            }
            ,processHamiltonSources: function (plateBarcodes, transformTypeId) {
                var processReq = ApiRequestObj.getPost('rest-ham/hamilton-plates/transform/' + transformTypeId);
                processReq.data = {
                    plateBarcodes: plateBarcodes
                }
                return $http(processReq);
            }
            ,trashSamples: function (sampleIds) {
                var trashReq = ApiRequestObj.getPost('rest-ham/trash-samples');
                trashReq.data = {
                    sampleIds: sampleIds
                }
                return $http(trashReq);
            }
            ,getServerDateTime: function () {
                var trashReq = ApiRequestObj.getPost('get-date-time');
                return $http(trashReq);
            }
        };
    }]
);
