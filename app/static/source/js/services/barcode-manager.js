var api_base_url = '/api/v1/';
var server_url = twist_api_url;

angular.module('twist.app').factory('BarcodeManager', ['Constants', 
    function (Constants) {

        var barcodePrefixes = {
            'p': Constants.BARCODE_TYPE_PLATE
            ,'i': Constants.BARCODE_TYPE_INSTRUMENT
            ,'c': Constants.BARCODE_TYPE_CARRIER
        };

        var instruments = {
            'iHAM04': Constants.INSTRUMENT_TYPE_HAMILTON
        };

        var carriers = {

        };

        return {
            validateType: function (barcode, expectedType) {
                if (barcodePrefixes[barcode.charAt(0)] == expectedType) {
                    return true;
                }
                return false;
            }
            ,validateInstrument: function (barcode, expectedInstrumentType) {
                if (instruments[barcode] == expectedInstrumentType) {
                    return true
                }
                return false;
            }
        };
    }
]);
