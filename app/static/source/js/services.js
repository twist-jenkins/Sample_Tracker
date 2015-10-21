var app, server_url, api_base_url;

api_base_url = '/api/v1/';
server_url = twist_api_url;

app = angular.module('twist.app')


.factory('ApiRequestObj', [
    function () {

        var newRequest = function(version) {
            var api_base = api_base_url;
            if (version) {
                api_base = 'api/' + version + '/';
            }
            return {
                url: server_url + api_base,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            };
        };

        var getRequest = function (method, apiPath, version) {
            var request = newRequest(version);
            request.method = method;
            request.url += apiPath;
            return request;
        };

        return {
            getGet: function (apiPath, version) {
                return getRequest('GET', apiPath, version);
            }
            ,getPost: function (apiPath, version) {
                return getRequest('POST', apiPath, version);
            }
            ,getDelete: function (apiPath, version) {
                return getRequest('DELETE', apiPath, version);
            }
            ,getPut: function (apiPath, version) {
                return getRequest('PUT', apiPath, version);
            }
        };
    }
])

.factory('User',['ApiRequestObj', '$http',
    function (ApiRequestObj, $http) {

        return {
            init: function () {

                var base = this;

                var userReq = ApiRequestObj.getGet('user');

                var resp = $http(userReq);

                resp.success(function (respData) {
                    base.data = respData.user;
                });

                return resp;
            }
        };
    }]
)

.factory('Api',['ApiRequestObj', '$http',
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
            ,submitSampleStep: function (data) {
                var submitReq = ApiRequestObj.getPost('track-sample-step');
                submitReq.data = data;
                return $http(submitReq);
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
                var plateDetailsReq = ApiRequestObj.getGet('plate_barcodes/' + barcode + (format ? '/' + format : ''));
                return $http(plateDetailsReq);
            }
        };
    }]
)

.factory('Formatter', [
    function () {

        var alphaNumeric = 'abcdefghijklmnopqrstuvwxyz0123456789';

        var stripNonAlphaNumeric = function (inString, dashOk, replaceWithSpace) {

            var okChars = alphaNumeric;
            if (dashOk) {
                okChars += '-';
            }

            var outString = inString;
            if (inString != null) {
                outString = '';
                inString = inString.toLowerCase();
                for (var i=0; i<inString.length;i++) {
                    var thisChar = inString.charAt(i);
                    if (okChars.indexOf(thisChar) != -1) {
                        outString += thisChar;
                    } else if (replaceWithSpace) {
                        outString += ' ';
                    }
                }
            }

            return outString;
        };

        return {
            lowerCaseAndSpaceToDash: function (str) {
                return str.toLowerCase().replace(/\s+/g, '-');
            }
            ,spaceToDash: function (str) {
                return str.replace(/\s+/g, '-');
            }
            ,dashToSpace: function (str) {
                return str.replace('-', ' ');
            }
            ,stripNonAlphaNumeric: function (str, dashOk, replaceWithSpace) {
                return stripNonAlphaNumeric(str, dashOk, replaceWithSpace);
            }
        }
    }]
)

.factory('TypeAhead', ['Api',
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
        };
    }]
)

