
var controller = (function() {

   var m_tableRowTemplateSource = $("#tableRowTemplate").html();
   var m_tableRowTemplate = Handlebars.compile(m_tableRowTemplateSource);

    var m_getSampleReportUrl = $("#getSampleReportUrl").val();

    var m_plateReportUrl = $("#plateReportUrl").val();

    /*
    var m_samplePlateExternalBarcodeUrl = $("#samplePlateExternalBarcodeUrl").val();
    var m_barcodeUpdatedPopup = new GenericPopup($("#barcodeUpdatedPopup"));
    var m_errorPopup = new GenericPopup($("#errorPopup"));

    var m_previousSourcePlateId = null;
    */



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
    function initTypeahead(data) {

      //var url = $("#getSamplePlatesListUrl").val();

       // var typeaheadSource = ['John', 'Alex', 'Terry'];

       $('#sampleId').typeahead({
          source:data
       });

     //  alert("inited");

/*
        $('#sourcePlateId').typeahead({
            ajax: url,
            items:30
            //source: typeaheadSource
        });

        $('#sourcePlateId').change(function() {
            setTimeout(getSelectedPlate,100);
        })
  */

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

        var getSampleIdsUrl = $("#getSampleIdsUrl").val();

        $.getJSON( getSampleIdsUrl, function( data ) {
           //alert("the ids are here");
           initTypeahead(data);
        });

        function clearForm() {
           $("#sampleId").val("");
           $("table tbody tr").remove();
           $("table").addClass("hidden");
        }

        $("#clearSearch").click(clearForm);

        function doSearch(e) {
            e.stopImmediatePropagation();
            e.preventDefault;
            //alert("E: " + e);
            var sampleId = $.trim($("#sampleId").val());
            if (sampleId !== "") {

                $("table tbody tr").remove();

                //alert("do a search");

                var url = m_getSampleReportUrl.replace("/0","/" + sampleId);
              //   alert(url);

                $.getJSON( url, function( data ) {

                    $("table").removeClass("hidden");

/*
            var context = {
                sourceBarcodeId:task_item.source_plate_id,
                sourceWell:task_item.source_well,
                destinationBarcodeId:task_item.destination_plate_id,
                destinationWell:task_item.destination_well
            }
           // alert("CONTEXT: " + JSON.stringify(context));
            //alert("task_item.source_plate_id: " + task_item.source_plate_id );
            var html = m_tableRowTemplate(context);
            //alert(html);
            $("table#spreadsheet tbody").append(html);

 <td>{{barcode}}</td>
      <td>{{wellId}}</td>
      <td>{{wellColumn}}</td>
      <td>{{wellRow}}</td>
      <td>{{task}}</td>

*/

                   
                   
                 //  alert("DATA: " + data);
                  // alert(JSON.stringify(data));

                   _.each(data,function(row) {
                      //alert("EACH: " + a + " " + b );

                      //  alert("row.column: " + row.column);

                       var plateReportUrl = m_plateReportUrl.replace("/0","/" + row.destination_plate_barcode);

                       var context = {
                          barcode:row.destination_plate_barcode,
                          platePageUrl:plateReportUrl,
                          wellId:row.well_id,
                          column:row.column,
                          row:row.row,
                          task:row.task
                       };

                       var html = m_tableRowTemplate(context);

                       $("table  tbody").append(html);

                   });





                });


            }

            e.preventDefault();
            return false;
        }
        $("#search").click(doSearch);

        //alert("inited");
    }

    function initFormOld() {
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
        //alert("init");
        initForm();

        setTimeout(function() {
           $("#search").trigger("click");
        },0);

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