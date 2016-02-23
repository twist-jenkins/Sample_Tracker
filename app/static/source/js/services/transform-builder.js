var api_base_url = '/api/v1/';
var server_url = twist_api_url;

angular.module('twist.app').factory('TransformBuilder', ['Api', 'Maps', 'Constants',
    function (Api, Maps, Constants) {

        var TransformSpec = function () {
            var base = this;
            base.type = null;
            base.title = '';
            base.sources = [];
            base.destinations = [];
            base.operations = [];

            base.updating = false;
            base.errors = [];
            base.map = null;
            base.details = null;
            base.sourcesReady = false;
            base.destinationsReady = false;
            base.planFromFile = false;
            base.autoUpdateSpec = true;

            base.error_message = '';

            var updating = function () {
                base.updating = true;
            }

            var ready = function () {
                base.updating = false;
            }

            var returnEmptyPlate = function () {
                return new TransformSpecSource(Constants.SOURCE_TYPE_PLATE);
            };

            base.updateOperationsList = function (toggleUpdating) {
                if (base.autoUpdateSpec) {

                    if (toggleUpdating) {
                        updating();
                    }

                    if (base.type == Constants.TRANSFORM_SPEC_TYPE_PLATE_STEP ||
                        (base.type == Constants.TRANSFORM_SPEC_TYPE_PLATE_PLANNING && base.details.transform_template_id >= 25 && base.details.transform_template_id <=29) ) {
                        if (base.sourcesReady && base.destinationsReady) {
                            // kieran
                            Api.previewTransformation( base.sources, base.destinations, base.details )
                                .success( function(result) {
                                    if( result.success ) {
                                        base.error_message = '';
                                        base.operations = result.data;

                                        if (result.responseCommands) {
                                            /* this transform requires additional actions or input data */
                                            base.handleResponseCommands(result.responseCommands);
                                        }

                                        if (base.operations.length) {
                                            //if we got operations, then that means sources AND destinations were ready
                                            //we should force validation on any requested data that exists since
                                            //otherwise this transform spec should be ready to save
                                            if (base.requestedDataItems && base.requestedDataItems.length) {
                                                for (var i=0; i < base.requestedDataItems.length; i++) {
                                                    base.requestedDataItems[i].validateNow = true;
                                                }
                                            }
                                        }

                                    } else {
                                        base.error_message = result.message;
                                    }

                                    if (toggleUpdating) {
                                        ready();
                                    }
                                }).error(function(data) {
                                    console.log('Error retrieving transform preview.');
                                });

                        } else {
                            base.clearOperationsList();
                            if (toggleUpdating) {
                                ready();
                            }
                        }
                    } else if (base.type == Constants.TRANSFORM_SPEC_TYPE_PLATE_PLANNING) {
                        // "rebatching for transformation"

                        if (base.sourcesReady) {

                            var templateId = base.details.transform_template_id;

                            switch (templateId) {
                                /***
                                * moved to backend

                                case 25:
                                    //Rebatching for trannsformation
                                    //first, we'll group source wells based on resistance_marker values
                                    var resistanceGroups = {};
                                    var destinationQuadrants = {};
                                    var destinationPlates = {};

                                    for (var i=0; i<base.sources.length;i++) {
                                        var source = base.sources[i];
                                        for (var j=0; j < source.items.length; j++) {
                                            var well = angular.copy(source.items[j]);
                                            well.source_plate_barcode = source.details.id
                                            var rMarkerVal = well.resistance_marker_plan ? well.resistance_marker_plan.toUpperCase() : 'NULL';
                                            if (!resistanceGroups[rMarkerVal]) {
                                                resistanceGroups[rMarkerVal] = [];
                                            }
                                            resistanceGroups[rMarkerVal].push(well);
                                        }
                                    }
                                    console.log(resistanceGroups);

                                    // resistance groups get written as 96-well quadrants to 384 well trays
                                    // build the quadrants
                                    for (group in resistanceGroups) {
                                        destinationQuadrants[group] = new Array(Math.ceil(resistanceGroups[group].length/96));
                                        var quadIndex = 0;
                                        for (var i=0; i < resistanceGroups[group].length; i++) {
                                            if (i && i%96 == 0) {
                                                quadIndex++;
                                            }
                                            if (!destinationQuadrants[group][quadIndex]) {
                                                destinationQuadrants[group][quadIndex] = [];
                                            }
                                            destinationQuadrants[group][quadIndex].push(resistanceGroups[group][i])
                                        }
                                    }
                                    console.log(destinationQuadrants);

                                    // use the 4-to-1 combine map to write the quadrants to 384 well plates
                                    var theMap = Maps.transformTemplates[18];

                                    // configure the ultimate destination plates - 384 wells
                                    for (group in destinationQuadrants) {
                                        destinationPlates[group] = new Array(Math.ceil(destinationQuadrants[group].length/4));

                                        var plateIndex = 0;
                                        for (var i=0; i < destinationQuadrants[group].length; i++) {
                                            if (i && i%4 == 0) {
                                                plateIndex++;
                                            }

                                            var quadrant = destinationQuadrants[group][i];
                                            var quardrantMap = theMap.plateWellToWellMaps[i%4];

                                            for (var j=0; j< quadrant.length; j++) {
                                                var well = quadrant[j];
                                                well.destination_plate_number = quardrantMap[j+1].destination_plate_number;
                                                console.log(well.destination_plate_number)
                                                well.destination_well_id = quardrantMap[j+1].destination_well_id;
                                                if (!destinationPlates[group][plateIndex]) {
                                                    destinationPlates[group][plateIndex] = [];
                                                }
                                                destinationPlates[group][plateIndex].push(well);
                                            }
                                        }

                                    }

                                    console.log(destinationPlates);

                                    var plateIndex = -1;

                                    //and add or fill the destination inputs for the necessary plates
                                    for (group in destinationPlates) {
                                        var plates = destinationPlates[group];
                                        for (var i=0; i<plates.length; i++) {
                                            plateIndex++;
                                            var dest = returnEmptyPlate();
                                            dest.details.title = '<strong>' + group + '</strong> Resistance  - <strong>Plate ' + (i + 1) + '</strong> of  ' + plates.length + ' &nbsp;(' + plates[i].length + ' wells filled):';
                                            if (!i) {
                                                dest['first_in_group'] = true;
                                            }
                                            if (base.destinations[plateIndex]) {
                                                if (base.destinations[plateIndex].loaded || base.destinations[plateIndex].updating) {
                                                    //do nothing - this destination was already entered
                                                } else {
                                                    dest.details.id = base.destinations[plateIndex].details.id;
                                                    base.destinations[plateIndex] = dest;
                                                    base.addDestination(plateIndex);
                                                }
                                            } else {
                                                base.destinations[plateIndex] = dest;
                                                base.addDestination(plateIndex);
                                            }

                                        }
                                    }

                                    if (base.destinationsReady) {

                                        var operations = [];

                                        var destPlateIndex = 0;

                                        for (group in destinationPlates) {
                                            var plates = destinationPlates[group];
                                            for (var i=0; i<plates.length; i++) {
                                                var plate = plates[i];
                                                destPlateIndex += i;

                                                for (var j=0; j<plate.length;j++) {
                                                    var sourceWell = plate[j];
                                                    var destWellRowColumnMap = Maps.rowColumnMaps[base.map.destination.plateTypeId];
                                                    var operationRow = {
                                                        source_plate_barcode: sourceWell.source_plate_barcode
                                                        ,source_well_name: sourceWell.column_and_row
                                                        ,source_sample_id: sourceWell.sample_id
                                                        ,destination_plate_barcode: base.destinations[destPlateIndex].details.id
                                                        ,destination_well_name: destWellRowColumnMap[sourceWell.destination_well_id].row + destWellRowColumnMap[sourceWell.destination_well_id].column
                                                        ,destination_plate_well_count: Maps.plateTypeInfo[theMap.destination.plateTypeId].wellCount
                                                    };
                                                    operations.push(operationRow);
                                                }
                                            }
                                            destPlateIndex++;

                                        }

                                        base.operations = operations;

                                    } else {
                                        base.clearOperationsList();
                                    }

                                break;
                                */

                            case 30:
                                    /* for NGS, the destination plate is the same as the source plate (as entered)
                                    * BUT the source plate we record is a placeholder for the dna barcodes plate
                                    * so we need to adjust the generated operations to reflect this */
                                    var operations = [];


                                    for (var i=0; i<base.sources.length;i++) {
                                        var plate = base.sources[i];
                                        for (var j=0; j<plate.items.length;j++) {
                                            var sourceWell = plate.items[j];
                                            var operationRow = {
                                                source_plate_barcode: 'NGS_BARCODE_PLATE'
                                                ,source_well_name: sourceWell.column_and_row
                                                ,source_sample_id: sourceWell.sample_id
                                                ,destination_plate_barcode: plate.details.id
                                                ,destination_well_name: sourceWell.column_and_row
                                                ,destination_plate_well_count: Maps.plateTypeInfo[plate.details.plateDetails.type].wellCount
                                            };
                                            operations.push(operationRow);
                                        }
                                    }

                                    base.operations = operations;
                                    break;
                            case 31:
                                    /* these are the interim types for Keiran to work on while kipp is in Puerto Rico */
                                    var operations = [];

                                    if (base.destinationsReady) {
                                        for (var i=0; i<base.sources.length;i++) {
                                            var plate = base.sources[i];
                                            for (var j=0; j<plate.items.length;j++) {
                                                var sourceWell = plate.items[j];
                                                var operationRow = {
                                                    source_plate_barcode: plate.details.id
                                                    ,source_well_name: sourceWell.column_and_row
                                                    ,source_sample_id: sourceWell.sample_id
                                                    ,destination_plate_barcode: base.destinations[0].details.id
                                                    ,destination_well_name: 'A1'
                                                    ,destination_plate_well_count: 1
                                                };
                                                operations.push(operationRow);
                                            }
                                        }
                                    }
                                    base.operations = operations;
                                    break;

                            default :
                                    console.log('Error: Unrecognized plate planning template id = [' + templateId + ']');
                                    break;
                            }

                        } else {
                            base.clearOperationsList();
                        }
                    }
                }
            };

            base.notReady = function (which) {
                if (which == Constants.PLATE_SOURCE) {
                    base.sourcesReady = false;
                } else if (which == Constants.PLATE_DESTINATION) {
                    base.destinationsReady = false;
                }
                base.clearOperationsList();
            };

            var sourcesReady;

            base.setType = function (thisType) {
                base.type = thisType;
            };

            base.setTitle = function (thisTitle) {
                base.title = thisTitle;
            };

            base.setDescription = function (description) {
                base.description = description;
            };

            base.getSourcesHeader = function () {
                var header = '';

                if (base.type == Constants.TRANSFORM_SPEC_TYPE_PLATE_STEP) {
                    header = 'Plate Barcode';
                    header+= base.sources.length > 1 ? 's' :'';
                    if (base.destinations.length) {
                        header = 'Source ' + header;
                    }
                } else if (base.type == Constants.TRANSFORM_SPEC_TYPE_PLATE_PLANNING) {
                    header = 'Source(s)'
                }

                return header;
            };

            base.addRequestedDataItems = function (items) {
                //don't replace data requests we've already gotten/displayed
                for (var i=0; i< items.length ;i++) {
                    var newItem = items[i];
                    var already = false;
                    for (var j=0; j < base.requestedDataItems.length; j++) {
                        currentItem = base.requestedDataItems[j];
                        if (currentItem.item.forProperty == newItem.item.forProperty) {
                            already = true;
                        }
                    }

                    if (!already) {
                        base.requestedDataItems.push(angular.copy(newItem));
                    }
                }

                base.validateRequestedData = true;
            }

            base.addPresentedDataItems = function (items) {
                for (var i=0; i< items.length ;i++) {
                    var newItem = items[i];
                    var already = false;
                    for (var j=0; j < base.presentedDataItems.length; j++) {
                        currentItem = base.presentedDataItems[j];
                        if (currentItem.item.forProperty == newItem.item.forProperty) {
                            base.presentedDataItems[j] = newItem;
                            already = true;
                        }
                    }

                    if (!already) {
                        base.presentedDataItems.push(angular.copy(newItem));
                    }
                }
            }

            base.getDestinationsHeader = function () {
                var header = '';

                if (base.type == Constants.TRANSFORM_SPEC_TYPE_PLATE_STEP) {
                    header = 'Destination Plate Barcode';
                    header+= base.destinations.length > 1 ? 's' :'';
                } else if (base.type == Constants.TRANSFORM_SPEC_TYPE_PLATE_PLANNING) {
                    header = 'Destination(s)'
                }

                return header;
            };

            base.clearOperationsList = function () {
                base.operations = [];
            };

            base.setTransformSpecDetails = function (typeObj) {
                base.details = typeObj;
                base.details['transform_type_id'] = typeObj.id;
                base.setTransformMap(Maps.transformTemplates[base.details.transform_template_id]);
                if (base.details.transform_template_id == 25 ||
                    base.details.transform_template_id == 26 ||
                    base.details.transform_template_id == 27 ||
                    base.details.transform_template_id == 28 ||
                    base.details.transform_template_id == 29 ||
                    base.details.transform_template_id == 30) {
                    base.setType(Constants.TRANSFORM_SPEC_TYPE_PLATE_PLANNING);
                } else {
                    base.setType(Constants.TRANSFORM_SPEC_TYPE_PLATE_STEP);
                }

                /* and read in any configured requested/presented data */

                if (base.map.details && base.map.details.requestedData) {

                    var requestedData = [];

                    for (var i=0; i< base.map.details.requestedData.length; i++) {
                        requestedData.push({
                            type: Constants.RESPONSE_COMMANDS_REQUEST_DATA
                            ,item: base.map.details.requestedData[i]
                        });
                    }

                    base.addRequestedDataItems(requestedData);
                }

                base.transformFromFile(false);
            }

            base.setTransformMap = function (map) {
                base.map = angular.copy(map);
                base.updateInputs();
            };

            base.updateInputs = function () {
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

                for (var i=0; i<base.sources.length; i++) {
                    base.sources[i].details.title = base.map.source.plateTitles ? base.map.source.plateTitles[i] || '' : '';
                }
                for (var i=0; i<base.destinations.length; i++) {
                    base.destinations[i].details.title = base.map.destination.plateTitles ? base.map.destination.plateTitles[i] || '' : '';
                    delete base.destinations[i]['first_in_group'];
                }

                if (!base.map.destination.plateCount) {
                    base.destinationsReady = true;
                }
            }

            base.addPlateInput = function (which, howMany) {
                if (!howMany) {
                    howMany = 1;
                }
                base.map[which].plateCount += howMany;
                base.updateInputs();
                base.updateOperationsList();
            }

            base.removePlateInput = function (which, plateIndex) {
                base.map[which].plateCount--;

                var newSources = [];
                var plates = base[which + 's'];
                for (var i=0; i<plates.length; i++) {
                    if (i != plateIndex) {
                        newSources.push(plates[i]);
                    }
                }
                base[which + 's'] = newSources;
                base.updateInputs();
                base.updateOperationsList();
            }

            base.checkSourcesReady = function (clearErrors) {

                for (var i=0; i<base.sources.length; i++) {

                    if (!base.sources[i].loaded) {
                        if (!base.sources[i].updating) { /* don't call base.notReady if the plate is still fetching its data */
                            delete base.sources[i].loaded
                            delete base.sources[i].error;
                            base.notReady('source');
                            return false;
                        }
                    } else {
                        //we might have loaded data but then removed the barcode for this input
                        if (base.sources[i].details.id == "") {
                            delete base.sources[i].loaded;
                            delete base.sources[i].error;
                            base.notReady('source');
                            return false;
                        }
                    }

                }
                return true;
            }

            base.addSource = function (sourceIndex) {
                var sourceItem = base.sources[sourceIndex];
                delete sourceItem.error;
                delete sourceItem.loaded;
                var barcode = sourceItem.details.id;

                /* TODO: add barcode format validation once we have it settled */

                var onError = function (sourceItem, msg) {
                    base.notReady('source');
                    sourceItem.loaded = false;
                    sourceItem.transformList = null;
                    sourceItem.error = msg;
                    sourceItem.updating = false;
                    ready();
                };

                updating();
                sourceItem.updating = true;

                var plateDetailsFetcher = Api.getBasicPlateDetails;

                if (base.type == Constants.TRANSFORM_SPEC_TYPE_PLATE_PLANNING) {
                    plateDetailsFetcher = Api.getPlateDetails;
                }

                plateDetailsFetcher(barcode).success(function (data) {
                    if (data.success) {
                        if (base.map.source.create) {
                            //then the source plate will be created in this step and should not exist - this success is actually an error
                            onError(sourceItem, 'Error: An plate with barcocde <strong>#' + barcode + '</strong> already exists.');
                        } else {

                            if (base.map.source.plateTypeId && data.plateDetails.type != base.map.source.plateTypeId) {
                                onError(sourceItem, 'Error: Source plate ' + barcode + ' type (' + data.plateDetails.type + ') does not match the expected value of ' + base.map.source.plateTypeId);
                            } else {
                                sourceItem.loaded = true;
                                sourceItem.items = data.wells;

                                var dataCopy = angular.copy(data);
                                delete dataCopy.wells;
                                jQuery.extend(sourceItem.details, dataCopy);
                                sourceItem.updating = false;
                                if (base.checkSourcesReady()) {
                                    base.sourcesReady = true;
                                } else {
                                    return;
                                }
                                base.updateOperationsList();
                            }
                            ready();
                        }
                        sourceItem.updating = false;
                    } else {
                        onError(sourceItem, 'Error: Plate info for ' + barcode + ' could not be found.');
                    }
                }).error(function (data) {
                    // if this transform expects source plates to be created in this step, then they won't already exist
                    // and this is an expected error
                    if (base.map.source.create) {
                        sourceItem.loaded = true;
                        sourceItem.updating = false;
                        if (base.checkSourcesReady()) {
                            base.sourcesReady = true;
                        }
                        base.updateOperationsList();
                        ready();
                    } else {
                        onError(sourceItem, 'Error: Plate data for ' + barcode + ' could not be retrieved.');
                    }
                });
            }

            base.checkDestinationsReady = function () {
                for (var i=0; i<base.destinations.length; i++) {
                    if (!base.destinations[i].details.id || (base.destinations[i].details.id && base.destinations[i].details.id.length < 6)) {
                        base.destinations[i].loaded = false;
                        base.notReady('destination');
                        return false;
                    }
                }
                return true;
            }

            base.addDestination = function (destIndex) {
                var destItem = base.destinations[destIndex];
                var barcode = destItem.details.id;

                var onError = function (destItem, msg) {
                    base.notReady('destination');
                    if (msg) {
                        destItem.error = msg;
                    }
                    destItem.updating = false;
                    ready();
                };

                if (barcode && barcode.length > 5) {

                    delete destItem.error;
                    delete destItem.loaded;

                    updating();
                    destItem.updating = true;

                    var barcodeArray = [barcode];

                    Api.checkDestinationPlatesAreNew(barcodeArray).success(function (data) {
                        if (!data.success) {
                            /* error - destination plates already exist */
                            onError(destItem, 'Error: A plate with barcode ' + barcode + ' already exists in the database.');
                        } else {
                            /* destination plate is new - we're good to go */
                            destItem.loaded = true; /* shows the "valid" icon for this input */
                            destItem.updating = false;
                            /* check if we have all the required destination barcodes */
                            for (var i=0; i<base.destinations.length; i++) {
                                if (base.destinations[i].details.id && base.destinations[i].details.id.length < 6) {
                                    onError(destItem);
                                    return;
                                } else if (!base.destinations[i].details.id) {
                                    base.destinationsReady = false;
                                    return;
                                }
                            }
                            base.destinationsReady = true;
                            base.updateOperationsList();
                        }
                        ready();
                    }).error(function (data) {
                        onError(destItem, 'The server returned an error while checking information about the destination plate.');
                    });

                } else {
                    onError(destItem, destItem.loaded ? 'Error: A barcode is required for this destination.' : false);
                }
            };

            base.setPlanFromFile = function (planFromFile) {
                base.planFromFile = planFromFile;
                base.autoUpdateSpec = !planFromFile;
            }

            base.transformFromFile = function (engaged, resultData) {
                base.setPlanFromFile(engaged);
                if (engaged) {
                    base.operations = resultData.transformJSON;
                    if (resultData.stats.sources.length) {
                        base.sources = [];
                        for (var i=0; i<resultData.stats.sources.length;i++) {
                            var source = returnEmptyPlate();
                            source.details.id = resultData.stats.sources[i];
                            base.sources.push(source);
                            base.addSource(base.sources.length - 1);
                        }
                    }

                    if (resultData.stats.destinations.length) {
                        base.destinations = [];
                        for (var i=0; i<resultData.stats.destinations.length;i++) {
                            var dest = returnEmptyPlate();
                            dest.details.id = resultData.stats.destinations[i];
                            base.destinations.push(dest);
                            base.addDestination(base.destinations.length - 1);
                        }
                    }
                } else {
                    base.clearOperationsList();
                }
            };

            base.getAsExcel = function () {

                var orderRowKeys = [
                    'source_plate_barcode'
                    ,'source_well_name'
                    ,'destination_plate_barcode'
                    ,'destination_well_name'
                    ,'destination_plate_well_count'
                ]

                var columnTitles = [
                    'Source Plate Barcode'
                    ,'Source Well'
                    ,'Destination Plate Barcode'
                    ,'Destination Well'
                    ,'Destination Well Count'
                ]

                /* excel file writing helpers */

                var Workbook = function () {
                    if(!(this instanceof Workbook)) return new Workbook();
                    this.SheetNames = [];
                    this.Sheets = {};
                };

                var datenum = function (v, date1904) {
                    if(date1904) v+=1462;
                    var epoch = Date.parse(v);
                    return (epoch - new Date(Date.UTC(1899, 11, 30))) / (24 * 60 * 60 * 1000);
                }

                var setCellDataType = function (cell) {
                    if(typeof cell.v === 'number') cell.t = 'n';
                    else if(typeof cell.v === 'boolean') cell.t = 'b';
                    else if(cell.v instanceof Date) {
                        cell.t = 'n'; cell.z = XLSX.SSF._table[14];
                        cell.v = datenum(cell.v);
                    }
                    else cell.t = 's';
                }

                /* end excel file writing helpers */

                var writeHeaderRow = function () {
                    for (var i=0; i<columnTitles.length; i++) {
                        var cell = {v: columnTitles[i]};
                        var cell_ref = XLSX.utils.encode_cell({c:i,r:0});
                        setCellDataType(cell);
                        ws[cell_ref] = cell;
                    }
                }

                var wb = new Workbook();
                wb.SheetNames.push('Twist Transform Plan');

                var ws = {};
                writeHeaderRow();
                /* range is s = starting row and col value; e = ending row and col value */
                /* basically, it should be 0,0 to col_count, row_count */
                var range = {s: {c:0, r:0}, e: {c:4, r: base.operations.length + 1}};
                for(var i = 0; i != base.operations.length; i++) {
                    row = base.operations[i];
                    for (var j=0; j<orderRowKeys.length; j++) {
                        var cell = {v: row[orderRowKeys[j]]};
                        var cell_ref = XLSX.utils.encode_cell({c:j,r:i + 1});
                        setCellDataType(cell);
                        ws[cell_ref] = cell;
                    }
                }
                ws['!ref'] = XLSX.utils.encode_range(range);
                var wscols = [
                    {wch:40}
                    ,{wch:20}
                    ,{wch:40}
                    ,{wch:20}
                    ,{wch:15}
                ];
                ws['!cols'] = wscols;

                wb.Sheets['Twist Transform Plan'] = ws;
                var wbout = XLSX.write(wb, {bookType:'xlsx', bookSST:true, type: 'binary'});

                var s2ab = function (s) {
                    var buf = new ArrayBuffer(s.length);
                    var view = new Uint8Array(buf);
                    for (var i=0; i!=s.length; ++i) view[i] = s.charCodeAt(i) & 0xFF;
                    return buf;
                }

                /*  saveAs is a global method supported natively or with FileSaver */
                saveAs(new Blob([s2ab(wbout)],{type:""}), "test.xlsx")
            };

            base.setPlateStepDefaults = function () {
                base.setType(Constants.TRANSFORM_SPEC_TYPE_PLATE_STEP);
            };

            base.reset = function () {
                base.presentedDataItems = [];
                base.requestedDataItems = [];


                for (var i=0; i< base.sources.length; i++) {
                    var source = base.sources[i];
                    if (source.details.id && source.details.id != '') {
                        base.addSource(i);
                    } else {
                        delete source.error;
                        delete source.loaded;
                    }
                }
                for (var i=0; i< base.destinations.length; i++) {
                    var destination = base.destinations[i];
                    if (destination.details.id && destination.details.id != '') {
                        base.addDestination(i);
                    } else {
                        delete destination.error;
                        delete destination.loaded;
                    }
                }
            }

            base.setCreateEditDefaults = function () {
                base.setTitle('New Transform Spec');
                base.setType(Constants.TRANSFORM_SPEC_TYPE_CUSTOM_PLATING);
                base.autoUpdateSpec = false;
            };

            base.handleResponseCommands = function (commands) {

                var presentedDataItems = [];
                var requestedDataItems = [];

                for (var i=0; i<commands.length; i++) {
                    var command = commands[i];
                    switch (command.type) {
                        case Constants.RESPONSE_COMMANDS_SET_DESTINATIONS:
                            var plates = command.plates;
                            for (var j=0; j<plates.length;j++) {
                                var plate = plates[j];
                                var dest = returnEmptyPlate();
                                dest.details.type = plate.type;
                                dest.details.title = plate.details.title;
                                dest.details.id = plate.details.id;
                                dest.first_in_group = plate.first_in_group;

                                if (base.destinations[j]) {
                                    if (base.destinations[j].loaded || base.destinations[j].updating) {
                                        //do nothing - this destination was already entered
                                    } else {
                                        dest.details.id = base.destinations[j].details.id;
                                        base.destinations[j] = dest;
                                        base.addDestination(j);
                                    }
                                } else {
                                    base.destinations[j] = dest;
                                    base.addDestination(j);
                                }
                            }
                            if (base.destinations.length > plates.length) {
                                base.destinations.splice(plates.length - base.destinations.length);
                            }
                            base.map.destination.plateCount = base.destinations.length;
                            break;
                        case Constants.RESPONSE_COMMANDS_SET_SOURCES:
                            var plates = command.plates;
                            for (var j=0; j<plates.length;j++) {
                                var plate = plates[j];
                                var source = returnEmptyPlate();

                                source.details.type = plate.type;
                                source.details.id = plate.details ? plate.details.id : null;

                                if (base.sources[j]) {
                                    if (base.sources[j].loaded || base.sources[j].updating) {
                                        //do nothing - this destination was already entered
                                    } else {
                                        source.details.id = base.sources[j].details ? base.sources[j].details.id : null;
                                        base.sources[j] = dest;
                                        base.addSource(j);
                                    }
                                } else {
                                    base.sources[j] = source;
                                }
                            }
                            if (base.sources.length > plates.length) {
                                base.sources.splice(plates.length - base.sources.length);
                            }
                            base.map.source.plateCount = base.sources.length;
                            break;
                        case Constants.RESPONSE_COMMANDS_PRESENT_DATA:
                            // assemble the presented data
                            presentedDataItems.push(command);
                            break;
                        case Constants.RESPONSE_COMMANDS_REQUEST_DATA:
                            // assemble the presented data
                            requestedDataItems.push(command);
                            break;

                        default :
                            console.log('Error: Unrecognized response command type = [' + command.type + ']');
                            break;
                    }


                }

                // present and request data after all other commands (such as SET_DESTINATIONS) are complete
                if (requestedDataItems.length) {
                    base.addRequestedDataItems(requestedDataItems);
                }

                if (presentedDataItems.length) {
                    base.addPresentedDataItems(presentedDataItems);
                }

            };

            base.serialize = function () {
                var sharedProps = ['type', 'title', 'description', 'notes'];
                var obj = {};

                for (var i = 0; i<sharedProps.length; i++) {
                    obj[sharedProps[i]] = base[sharedProps[i]];
                }

                obj.sources = angular.copy(base.sources);

                for (var i=0; i< obj.sources.length; i++) {
                    var plate = obj.sources[i];
                    delete plate.details.childPlates;
                    delete plate.details.parentPlates;
                    delete plate.details.parentToThisTaskName;
                    delete plate.details.thisToChildTaskName
                    if (plate.details.plateDetails) {
                        delete plate.details.plateDetails.dateCreatedFormatted;
                    }
                    delete plate.details.success;
                    delete plate.items;
                    delete plate.updating;
                    delete plate.loaded;
                    delete plate.details.title;
                }

                obj.destinations = angular.copy(base.destinations);

                for (var i=0; i< obj.destinations.length; i++) {
                    var plate = obj.destinations[i];
                    if (base.map.destination.plateTypeId) {
                        plate.details.plateDetails = {type: base.map.destination.plateTypeId};
                    }
                    delete plate.details.success;
                    delete plate.items;
                    delete plate.updating;
                    delete plate.loaded;
                    delete plate.details.title;
                }

                /* for NGS barcoding transforms, we need to add the source plate as the destination */
                if (base.details.transform_template_id == 30) {
                    obj.destinations = angular.copy(base.sources);
                }

                obj.operations = angular.copy(base.operations);
                obj.details = angular.copy(base.details);

                return JSON.stringify(obj);
            }

            var init = function () {
                return base;
            };

            return init();
        }

        var TransformSpecSource = function (kind) {
            var base = this;

            base.id = null;
            base.type = kind;
            base.details = {};
            base.items = [];
            base.loaded = false;

            switch (kind) {
                case Constants.SOURCE_TYPE_PLATE:
                    base.details = {
                        text: '',
                        title: ''
                    }
                    break;

                default :
                    console.log('Error: Unrecognized kind = [' + kind + ']');
                    break;
            }

            var init = function () {
                return base;
            };

            return init();
        }

        return {

            newTransformSpec: function () {
                return new TransformSpec();
            }
            ,newTransformSpecSource: function (kind) {
                return new TransformSpecSource(kind);
            }

        }

    }
]);