.factory('TransferPlanner', ['Api', 'Maps', 
    function (Api, Maps) {

        var TransferPlan = function () {
            var base = this;
            base.updating = false;
            base.sources = [];
            base.destinations = [];
            base.plateTransfers = [];
            base.errors = [];
            base.map = null;
            base.typeDetails = null;
            base.sourcesReady = false;
            base.destinationsReady = false;
            base.planFromFile = false;

            var updating = function () {
                base.updating = true;
            }

            var ready = function () {
                base.updating = false;
            }

            var returnEmptyPlate = function () {
                return {text: '', title: ''};
            };

            var updateTransferList = function () {
                if (base.sourcesReady && base.destinationsReady) {
                    var transfers = [];
                    
                    if (base.typeDetails.transfer_template_id == 1 || base.typeDetails.transfer_template_id == 2) {
                        /* sopurce and destination plate are same size and layout */
                        var plate = base.sources[0];
                        for (var j=0; j<plate.data.wells.length;j++) {
                            var sourceWell = plate.data.wells[j];
                            var transferRow = {
                                source_plate_barcode: plate.text
                                ,source_well_name: sourceWell.column_and_row
                                ,source_sample_id: sourceWell.sample_id
                                ,destination_plate_barcode: (base.typeDetails.transfer_template_id == 2 ? plate.text : base.destinations[0].text)
                                ,destination_well_name: sourceWell.column_and_row
                                ,destination_plate_well_count: Maps.plateTypeInfo[plate.data.plateDetails.type].wellCount
                            };
                            transfers.push(transferRow);
                        }
                        base.plateTransfers = transfers;
                    } else {
                        /* source and destination are different size and/or layout*/
                        for (var i=0;i< base.sources.length;i++) {
                            var plate = base.sources[i];
                            var wellsMap = base.map.plateWellToWellMaps[i];

                            console.log(wellsMap);

                            for (var j=0; j<plate.data.wells.length;j++) {
                                var sourceWell = plate.data.wells[j];
                                var destWell = wellsMap[sourceWell.well_id];
                                var destWellRowColumnMap = Maps.rowColumnMaps[base.map.destination.plateTypeId]
                                var transferRow = {
                                    source_plate_barcode: plate.text
                                    ,source_well_name: sourceWell.column_and_row
                                    ,source_sample_id: sourceWell.sample_id
                                    ,destination_plate_barcode: base.destinations[destWell.destination_plate_number - 1].text
                                    ,destination_well_name: destWellRowColumnMap[destWell.destination_well_id].row + destWellRowColumnMap[destWell.destination_well_id].column
                                    ,destination_plate_well_count: Maps.plateTypeInfo[base.map.destination.plateTypeId].wellCount
                                };
                                transfers.push(transferRow);
                            }
                        }
                    }

                    base.plateTransfers = transfers;
                    console.log(base.plateTransfers);
                } else {
                    console.log('NOT TRANS READY!!!');
                    clearPlateTransfers();
                }
            };

            var clearPlateTransfers = function () {
                base.plateTransfers = [];
            };

            var notReady = function (which) {
                if (which == 'source') {
                    base.sourcesReady = false;
                } else if (which == 'destination') {
                    base.destinationsReady = false;
                }
                clearPlateTransfers();
            };

            var sourcesReady

            base.setTransferTypeDetails = function (typeObj) {
                base.typeDetails = typeObj;
                base.setTransferMap(Maps.transferTemplates[base.typeDetails.transfer_template_id]);
                base.transferFromFile(false);
            }

            base.setTransferMap = function (map) {
                base.map = map;

                var sourceCount = base.map.source.plateCount;
                var destCount = base.map.destination.plateCount;

                /* we need to expand or contract the plate arrays to match the selected step type */
                while (base.sources.length != sourceCount) {
                    if (base.sources.length < sourceCount) {
                        base.sources.push(returnEmptyPlate());
                    } else if (base.sources.length > sourceCount) {
                        base.sources.splice(base.sources.length - (base.sources.length - sourceCount));
                    }
                }
                while (base.destinations.length != destCount) {
                    if (base.destinations.length < destCount) {
                        base.destinations.push(returnEmptyPlate());
                    } else if (base.destinations.length > destCount) {
                        base.destinations.splice(base.destinations.length - (base.destinations.length - destCount));
                    }
                }

                //TO DO - move labels into transfer map
                for (var i=0; i<base.sources.length; i++) {
                    base.sources[i].title = base.map.source.plateTitles ? base.map.source.plateTitles[i] || '' : '';
                }
                for (var i=0; i<base.destinations.length; i++) {
                    base.destinations[i].title = base.map.destination.plateTitles ? base.map.destination.plateTitles[i] || '' : '';
                }

                if (!base.map.destination.plateCount) {
                    base.destinationsReady = true;
                }

            };

            base.addSourcePlate = function (sourceIndex) {
                var sourceItem = base.sources[sourceIndex];
                delete sourceItem.error;
                var barcode = sourceItem.text;

                var onError = function (sourceItem, msg) {
                    notReady('source');
                    sourceItem.data = null;
                    sourceItem.transferList = null;
                    sourceItem.error = msg;
                    ready();
                    sourceItem.updating = false;
                };

                updating();
                sourceItem.updating = true;
                Api.getPlateDetails(barcode).success(function (data) {
                    if (data.success) {
                        console.log('TO DO: validate proper plate type etc');

                        if (base.map.source.plateTypeId && data.plateDetails.type != base.map.source.plateTypeId) {
                            onError(sourceItem, 'Error: Source plate ' + barcode + ' type (' + data.plateDetails.type + ') does not match the expected value of ' + base.map.source.plateTypeId);
                        } else {
                            sourceItem.data = data;
                            for (var i=0; i<base.sources.length; i++) {
                                if (base.sources[i].data == null) {
                                    notReady('source');
                                    return;
                                }
                            }
                            base.sourcesReady = true;
                            updateTransferList();
                        }
                        ready();
                        sourceItem.updating = false;
                        console.log(base);
                    } else {
                        onError(sourceItem, 'Error: Plate info for ' + barcode + ' could not be found.');
                    }  
                }).error(function () {
                    onError(sourceItem, 'Error: Plate data for ' + barcode + ' could not be retrieved.');
                });
            }

            base.addDestinationPlate = function (destIndex) {
                console.log('ADD DESTINATION PLATE');
                var destItem = base.destinations[destIndex];
                delete destItem.error;
                var barcode = destItem.text;

                var onError = function (destItem, msg) {
                    notReady('destination');
                    if (msg) {
                        destItem.error = msg;
                    }
                    ready();
                };

                if (barcode.length > 5) {

                    updating();
                    Api.getPlateDetails(barcode).success(function (data) {
                        if (data.success) {
                            onError(destItem, 'Error: A plate with barcode ' + barcode + ' already exists in the database.');
                            console.log(base.errors);
                            console.log(base);
                        } else { 
                            /* then we're good to go - check if we have all the required destination barcodes */
                            for (var i=0; i<base.destinations.length; i++) {
                                if (base.destinations[i].length < 6) {
                                    onError(destItem);
                                    return;
                                }
                            }
                            base.destinationsReady = true;
                            updateTransferList();
                            console.log('[[[[[[[' + base.destinationsReady);
                        }
                        ready();  
                    });

                } else {
                    onError();
                }
                console.log(']]]]]]]' + base.destinationsReady);
            };

            base.transferFromFile = function (engaged, transfersJSON) {
                base.planFromFile = engaged;
                if (engaged) {
                    base.plateTransfers = transfersJSON;
                } else {
                    clearPlateTransfers();
                }
            };

            var init = function () {
                return base;
            };

            return init();
        }

        return {

            newTransferPlan: function () {
                return new TransferPlan();
            }

        }

    }
])

