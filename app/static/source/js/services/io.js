var api_base_url = '/api/v1/';
var server_url = twist_api_url;

angular.module('twist.app').factory('Io', ['Api', '$q',  
    function (Api, $q) {

        /* fetches are promises that get resolved each time the fetchCount for a given type goes to zero */
        /* a new promise is created whenever a fetchcount  gores from 0 to 1 */
        var fetches = {
            plate: $q.defer()
            ,specPreview: $q.defer()
            ,spec: $q.defer()
        };

        /* start is a resolved state for the deferred fetches above */
        for (fetch in fetches) {
            fetches[fetch].resolve({});
        }

        var fetchCount = {
            plate: 0
            ,specPreview: 0
            ,spec: 0
        }

        /* thenCounts track how many deferred requests are waiting or other types to finish (using the whenReady method below) */
        var thenCounts = {
            plate: 0
            ,specPreview: 0
            ,spec: 0
        }

        /* NOTE: The code will dynamically create fetches and count vars for for types that aren't spec'd above */

        var start = function (what) {
            if (!fetchCount[what]) {
                fetches[what] = $q.defer();
            }
            fetchCount[what]++
        }

        var finish = function (what) {
            fetchCount[what]--;
            if (!fetchCount[what]) {
                fetches[what].resolve();
            }
        }

        return {
            /* when a given IO promise resolves, then execute the supplied function */
            /* once = true will set a maximum of one function to execute at resolution */
            whenReady: function (what, thenDo, once) {
                if (!thenCounts[what] || !once) {
                    thenCounts[what]++;
                    fetches[what].promise.then(function (data) {
                        thenCounts[what]--;
                        thenDo();
                    });
                } else {
                    console.log('');
                }
            }
            ,getSourcePlate: function (barcode, fullDetails) {

                var plateDetailsFetcher = fullDetails ? Api.getPlateDetail : Api.getBasicPlateDetails;

                start('plate');
                var fetch = plateDetailsFetcher(barcode);

                fetch.success(function (data) {
                    finish('plate');
                }).error(function (data) {
                    finish('plate');
                });

                return fetch;

            }
            ,checkDestinations: function (barcodeArray) {
                start('plate');
                var fetch = checkDestinationPlatesAreNew(barcodeArray);

                fetch.success(function (data) {
                    finish('plate');
                }).error(function (data) {
                    finish('plate');
                });

                return fetch;
            }

        };
    }]
);