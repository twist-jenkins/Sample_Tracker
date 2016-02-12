var api_base_url = '/api/v1/';
var server_url = twist_api_url;

angular.module('twist.app').factory('FileParser',['Maps', '$q', 'Api',  
    function (Maps, $q, Api) {

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

        var getTransferRowsFromFile = function (fileData, transformSpec) {

            var map = transformSpec.map;
            var transferTypeData = transformSpec.transferTypeData;

            var transferJSON = [];
            var thisRow = {};
            var firstRow = true;
            var srcPlates = {};
            var destPlates = {};

            var fileErrors = [];
            var fileStats = {};

            var asyncReturn = $q.defer();

            var setStats = function (validateStats, isQpix) {

                fileStats.wellCountHeader = 'Source plate well counts:';
                if (isQpix) {
                    fileStats.wellCountHeader = 'Source plate pick counts:';
                }

                fileStats.sourceRowCounts = srcPlates;
            
                var count = 0;
                var plates = [];
                for (plate in srcPlates) {
                    count++;
                    plates.push(plate);
                }
                fileStats.sources = plates.concat([]);
                fileStats.source_plate_count = count;

                if (fileStats.source_plate_count == 0) {
                    fileErrors.push('This file contains no source plates.');
                }

                if (validateStats && !transformSpec.map.source.variablePlateCount && count != transformSpec.map.source.plateCount) {
                    fileErrors.push('This transfer expects ' + transformSpec.map.source.plateCount + ' source plate(s) but found ' + count + ' in the file');
                }
                count = 0;
                plates = [];
                for (plate in destPlates) {
                    count++;
                    plates.push(plate);
                }
                fileStats.destinations = plates.concat([]);
                fileStats.destination_plate_count = count;

                if (fileStats.destination_plate_count == 0) {
                    fileErrors.push('This file contains no destination plates.');
                }

                if (validateStats && !transformSpec.map.destination.variablePlateCount && count != transformSpec.map.destination.plateCount) {
                    if (transformSpec.details.transfer_template_id == 2) {
                        if (count != 1) {
                            fileErrors.push('This transfer expects the same source and destination plate but found ' + count + ' destination plates in the file');
                        }
                    } else {
                        fileErrors.push('This transfer expects ' + transformSpec.map.destination.plateCount + ' destination plate(s) but found ' + count + ' in the file');
                    }
                    
                }

                fileStats.sourcePlateRows = srcPlates;
            }

            if ( fileData.substring(0, 8) == 'Run Date') {
                /* this is a csv log file from qpix */
                var transferTypeId = transformSpec.details.transfer_template_id;
                if (transferTypeId != 16 && transferTypeId != 21 && transferTypeId != 22) {
                    fileErrors.push('This transfer type (' + transferTypeId + ') does not expect a log file as input.');
                    var result = {
                        errors: fileErrors
                        ,stats: fileStats
                        ,transferJSON: transferJSON
                    };
                    asyncReturn.reject(result);
                } else {
                    var fileData = fileData.split('\r');

                    var transferStartIndex = fileData.length;

                    for (var i=0; i<fileData.length; i++) {
                        var row = fileData[i].trim();
                        if (row.trim() == 'Source Barcode,Source Region,Feature Position X,Feature Position Y,Destination Barcode,Destination Well') {
                            transferStartIndex = i + 1;
                        } else if (i >= transferStartIndex && row != '') {
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

                    setStats(false, true);
                    
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

            var packageResponse = function () {
                var result = {
                    errors: fileErrors
                    ,stats: fileStats
                    ,transferJSON: transferJSON
                };

                asyncReturn.resolve(result);
            };

            var decorateResponse = function (respData, thisError) {

                if (thisError) {
                    fileErrors.push(thisError);
                } else {
                    for (var i=0; i< transferJSON.length; i++) {
                        var row = transferJSON[i];
                        var sourceBarcode = row.source_plate_barcode;
                        var sourcePlateWellData = respData.plateWellData[sourceBarcode];
                        transferJSON[i]['source_sample_id'] = sourcePlateWellData.wells[row.source_well_name] ? sourcePlateWellData.wells[row.source_well_name]['sample_id'] : 'empty';
                    }
                }

                packageResponse();
            }

            if (fileErrors.length) {
                packageResponse();
            } else {
                var source_barcodes = [];
                for (barcode in srcPlates) {
                    source_barcodes.push(barcode);
                }
                var destination_barcodes = [];
                for (barcode in destPlates) {
                    destination_barcodes.push(barcode);
                }

                Api.getSourcePlateWellData(source_barcodes).success(function (data) {
                    var sourceData = data;

                    if (sourceData.success) {

                        if (transformSpec.details.transfer_template_id != 2) {
                            /* this is NOT a same-plate step, check that the destination plate is not already in the db */
                            Api.checkDestinationPlatesAreNew(destination_barcodes).success(function (data) {
                                if (!data.success) {
                                    /* error - destination plates already exist */
                                    decorateResponse(sourceData, data.errorMessage);
                                } else {
                                    /* destination plates are new - we're good to go */
                                    decorateResponse(sourceData);
                                }
                            }).error(function (data) {
                                decorateResponse(sourceData, 'The server returned an error while checking information about the destination plate(s).');
                            });
                        } else {
                            /* this is a same-plate step so the dest plate will already exist - no need to check for it */
                            decorateResponse(sourceData);
                        }
                        
                    } else {
                        decorateResponse(sourceData, sourceData.errorMessage);
                    }
                }).error(function (data) {
                    decorateResponse(data, 'Sample information could not be retrieved for these source plates.');
                });
            }
                
            return asyncReturn.promise;
        }
        return {
            getTransferRowsFromFile: getTransferRowsFromFile
        };
    }]
);
