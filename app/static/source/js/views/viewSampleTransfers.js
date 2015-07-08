/*************************************************************************************
 *
 * Copyright (c) 2015 Twist Bioscience
 *
 * File: app/static/source/js/views/editPlate.js
 * 
 *************************************************************************************/

var controller = (function() {


   function init() {
      

      $("table tbody tr td:nth-child(3)").each(function() {
         //alert("bla");
         var $td = $(this);
         var val = $td.text();
         if (val !== "") {
            //alert("TD: " + $td);
            //alert(val);
            // 2015-07-07 18:26:48.000051

            //var dateCreated = data.plateDetails.dateCreated;
            var momentDate = moment(val, "YYYY-MM-DD HH:mm:ss");
            var dateCreatedString = momentDate.format("dddd, MMMM Do YYYY, h:mm a");

            $td.text(dateCreatedString);

            //alert(dateCreatedString);

         }
      });
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