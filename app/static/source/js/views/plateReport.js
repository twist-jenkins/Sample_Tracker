/*************************************************************************************
 *
 * Copyright (c) 2015 Twist Bioscience
 *
 * File: app/static/source/js/views/plateReport.js
 * 
 *************************************************************************************/

var controller = (function() {

   var m_parentPlateRowTemplateSource = $("#parentPlateRowTemplate").html();

   var m_parentPlateRowTemplate = Handlebars.compile(m_parentPlateRowTemplateSource);

   var m_samePlateRowTemplate = Handlebars.compile($('#samePlateRowTemplate').html());

   var m_wellRowTemplateSource = $("#wellRowTemplate").html();

   var m_wellRowTemplate = Handlebars.compile(m_wellRowTemplateSource);

   var m_getPlateReportUrl = $("#getPlateReportUrl").val();

   var m_plateReportUrl = $("#plateReportUrl").val();

   var m_sampleReportUrl = $("#sampleReportUrl").val();

   var m_getCSVPlateReportUrl = $("#getCSVPlateReportUrl").val();

   var m_errorPopup = new GenericPopup($("#errorPopup"));


   /**
    * Init the "type ahead" behavior in the sample plate barcode text field. As the user types, it goes out to the
    * database and returns a list of sample plate barcode values that contain the string the user has typed so far.
    *
    * https://github.com/biggora/bootstrap-ajax-typeahead
    */
   function initTypeahead() {

      var url = $("#getSampleBarcodesListUrl").val();

      $('#barcode').typeahead({
         ajax: url,
         items: 30
      });
   }



   function initForm() {

      //
      // This is where we grab the sample plate barcodes list that is used by the "type ahead" functionality.
      //
      initTypeahead();

      //
      // The "clear/reset the form" method.
      //
      function clearForm() {
         $('#barcode').val("");
         $("table tbody tr").remove();
         $("#exportAsExcel").addClass("hidden");
         $(".form-group.plateDetails, .form-group.parentPlates, .form-group.childPlates, .form-group.wells").addClass("hidden");
      }

      //
      // If the user clicks the little "x" in the text field where they enter the barcode, it resets the form.
      //
      $("#clearSearch").click(clearForm);

      //
      // The user clicked the "Search" button. Should be "Show Report"
      //
      function doSearch(e) {

         //e.stopImmediatePropagation();
         //e.preventDefault;
         //alert("E: " + e);


         //
         // Grab the report for the plate with the user-entered (or selected from dropdown) barcode.
         //
         var barcode = $.trim($("#barcode").val());
         if (barcode !== "") {

            $("table tbody tr").remove();

            var url = m_getPlateReportUrl.replace("/0", "/" + barcode);
            $.getJSON(url, function(data) {

               if (!data.success) {
                  m_errorPopup.show(data.errorMessage);
                  return;
               }

               //
               // Show stuff that is hidden if the user hasn't yet requested the report.
               //
               $("#exportAsExcel").removeClass("hidden");
               $(".form-group.plateDetails").removeClass("hidden");

               //
               // Update the UI with the data from the report.
               //

               //
               // REPORT HEADER
               //

               var dateCreated = data.plateDetails.dateCreated;
               var momentDate = moment(dateCreated, "YYYY-MM-DD HH:mm:ss");
               var dateCreatedString = momentDate.format("dddd, MMMM Do YYYY, h:mm a");

               $(".plateDetails span.dateCreated").text(dateCreatedString);
               $(".plateDetails span.createdBy").text(data.plateDetails.createdBy);



               //
               // PARENT PLATES
               //

               if (data.parentPlates.length) {

                  if (data.parentToThisTaskName) {
                     $(".parentPlates span.taskName").text(data.parentToThisTaskName);
                  }

                  _.each(data.parentPlates, function(parentPlate) {

                     var plateReportUrl = m_plateReportUrl.replace("/0", "/" + parentPlate.externalBarcode);

                     var dateCreated = parentPlate.dateCreated;
                     var momentDate = moment(dateCreated, "YYYY-MM-DD HH:mm:ss");
                     var dateCreatedString = momentDate.format("dddd, MMMM Do YYYY, h:mm a");

                     var context = {
                        plateBarcode: parentPlate.externalBarcode,
                        plateReportUrl: plateReportUrl,
                        plateCreationDateTime: dateCreatedString
                     };
                     var html = m_parentPlateRowTemplate(context);
                     $(".form-group.parentPlates").removeClass("hidden");
                     $(".form-group.parentPlates table tbody").append(html);
                  });

               } else {
                  $(".form-group.parentPlates").addClass("hidden");
               }

               

               //
               // CHILD PLATES
               //

               if (data.childPlates.length) {

                  if (data.thisToChildTaskName) {
                     $(".childPlates span.taskName").text(data.thisToChildTaskName);
                  }

                  var insertIntoBlock, rowML, samePlateSteps = 0, childPlateSteps = 0;

                  _.each(data.childPlates, function(childPlate) {

                     var plateReportUrl = m_plateReportUrl.replace("/0", "/" + childPlate.externalBarcode);

                     var dateCreated = childPlate.dateCreated;
                     var momentDate = moment(dateCreated, "YYYY-MM-DD HH:mm:ss");
                     var dateCreatedString = momentDate.format("dddd, MMMM Do YYYY, h:mm a");

                     var context = {
                        plateBarcode: childPlate.externalBarcode,
                        plateReportUrl: plateReportUrl,
                        plateCreationDateTime: dateCreatedString
                     };

                     //some "child plates" are actually just records for a step performed on the *same* plate
                     //we'll want to list these as Same-Plate Steps rather child plates
                     if (barcode === childPlate.externalBarcode) {
                        samePlateSteps++;
                        delete context.plateBarcode;
                        context.plateCreationDateTime = $(".form-group.samePlateSteps tr").length + '. ' + context.plateCreationDateTime;
                        insertIntoBlock = $(".form-group.samePlateSteps");
                        rowML = m_samePlateRowTemplate(context);
                        $(".form-group.samePlateSteps").removeClass("hidden");
                     } else {
                        childPlateSteps++;
                        insertIntoBlock = $(".form-group.childPlates");
                        rowML = m_parentPlateRowTemplate(context);
                        $(".form-group.childPlates").removeClass("hidden");
                     }

                     $('table tbody', insertIntoBlock).append(rowML);
                     
                  });

                  if (!samePlateSteps) {
                     $(".form-group.samePlateSteps").addClass("hidden");
                  }

                  if (!childPlateSteps) {
                     $(".form-group.childPlates").addClass("hidden");
                  }
   
               } else {
                  $(".form-group.samePlateSteps").addClass("hidden");
                  $(".form-group.childPlates").addClass("hidden");
               }


               //
               // "WELLS" IN THIS PLATE
               //

               _.each(data.wells, function(well) {
                  var sampleReportUrl = m_sampleReportUrl.replace("/0", "/" + well.sample_id);
                  var context = {
                     wellId: well.well_id,
                     columnAndRow: well.column_and_row,
                     sampleId: well.sample_id,
                     sampleReportUrl: sampleReportUrl
                  };
                  var html = m_wellRowTemplate(context);
                  $(".form-group.wells table tbody").append(html);
               });

            });

         }

         e.preventDefault();
         return false;
      }

      //
      // Set up the click handler for the "Show Report" button.
      //
      $("#search").click(doSearch);

      // 
      // Set up the click handler for the "Export as Excel" button.
      //
      // This opens a new browser tab and in that tab downloads the report as a .CSV file.
      //
      $("#exportAsExcel").click(function(e) {
         e.stopImmediatePropagation();
         e.preventDefault();

         var barcode = $.trim($("#barcode").val());
         if (barcode !== "") {
            var url = m_getCSVPlateReportUrl.replace("/0", "/" + barcode);
            window.open(url, "_blank");
         }
      });

      //alert("inited");
   }



   //
   // Init the page controller (and get data and such). If the URL used to bring up this page contained a barcode, then
   // the "barcode" text field has a value and clicking the "Show Report" button would cause a report to be shown
   // on the screen. So what we do is invoke a "click" handler for that button. If there is a barcode in the text field
   // (because it was passed via the URL), the the page goes out and gets the report and shows it. And if no barcode was
   // specified on the URL (and thus the text field is empty), then the click handler does nothing!
   //
   // Why do we do that click handler thingy? So that as soon as the page shows the report associated with the URL-passed-barcode
   // will show. This lets us have URLs throughout this app that the user can click and that cause a page+report to be shown
   // corresponding with the sample or plate the user clicked.
   //
   function init() {
      initForm();
      setTimeout(function() {
         $("#search").trigger("click");
      }, 0);
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