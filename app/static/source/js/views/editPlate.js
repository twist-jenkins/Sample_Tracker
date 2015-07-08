/*************************************************************************************
 *
 * Copyright (c) 2015 Twist Bioscience
 *
 * File: app/static/source/js/views/editPlate.js
 * 
 *************************************************************************************/

var controller = (function() {

   var m_getPlateByIdUrl = $("#getPlateByIdUrl").val();

   var m_samplePlateExternalBarcodeUrl = $("#samplePlateExternalBarcodeUrl").val();

   var m_barcodeUpdatedPopup = new GenericPopup($("#barcodeUpdatedPopup"));

   var m_errorPopup = new GenericPopup($("#errorPopup"));

   var m_previousSourcePlateId = null;

   //
   // Grab the plate id entered into the UI. If one was entered, make a JSON call to grab the plate's details,
   // and show those details onto the web page.
   //
   function getSelectedPlate() {

      var sourcePlateId = $('#sourcePlateId').val();

      if (m_previousSourcePlateId == sourcePlateId) {
         return;
      }

      //
      // Grab the data for the selected plate from the back end.
      //
      var url = m_getPlateByIdUrl.replace("/0", "/" + sourcePlateId);
      $.getJSON(url, function(data) {
         
         if (data.externalBarcode && data.externalBarcode !== "") {
            $("#externalBarcode").val(data.externalBarcode)
         } else {
            $("#externalBarcode").val("");
         }

         //
         // Update the screen.
         //

         var $form = $(".maincontent form");

         $(".form-group.name p", $form).text(data.name);
         $(".form-group.description p", $form).text(data.description);
         $(".form-group.samplePlateType p", $form).text(data.samplePlateType);
         $(".form-group.storageLocation p", $form).text(data.storageLocation);
         $(".form-group.status p", $form).text(data.status);
      });

      m_previousSourcePlateId = sourcePlateId;
   }

   /**
    * Init the "type ahead" behavior in the sample plate id text field. As the user types, it goes out to the
    * database and returns a list of sample plate id values that contain the string the user has typed so far.
    *
    * https://github.com/biggora/bootstrap-ajax-typeahead
    */
   function initTypeahead() {

      var url = $("#getSamplePlatesListUrl").val();

      var typeaheadSource = ['John', 'Alex', 'Terry'];

      $('#sourcePlateId').typeahead({
         ajax: url,
         items: 30
      });

      $('#sourcePlateId').change(function() {
         setTimeout(getSelectedPlate, 100);
      })
   }

   function clearForm() {
      $('#sourcePlateId').val("");
      $(".form-group p").text("");
   }


   function initForm() {

      //
      // This is where we grab the sample plate ids list that is used by the "type ahead" functionality.
      //
      initTypeahead();


      //
      // If the user clicks the little "x" in the text field where they enter the plate id, it resets the form.
      //
      $("#clearPlateId").click(function() {
         clearForm();
      });

      //
      // Set up the "Update Barcode" button click handler.
      //
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

         //
         // We send data to the back end and update the barcode for the selected plate (the plate id was entered
         // by the user as was the barcode).
         //
         var url = m_samplePlateExternalBarcodeUrl.replace("/0", "/" + sourcePlateId);
         var data = JSON.stringify({
            sample_plate_id: sourcePlateId,
            externalBarcode: externalBarcode
         });

         Twist.Utils.ajaxJsonPost(url, data, function(data) {
            if (data.success) {
               m_barcodeUpdatedPopup.showWithTimeout(1000);
            } else {
               m_errorPopup.show(data.errorMessage);
            }
         });
      });
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