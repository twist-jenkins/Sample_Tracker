
Dropzone.autoDiscover = false;

var controller = (function() {

   var m_tableRowTemplateSource = $("#tableRowTemplate").html();
   var m_tableRowTemplate = Handlebars.compile(m_tableRowTemplateSource);
   var m_sampleTransferTypeDropdown = new DropDownButton($("#sampleTransferTypeDropDown"),$("#sampleTransferTypeDropDown .selectedItemId"));
   var m_errorPopup = new GenericPopup($("#errorPopup"));
   var m_createSampleMovementUrl = $("#createSampleMovementUrl").val();

   function initDropzone() {

      //$("div#dropzone").dropzone({ url: "/file/post" });
     // return;

      var url = $("#dragndropurl").val();
    //  alert(url);

      var myDropZone = new FileDropZone("div#dropzone", url);

      var hasError = false;

      myDropZone.on("sending",function() {
         hasError = false;
      });

      myDropZone.on("complete", function(file) {

          $("div#dropzone").addClass("hidden");
          $("#simplemovefields").addClass("hidden");
          $("#dragndropmovefields em").addClass("hidden");

          $("table#spreadsheet").removeClass("hidden");

          //alert("complete");

         //location.reload();

            //alert("COMPLETE");

            //alert("COMPLETE IN MAIN");

            if (hasError) {
               return;
            }

            //var sequencesUploadedPopup = new GenericPopup($("#customerAndOrderUploadedPopup"));
            //sequencesUploadedPopup.show();
             
            //sequencesUploadedPopup.on("closed",function() {
            //   location.reload();
            //});

      });

      myDropZone.on("error", function(e,errorMessage) {
         //e.preventDefault();
         e.stopImmediatePropagation();
         alert(errorMessage);
         hasError = true;
      });

      myDropZone.on("success", function(e,responseJson) {
         //e.preventDefault();
         e.stopImmediatePropagation();
         //alert(JSON.stringify(responseJson));


/*
 <td>{{sourcePlateId}}</td>
      <td>{{sourceWell}}</td>
      <td>{{destinationPlateId}}</td>
      <td>{{destinationWell}}</td>
*/


        //alert("responseJson.task_items: " + JSON.stringify(responseJson.task_items));
        //return;

/*
<!--
   "source_plate_barcode":worksheet.cell_value(curr_row,0),
                "source_well_id":worksheet.cell_value(curr_row,1),
                "source_col_and_row":worksheet.cell_value(curr_row,2),
                "destination_plate_type_name":worksheet.cell_value(curr_row,3),
                "destination_plate_barcode":worksheet.cell_value(curr_row,4),
                "destination_well_id":worksheet.cell_value(curr_row,5),
                "destination_col_and_row":worksheet.cell_value(curr_row,6)
-->

{% raw %}
<script id="tableRowTemplate" type="text/x-handlebars-template">
   <tr>
      <td>{{sourcePlateBarcode}}</td>
      <td>{{}}</td>
      <td>{{}}</td>
      <td>{{}}</td>
      <td>{{}}</td>
      <td>{{}}</td>
      <td>{{}}</td>
   </tr>
</script>
*/

         _.each(responseJson.task_items,function(task_item) {
            

            // $("table#spreadsheet tbody 

            var context = {
                sourcePlateBarcode:task_item.source_plate_barcode,
                sourceWellId:task_item.source_well_id,
                sourceColAndRow:task_item.source_col_and_row,
                destinationPlateType:task_item.destination_plate_type_name,
                destinationPlateBarcode:task_item.destination_plate_barcode,
                destinationWellId:task_item.destination_well_id,
                destinationColAndRow:task_item.destination_col_and_row

            }
           // alert("CONTEXT: " + JSON.stringify(context));
            //alert("task_item.source_plate_id: " + task_item.source_plate_id );
            var html = m_tableRowTemplate(context);
            //alert(html);
            $("table#spreadsheet tbody").append(html);
         });


         /*
               var context = {
         message: this.errors.message
      };
      var html = this.htmlHemplate(context);
         */

         //hasError = true;
      });

   }

    function initForm() {

        function resetForm() {

          m_sampleTransferTypeDropdown.reset();

          $("#sourceBarcodeId").val("");
          $("#destinationBarcodeId").val("");

          $("div#dropzone").removeClass("hidden");
          $("#simplemovefields").removeClass("hidden");
          $("#dragndropmovefields em").removeClass("hidden");

          $("table#spreadsheet").addClass("hidden");

          $("table#spreadsheet tbody tr").remove();

        }

        function submitForm() {
            var useSpreadsheetData = !$("table#spreadsheet").hasClass("hidden");

            //alert("useSpreadsheetData: " + useSpreadsheetData);

            var sampleTransferTypeId = m_sampleTransferTypeDropdown.val();
            var sourceBarcodeId = null, destinationBarcodeId = null;
            var postData = null;

            if (sampleTransferTypeId === "") {
               m_errorPopup.show("Please specify a transfer type.");
               return;
            }

            postData = {
               sampleTransferTypeId:sampleTransferTypeId
            }

/*
 "source_plate_barcode":worksheet.cell_value(curr_row,0),
                "source_well_id":worksheet.cell_value(curr_row,1),
                "source_col_and_row":worksheet.cell_value(curr_row,2),
                "destination_plate_type_name":worksheet.cell_value(curr_row,3),
                "destination_plate_barcode":worksheet.cell_value(curr_row,4),
                "destination_well_id":worksheet.cell_value(curr_row,5),
                "destination_col_and_row":worksheet.cell_value(curr_row,6)
*/

            if (useSpreadsheetData) {
               postData.wells = [];
               $("table#spreadsheet tbody tr").each(function() {
                  var $tr = $(this);
                  var oneWell = {
                     sourcePlateBarcode:$.trim($("td:eq(0)",$tr).text()),
                     sourceWellId:$.trim($("td:eq(1)",$tr).text()),
                     sourceColAndRow:$.trim($("td:eq(2)",$tr).text()),
                     destinationPlateType:$.trim($("td:eq(3)",$tr).text()),
                     destinationPlateBarcode:$.trim($("td:eq(4)",$tr).text()),
                     destinationWellId:$.trim($("td:eq(5)",$tr).text()),
                     destinationColAndRow:$.trim($("td:eq(6)",$tr).text())
                  }
                  postData.wells.push(oneWell);
               });
            } else {
               sourceBarcodeId = $.trim($("#sourceBarcodeId").val());
               destinationBarcodeId = $.trim($("#destinationBarcodeId").val());

               if (sourceBarcodeId === "" || destinationBarcodeId === "") {
                 m_errorPopup.show("Please specify a source plate id and a destination plate id.");
                 return;                  
               }

               postData.sourceBarcodeId = sourceBarcodeId;
               postData.destinationBarcodeId = destinationBarcodeId;

            }

           // alert("post data: " + postData);
           // alert(JSON.stringify(postData));

           // alert("URL: " + m_createSampleMovementUrl);

            var data = JSON.stringify(postData);

            Twist.Utils.ajaxJsonPost(m_createSampleMovementUrl,data,function(data) {

               //alert("SUCCESS: " + data.success);

               if (data.success) {
                  resetForm();
                  m_errorPopup.show("Sample transfer was saved.");
               }

              // alert("RESPONDED: " + data);
              // alert(JSON.stringify(data));

               //callback(data.error,data.errors,data.sequenceStatistics);
            });

/*
      var data = JSON.stringify({
         sequence: sequence,
      });

      Twist.Utils.ajaxJsonPost(this.validateOneSequenceUrl,data,function(data) {
         callback(data.error,data.errors,data.sequenceStatistics);
      });
*/

            
        }


        /*
        buttonsholder
        */

        $("form div.buttonsholder .reset").click(function(e) {
            resetForm();
        });

        $("form div.buttonsholder .submit").click(function(e) {
            submitForm();
        });

    }

    /**
    * https://github.com/biggora/bootstrap-ajax-typeahead
    */
    function initTypeahead() {

      var url = $("#getSampleBarcodesListUrl").val();

var typeaheadSource = ['John', 'Alex', 'Terry'];

$('#sourceBarcodeId').typeahead({
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

    function init() {
       // alert("init");
        
        initDropzone();
        initForm();
        initTypeahead();

       // alert("foo");
       

       // alert("well?");
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