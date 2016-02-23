var api_base_url = '/api/v1/';
var server_url = twist_api_url;

angular.module('twist.app').factory('Constants',[
    function () {
        return {
            PLATE_SOURCE: 'source'
            ,PLATE_DESTINATION: 'destination'
            ,STEP_TYPE_DROPDOWN_LABEL: 'Select a Step'
            ,USER_SPECIFIED_TRANSFORM_TYPE: 'user_specified'
            ,STANDARD_TEMPLATE: 'standard_template'
            ,FILE_UPLOAD: 'file_upload'
            ,TRANSFORM_SPEC_TYPE_PLATE_PLANNING: 'PLATE_PLANNING'
            ,TRANSFORM_SPEC_TYPE_PLATE_STEP: 'plate_step'
            ,SOURCE_TYPE_PLATE: 'plate'
            ,HAMILTON_OPERATION: 'hamilton'
            ,HAMILTON_TRANSFORM_TYPE: 'hamilton'
            ,HAMILTON_CARRIER_BARCODE_PREFIX: 'CARR'
            ,HAMILTON_CARRIER_POSITION_BARCODE_PREFIX: 'CARP'
            ,HAMILTON_PLATE_BARCODE_PREFIX: 'PLT'
            ,HAMILTON_ELEMENT_CARRIER: 'carrier'
            ,HAMILTON_ELEMENT_CARRIER_POSITION: 'carrier-position'
            ,HAMILTON_ELEMENT_PLATE: 'plate'
            ,SHIPPING_TUBES_CARRIER_TYPE: '96_TUBE'
            ,SHIPPING_TUBE_PLATE_TYPE: 'SHIPPING_TUBE_PLATE'
            ,RESPONSE_COMMANDS_SET_DESTINATIONS: 'SET_DESTINATIONS'
            ,RESPONSE_COMMANDS_SET_SOURCES: 'SET_SOURCES'
            ,RESPONSE_COMMANDS_ADD_TRANSFORM_SPEC_DETAIL: 'ADD_TRANSFORM_SPEC_DETAIL'
            ,RESPONSE_COMMANDS_PRESENT_DATA: 'PRESENT_DATA'
            ,RESPONSE_COMMANDS_REQUEST_DATA: 'REQUEST_DATA'
            ,DATA_TYPE_TEXT: 'text'
            ,DATA_TYPE_FILE_DATA: 'file-data'
            ,DATA_TYPE_LINK: 'link'
            ,DATA_TYPE_ARRAY: 'array'
            ,DATA_TYPE_BARCODE: 'barcode'
            ,DATA_TYPE_RADIO: 'radio'
            ,DATA_TYPE_CSV: 'csv'
            ,BARCODE_PREFIX_PLATE: 'p'
            ,BARCODE_TYPE_PLATE: 'PLATE'
            ,BARCODE_TYPE_INSTRUMENT: 'INSTRUMENT'
            ,BARCODE_TYPE_CARRIER: 'CARRIER'
            ,BARCODE_TYPE_CARTRIDGE: 'CARTRIDGE'
            ,BARCODE_TYPE_FLOWCELL: 'FLOWCELL'
            ,INSTRUMENT_TYPE_HAMILTON: 'HAMILTON'
            ,INSTRUMENT_TYPE_SEQUENCER: 'SEQUENCER'
            ,INSTRUMENT_TYPE_ECHO: 'ECHO'
            ,INSTRUMENT_TYPE_THERMOCYCLER: 'THERMOCYCLER'

        };
    }]
);
