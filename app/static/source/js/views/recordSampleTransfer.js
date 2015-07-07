/*************************************************************************************
 *
 * Copyright (c) 2015 Twist Bioscience
 *
 * File: app/static/source/js/views/recordSampleTransfer.js
 * 
 *************************************************************************************/
 
Dropzone.autoDiscover = false;

var controller = (function() {

   var m_tableRowTemplateSource = $("#tableRowTemplate").html();
   var m_tableRowTemplate = Handlebars.compile(m_tableRowTemplateSource);

   var m_sampleTransferTypeDropdown = new DropDownButton($("#sampleTransferTypeDropDown"), $("#sampleTransferTypeDropDown .selectedItemId"));
   
   var m_errorPopup = new GenericPopup($("#errorPopup"));
   
   var m_createSampleMovementUrl = $("#createSampleMovementUrl").val();

   //
   // Init the widget where the user drags-and-drops the XLS file that specifies the well-by-well transfers to do.
   //
   function initDropzone() {

      var url = $("#dragndropurl").val();

      var myDropZone = new FileDropZone("div#dropzone", url);

      var hasError = false;

      myDropZone.on("sending", function() {
         hasError = false;
      });

      myDropZone.on("complete", function(file) {
         $("div#dropzone").addClass("hidden");
         $("#simplemovefields").addClass("hidden");
         $("#dragndropmovefields em").addClass("hidden");

         $("table#spreadsheet").removeClass("hidden");

         if (hasError) {
            return;
         }
      });

      myDropZone.on("error", function(e, errorMessage) {
         e.stopImmediatePropagation();
         alert(errorMessage);
         hasError = true;
      });

      //
      // Once the file has been uploaded to the server, output to the screen a table that contains the values
      // that were extracted from the file.
      //
      // This is to allow the user to view what they've uploaded - giving them a chance to realize they made a mistake
      // or validating that their data was exactly what they intended to upload.
      //
      myDropZone.on("success", function(e, responseJson) {
         e.stopImmediatePropagation();

         _.each(responseJson.task_items, function(task_item) {
            var context = {
               sourcePlateBarcode: task_item.source_plate_barcode,
               sourceWellId: task_item.source_well_id,
               sourceColAndRow: task_item.source_col_and_row,
               destinationPlateType: task_item.destination_plate_type_name,
               destinationPlateBarcode: task_item.destination_plate_barcode,
               destinationWellId: task_item.destination_well_id,
               destinationColAndRow: task_item.destination_col_and_row

            }
            var html = m_tableRowTemplate(context);

            $("table#spreadsheet tbody").append(html);
         });
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

      //
      // The user clicked the "submit" button. Now determine whether the user simply entered source and destination
      // barcodes for sample plates or used the "upload" widget to upload a spreadsheet where each row in the
      // spreadsheet represents a well-to-well transfer from a source plate to a destination plate.
      //
      function submitForm() {

         var useSpreadsheetData = !$("table#spreadsheet").hasClass("hidden");

         var sampleTransferTypeId = m_sampleTransferTypeDropdown.val();
         var sourceBarcodeId = null,
            destinationBarcodeId = null;
         var postData = null;

         if (sampleTransferTypeId === "") {
            m_errorPopup.show("Please specify a transfer type.");
            return;
         }

         postData = {
            sampleTransferTypeId: sampleTransferTypeId
         }

         //
         // If the user dragged-and-dropped a spreadsheet, package all the rows of data into the "postData" 
         // object.
         //
         if (useSpreadsheetData) {
            postData.wells = [];
            $("table#spreadsheet tbody tr").each(function() {
               var $tr = $(this);
               var oneWell = {
                  sourcePlateBarcode: $.trim($("td:eq(0)", $tr).text()),
                  sourceWellId: $.trim($("td:eq(1)", $tr).text()),
                  sourceColAndRow: $.trim($("td:eq(2)", $tr).text()),
                  destinationPlateType: $.trim($("td:eq(3)", $tr).text()),
                  destinationPlateBarcode: $.trim($("td:eq(4)", $tr).text()),
                  destinationWellId: $.trim($("td:eq(5)", $tr).text()),
                  destinationColAndRow: $.trim($("td:eq(6)", $tr).text())
               }
               postData.wells.push(oneWell);
            });

         //
         // If the user didn't drag-and-drop a spreadsheet, copy the barcodes the user entered into the
         // two fields at the top of the form.
         //
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

         //
         // POST the data to the server. Once this returns the server will have created one or more new "sample_plate"
         // rows, a new "sample_plate_layout" row for each destination well that was populated, a "sample_transfer"
         // row representing the transfer the user did, and a "sample_transfer_detail" row for each well-to-well
         // transfer that occurred.
         //
         var data = JSON.stringify(postData);

         Twist.Utils.ajaxJsonPost(m_createSampleMovementUrl, data, function(data) {
            if (data.success) {
               resetForm();

               //
               // NOT AN ERROR! JUST REUSING THE DIALOG/POPUP.
               //
               m_errorPopup.show("Sample transfer was saved.");
            }
         });
      }

      $("form div.buttonsholder .reset").click(function(e) {
         resetForm();
      });

      $("form div.buttonsholder .submit").click(function(e) {
         submitForm();
      });

   }


   /**
   * Init the "type ahead" behavior in the source plate barcode text field. As the user types, it goes out to the
   * database and returns a list of plate barcode values that contain the string the user has typed so far.
   *
   * https://github.com/biggora/bootstrap-ajax-typeahead
   */
   function initTypeahead() {
      var url = $("#getSampleBarcodesListUrl").val();
      $('#sourceBarcodeId').typeahead({
         ajax: url,
         items: 30
      });
   }

   function init() {
      initDropzone();
      initForm();
      initTypeahead();
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