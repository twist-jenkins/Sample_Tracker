
var controller = (function() {

    var m_getPlateByIdUrl = $("#getPlateByIdUrl").val();
    var m_samplePlateExternalBarcodeUrl = $("#samplePlateExternalBarcodeUrl").val();
    var m_barcodeUpdatedPopup = new GenericPopup($("#barcodeUpdatedPopup"));
    var m_errorPopup = new GenericPopup($("#errorPopup"));

    var m_previousSourcePlateId = null;

    function getSelectedPlate() {

        var sourcePlateId = $('#sourcePlateId').val();

        if (m_previousSourcePlateId == sourcePlateId) {
            return;
        }

        

       // alert("get selected plate");
        var url = m_getPlateByIdUrl.replace("/0","/" + sourcePlateId);

        $.getJSON( url, function( data ) {
            //alert("DATA: " + data);
            //alert(JSON.stringify(data));

            var $form = $(".maincontent form");

            $(".form-group.name p",$form).text(data.name);
            $(".form-group.description p",$form).text(data.description);
            $(".form-group.samplePlateType p",$form).text(data.samplePlateType);
            $(".form-group.storageLocation p",$form).text(data.storageLocation);
            $(".form-group.status p",$form).text(data.status);






        });

        m_previousSourcePlateId = sourcePlateId;

       // alert(url);

       // alert("well?");

        /*
        $.getJSON( "ajax/test.json", function( data ) {
            */
    }

    /**
    * https://github.com/biggora/bootstrap-ajax-typeahead
    */
    function initTypeahead() {

      var url = $("#getSamplePlatesListUrl").val();

        var typeaheadSource = ['John', 'Alex', 'Terry'];

        $('#sourcePlateId').typeahead({
            ajax: url,
            items:30
            //source: typeaheadSource
        });

        $('#sourcePlateId').change(function() {
            setTimeout(getSelectedPlate,100);
        })
    }

    function clearForm() {
        $('#sourcePlateId').val("");

        $(".form-group p").text("");
    }

/*
            var data = JSON.stringify(postData);

            Twist.Utils.ajaxJsonPost(m_createSampleMovementUrl,data,function(data) {
               alert("RESPONDED: " + data);
               alert(JSON.stringify(data));

               //callback(data.error,data.errors,data.sequenceStatistics);
            });

{
   "status": "disposed",
   "sample_plate_id": "SPLT_5487897279930593d6805acc",
   "storage_location": "OPEN: CHIP LAB",
   "external_barcode": null,
   "name": "SRN_000180 OEX Plate 3",
   "description": "SRN_000180 Oligo Extraction Plate: 3",
   "sample_plate_type": "30 well, plastic (Twist NW)"
}
*/

    function initForm() {
        initTypeahead();
        $("#clearPlateId").click(function() {
            clearForm();
        });

        $(".maincontent form .buttonsholder button").click(function() {

            var sourcePlateId = $('#sourcePlateId').val();
            var externalBarcode = $("#externalBarcode").val();

            if ($.trim(sourcePlateId) === "") {
                m_errorPopup.show("Please select a source plate id");
                return;
            }

            if ($.trim(externalBarcode) === "") {
                m_errorPopup.show("Please specify a barcode");
                return;
            }

            var url = m_samplePlateExternalBarcodeUrl.replace("/0","/" + sourcePlateId);
           // alert(url);

           // alert("externalBarcode: " + externalBarcode);


            var data = JSON.stringify({
                sample_plate_id:sourcePlateId,
                externalBarcode:externalBarcode
            });

            Twist.Utils.ajaxJsonPost(url,data,function(data) {

                m_barcodeUpdatedPopup.showWithTimeout(1000);

              // alert("RESPONDED: " + data);
               //alert(JSON.stringify(data));

               //callback(data.error,data.errors,data.sequenceStatistics);
            });

        })
    }


    function init() {
        
        initForm();
    }


   return {
      init: function() {
         init();
      }
   }
})();

$(function() {
   controller.init();
});