.factory('Constants',[
    function () {
        return {
            PLATE_SOURCE: 'source'
            ,PLATE_DESTINATION: 'destination'
            ,STEP_TYPE_DROPDOWN_LABEL: 'Select a Step'
            ,USER_SPECIFIED_TRANSFER_TYPE: 'user_specified'
            ,STANDARD_TRANSFER_TYPE: 'standard'
            ,EXCEL: 'excel'
        };
    }]
)

.factory('FileParser',['Maps', 
    function (Maps) {

        var getNormalRowColumnFromQPix = function (rowColumn, plateType) {

            var qpixMap = Maps.rowColumnMaps['QPIX_SPTT_0004'];
            var humanMap = Maps.rowColumnMaps['SPTT_0004'];

            var row = rowColumn.substring(0, 1);
            var column = rowColumn.substring(1) - 0;

            for (well in qpixMap) {
                if (row == qpixMap[well].row && column == qpixMap[well].column) {
                    return humanMap[well].row + humanMap[well].column
                }
            }

            return 'ERROR: Could not map ' + rowColumn + ' to human well id.';
        };

        var getTransferRowsFromFile = function (fileData, transferPlan) {

            var map = transferPlan.map;
            var transferTypeData = transferPlan.transferTypeData;

            var transferJSON = [];
            var thisRow = {};
            var firstRow = true;
            var srcPlates = {};
            var destPlates = {};

            var fileErrors = [];
            var fileStats = {};

            var setStats = function (validateStats, isQpix) {

                fileStats.wellCountHeader = 'Source plate well counts:';
                if (isQpix) {
                    fileStats.wellCountHeader = 'Source plate pick counts:';
                }

                fileStats.sourceRowCounts = srcPlates;
            
                var count = 0;
                for (plate in srcPlates) {
                    count++;
                }
                fileStats.source_plate_count = count;

                if (validateStats && count != transferPlan.map.source.plateCount) {
                    fileErrors.push('This transfer expects ' + transferPlan.map.source.plateCount + ' source plate(s) but found ' + count + ' in the file');
                }
                var count = 0;
                for (plate in destPlates) {
                    count++;
                }
                fileStats.destination_plate_count = count;
                if (validateStats && count != transferPlan.map.destination.plateCount) {
                    fileErrors.push('This transfer expects ' + transferPlan.map.destination.plateCount + ' destination plate(s) but found ' + count + ' in the file');
                }

                fileStats.sourcePlateRows = srcPlates;
            }

            if ( fileData.substring(0, 8) == 'Run Date') {
                /* this is a csv log file from qpix */
                var transferTypeId = transferPlan.typeDetails.transfer_template_id;
                if (transferTypeId != 16 && transferTypeId != 21 && transferTypeId != 22) {
                    fileErrors.push('This transfer type (' + transferTypeId + ') does not expect a log file as input.');
                } else {
                    var fileData = fileData.split('\n');

                    var transferStartIndex = fileData.length;

                    for (var i=0; i<fileData.length; i++) {
                        var row = fileData[i];
                        if (row.trim() == 'Source Barcode,Source Region,Feature Position X,Feature Position Y,Destination Barcode,Destination Well') {
                            transferStartIndex = i + 1;
                        } else if (i >= transferStartIndex) {
                            var rowBits = row.split(',');

                            var sourceBarcode = rowBits[0];
                            var destinationBarcode = rowBits[4];
                            var sourceWellName = rowBits[1];
                            var destinationWellName = rowBits[5];

                            if (!srcPlates[sourceBarcode]) {
                                srcPlates[sourceBarcode] = 1;
                            } else {
                                srcPlates[sourceBarcode]++;
                            }
                            destPlates[destinationBarcode] = destinationBarcode;

                            var rowBits = row.split(',');
                            var destinationPlateTypeInfo = Maps.plateTypeInfo[map.destination.plateTypeId];
                            var thisRow = {
                                source_plate_barcode: sourceBarcode
                                ,source_well_name: getNormalRowColumnFromQPix(sourceWellName)
                                ,destination_plate_barcode: destinationBarcode
                                ,destination_well_name: destinationWellName
                                ,destination_plate_well_count: destinationPlateTypeInfo.wellCount
                            }
                            transferJSON.push(thisRow);
                        }
                    }

                    /* and now we need to retrieve the sample_ids for these wells by referring to the Hamilton step 

                        NEED TO USE PROMISE(S) FOR THIS
                    */



                    setStats(false, true)
                }
                
            } else {
                /* then we assume this is an excel file */
                var workbook = XLSX.read(fileData, {type: 'binary'});

                var first_sheet_name = workbook.SheetNames[0];
                var worksheet = workbook.Sheets[first_sheet_name];

                // parse through the sheet and compile the rows to json
                for (z in worksheet) {
                    if(z[0] === '!') {continue;}
                    var col = z.substring(0,1);
                    var val = worksheet[z].v;
                    switch (col) {
                        case 'A':
                            thisRow.source_plate_barcode = val;
                            if (!firstRow) {
                                if (!srcPlates[val]) {
                                    srcPlates[val] = 1;
                                } else {
                                    srcPlates[val]++;
                                }
                            }
                            break;
                        case 'B':
                            thisRow.source_well_name = val;
                            break;    
                        case 'C':
                            thisRow.destination_plate_barcode = val;
                            if (!firstRow) {
                                destPlates[val] = val;
                            }
                            break;
                        case 'D':
                            thisRow.destination_well_name = val;
                            break;
                        case 'E':
                            thisRow.destination_plate_well_count = val;
                            break;

                        default :
                            fileErrors.push('Error: Unknown column in input file: ' + col);
                            break;
                    }
                    if (col == 'E') {
                        if (!firstRow) {
                            transferJSON.push(thisRow);
                        }
                        firstRow = false;
                        thisRow = {};
                    }
                }

                setStats(true);
            }

            var result = {
                errors: fileErrors
                ,stats: fileStats
                ,transferJSON: transferJSON
            };
                
            return result;
        }
        return {
            getTransferRowsFromFile: getTransferRowsFromFile
        };
    }]
)


;