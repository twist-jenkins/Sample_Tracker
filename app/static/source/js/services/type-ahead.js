var api_base_url = '/api/v1/';
var server_url = twist_api_url;

angular.module('twist.app').factory('TypeAhead', ['Api',
    function (Api) {
        return {
            getTypeAheadBarcodes: function (queryText) {

                return Api.getBarcodes(queryText).then(function (resp) {
                    queryText = queryText.toLowerCase();

                    var goodData = [];

                    for (var i=0; i< resp.data.length ;i++) {
                        if (resp.data[i].toLowerCase().indexOf(queryText) != -1) {
                            goodData.push(resp.data[i]);
                        }
                    }
                    return goodData;
                });
            }
            ,getTypeAheadPlateIds: function (queryText) {
                return Api.getSamplePlatesList(queryText).then(function (resp) {
                    queryText = queryText.toLowerCase();

                    var goodData = [];

                    for (var i=0; i< resp.data.length ;i++) {
                        if (resp.data[i].toLowerCase().indexOf(queryText) != -1) {
                            goodData.push(resp.data[i]);
                        }
                    }
                    return goodData;
                });
            }
            ,getTransformSpecIds: function (queryText) {
                return Api.getTransformSpecs(queryText).then(function (resp) {
                    queryText = queryText.toLowerCase();

                    var goodData = [];
                    for (var i=0; i< resp.data.data.length ;i++) {
                        var specId = resp.data.data[i].spec_id + '';
                        if (specId.toLowerCase().indexOf(queryText) != -1) {
                            goodData.push(specId);
                        }
                    }
                    return goodData;
                });
            }
        };
    }]
);
