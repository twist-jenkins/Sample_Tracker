
var controller = (function() {

   var m_parentPlateRowTemplateSource = $("#parentPlateRowTemplate").html();
   var m_parentPlateRowTemplate = Handlebars.compile(m_parentPlateRowTemplateSource);

   var m_wellRowTemplateSource = $("#wellRowTemplate").html();
   var m_wellRowTemplate = Handlebars.compile(m_wellRowTemplateSource);

    var m_getPlateReportUrl = $("#getPlateReportUrl").val();

    var m_plateReportUrl = $("#plateReportUrl").val();

    var m_sampleReportUrl = $("#sampleReportUrl").val();

    var m_getCSVPlateReportUrl = $("#getCSVPlateReportUrl").val();

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
    function initTypeahead() {

      var url = $("#getSampleBarcodesListUrl").val();



$('#barcode').typeahead({
    ajax: url,
    items:30
    //source: typeaheadSource
});

/*
$('#destinationPlateId').typeahead({
    ajax: url,
    items:30
    //source: typeaheadSource
});
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

        initTypeahead();

        function clearForm() {
           $('#barcode').val("");
           $("table tbody tr").remove();
           $("#exportAsExcel").addClass("hidden");
           $(".form-group.plateDetails, .form-group.parentPlates, .form-group.childPlates, .form-group.wells").addClass("hidden");
        }

        $("#clearSearch").click(clearForm);

        function doSearch(e) {

            //alert("do search");

            e.stopImmediatePropagation();
            e.preventDefault;
            //alert("E: " + e);
            var barcode = $.trim($("#barcode").val());
            if (barcode !== "") {

                $("table tbody tr").remove();

                //alert("do a search");

                var url = m_getPlateReportUrl.replace("/0","/" + barcode);
              //   alert(url);

                $.getJSON( url, function( data ) {

                   // alert("FOO");
                   // alert(JSON.stringify(data));
                   // return;

                    $("#exportAsExcel").removeClass("hidden");
                    $(".form-group.parentPlates, .form-group.wells").removeClass("hidden");
                    $(".form-group.childPlates, .form-group.wells").removeClass("hidden");
                    $(".form-group.plateDetails").removeClass("hidden");



                    var dateCreated = data.plateDetails.dateCreated;
                    var momentDate = moment(dateCreated, "YYYY-MM-DD HH:mm:ss");
                    var dateCreatedString = momentDate.format("dddd, MMMM Do YYYY, h:mm a");

                    $(".plateDetails span.dateCreated").text(dateCreatedString);

                    $(".plateDetails span.createdBy").text(data.plateDetails.createdBy);

                    if (data.parentToThisTaskName) {
                       $(".parentPlates span.taskName").text(data.parentToThisTaskName);
                    }

                    if (data.thisToChildTaskName) {
                       $(".childPlates span.taskName").text(data.thisToChildTaskName);
                    }
                    
                  /*
                  "parentToThisTaskName":parent_to_this_task_name,
        "childPlates":child_plates,
        "thisToChildTaskName":this_to_child_task_name,
        "wells":wells,
                  */



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

var m_parentPlateRowTemplateSource = $("#parentPlateRowTemplate").html();
   var m_parentPlateRowTemplate = Handlebars.compile(m_parentPlateRowTemplateSource);

   var m_wellRowTemplateSource = $("#wellRowTemplate").html();
   var m_wellRowTemplate = Handlebars.compile(m_wellRowTemplateSource);


   {"parentPlates":[],"wells":[{"column":-1,"row":"-1","sample_id":"OSA_546bc9677993058485ebe118","well_id":2},{"column":-1,"row":"-1","sample_id":"OSA_546bc9677993058485ebe119","well_id":3},{"column":-1,"row":"-1","sample_id":"OSA_546bc9677993058485ebe11a","well_id":4}]}


    <td>{{plateBarcode}}</td>
      <td>{{plateCreationDateTime}}</td>
   </tr>
</script>
<script id="wellRowTemplate" type="text/x-handlebars-template">
   <tr>
      <td>{{wellId}}</td>
      <td>{{column}}</td>
      <td>{{row}}</td>
      <td>{{sampleId}}</td>

*/

                  if (data.parentPlates.length == 0) {
                      $(".form-group.parentPlates").addClass("hidden");
                  } else {
                    _.each(data.parentPlates,function(parentPlate) {

                         var plateReportUrl = m_plateReportUrl.replace("/0","/" + parentPlate.externalBarcode);

                         var dateCreated = parentPlate.dateCreated;
                         var momentDate = moment(dateCreated, "YYYY-MM-DD HH:mm:ss");
                         var dateCreatedString = momentDate.format("dddd, MMMM Do YYYY, h:mm a");

                         var context = {
                            plateBarcode:parentPlate.externalBarcode,
                            plateReportUrl:plateReportUrl,
                            plateCreationDateTime:dateCreatedString
                         };
                         var html = m_parentPlateRowTemplate(context);
                         $(".form-group.parentPlates table tbody").append(html);

                        
                    });
                  }

                  if (data.childPlates.length == 0) {
                      $(".form-group.childPlates").addClass("hidden");
                  } else {

                    _.each(data.childPlates,function(childPlate) {

                         var plateReportUrl = m_plateReportUrl.replace("/0","/" + childPlate.externalBarcode);

                         var dateCreated = childPlate.dateCreated;
                         var momentDate = moment(dateCreated, "YYYY-MM-DD HH:mm:ss");
                         var dateCreatedString = momentDate.format("dddd, MMMM Do YYYY, h:mm a");

                         var context = {
                            plateBarcode:childPlate.externalBarcode,
                            plateReportUrl:plateReportUrl,
                            plateCreationDateTime:dateCreatedString
                         };
                         var html = m_parentPlateRowTemplate(context);
                         $(".form-group.childPlates table tbody").append(html);
                    });
                  }

                  _.each(data.wells,function(well) {

                       var sampleReportUrl = m_sampleReportUrl.replace("/0","/" + well.sample_id);

                       var context = {
                          wellId:well.well_id,
                          column:well.column,
                          row:well.row,
                          sampleId:well.sample_id,
                          sampleReportUrl:sampleReportUrl
                       };
                       var html = m_wellRowTemplate(context);
                       $(".form-group.wells table tbody").append(html);
                  });
                   
                   
                 //  alert("DATA: " + data);
                  // alert(JSON.stringify(data));

                    /*
                   _.each(data,function(row) {
                      //alert("EACH: " + a + " " + b );

                      //  alert("row.column: " + row.column);

                       var context = {
                          barcode:row.destination_plate_barcode,
                          wellId:row.well_id,
                          column:row.column,
                          row:row.row,
                          task:row.task
                       };

                       var html = m_tableRowTemplate(context);

                       $("table  tbody").append(html);

                   });
                */





                });


            }

            e.preventDefault();
            return false;
        }
        $("#search").click(doSearch);

        // getCSVPlateReportUrl

        $("#exportAsExcel").click(function(e) {

            e.stopImmediatePropagation();
            e.preventDefault();

            var barcode = $.trim($("#barcode").val());

            if (barcode !== "") {
               var url = m_getCSVPlateReportUrl.replace("/0","/" + barcode);

              // alert(url);

               window.open(url,"_blank");
            }

        });

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
                m_errorPopup.show("Please select a source barcode");
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

      //  alert("init plate report");
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