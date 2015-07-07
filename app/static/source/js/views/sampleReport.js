/*************************************************************************************
 *
 * Copyright (c) 2015 Twist Bioscience
 *
 * File: app/static/source/js/views/sampleReport.js
 * 
 *************************************************************************************/

var controller = (function() {

   var m_tableRowTemplateSource = $("#tableRowTemplate").html();

   var m_tableRowTemplate = Handlebars.compile(m_tableRowTemplateSource);

   var m_getSampleReportUrl = $("#getSampleReportUrl").val();

   var m_plateReportUrl = $("#plateReportUrl").val();

   var m_getCSVSampleReportUrl = $("#getCSVSampleReportUrl").val();


   /**
   * Init the "type ahead" behavior in the sample id text field. As the user types, it goes out to the
   * database and returns a list of sample id values that contain the string the user has typed so far.
   *
   * https://github.com/biggora/bootstrap-ajax-typeahead
   */
   function initTypeahead(data) {
      $('#sampleId').typeahead({
         source: data
      });
   }


   function initForm() {

      //
      // This is where we grab the sample id's list that is used by the "type ahead" functionality.
      //
      var getSampleIdsUrl = $("#getSampleIdsUrl").val();
      $.getJSON(getSampleIdsUrl, function(data) {
         initTypeahead(data);
      });

      //
      // The "clear/reset the form" method.
      //
      function clearForm() {
         $("#sampleId").val("");
         $("table tbody tr").remove();
         $("table").addClass("hidden");
         $("#exportAsExcel").addClass("hidden");
      }

      //
      // If the user clicks the little "x" in the text field where they enter the sample id, it resets the form.
      //
      $("#clearSearch").click(clearForm);

      //
      // The user clicked the "Search" button. Should be "Show Report"
      //
      function doSearch(e) {

         //e.stopImmediatePropagation();
         //e.preventDefault;
         
         //
         // Grab the report for the user-entered (or selected from dropdown) sample id.
         //
         var sampleId = $.trim($("#sampleId").val());
         if (sampleId !== "") {

            $("table tbody tr").remove();

            var url = m_getSampleReportUrl.replace("/0", "/" + sampleId);
            $.getJSON(url, function(data) {

               //
               // Show stuff that is hidden if the user hasn't yet requested the report.
               //
               $("table").removeClass("hidden");
               $("#exportAsExcel").removeClass("hidden");

               //
               // Update the UI with the data from the report.
               //
               _.each(data, function(row) {
                  var plateReportUrl = m_plateReportUrl.replace("/0", "/" + row.destination_plate_barcode);
                  var context = {
                     barcode: row.destination_plate_barcode,
                     platePageUrl: plateReportUrl,
                     wellId: row.well_id,
                     column: row.column,
                     row: row.row,
                     task: row.task
                  };
                  var html = m_tableRowTemplate(context);
                  $("table  tbody").append(html);
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
         e.preventDefault();
         var sampleId = $.trim($("#sampleId").val());
         if (sampleId !== "") {
            var url = m_getCSVSampleReportUrl.replace("/0", "/" + sampleId);
            window.open(url, "_blank");
         }
      });
   }

   //
   // Init the page controller (and get data and such). If the URL used to bring up this page contained a sample id, then
   // the "sample id" text field has a value and clicking the "Show Report" button would cause a report to be shown
   // on the screen. So what we do is invoke a "click" handler for that button. If there is a sample id in the text field
   // (because it was passed via the URL), the the page goes out and gets the report and shows it. And if no sample id was
   // specified on the URL (and thus the text field is empty), then the click handler does nothing!
   //
   // Why do we do that click handler thingy? So that as soon as the page shows the report associated with the URL-passed-id
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