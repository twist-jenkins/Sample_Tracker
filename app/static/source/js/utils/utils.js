/*************************************************************************************
 *
 * Copyright (c) 2015 Twist Bioscience
 *
 * File: app/static/source/js/utils/utils.js
 *
 *************************************************************************************/

window.onerror = function(msg, url, line, col, error) {
   // Note that col & error are new to the HTML 5 spec and may not be 
   // supported in every browser.  It worked for me in Chrome.
   var extra = !col ? '' : '\ncolumn: ' + col;
   extra += !error ? '' : '\nerror: ' + error;

   // You can view the information in an alert to see things working like this:
   alert("Error: " + msg + "\nurl: " + url + "\nline: " + line + extra);

   // TODO: Report this error via ajax so you can keep track
   //       of what pages have JS issues

   var suppressErrorAlert = true;
   // If you return true, then error alerts (like in older versions of 
   // Internet Explorer) will be suppressed.
   return suppressErrorAlert;
};


var Twist = Twist || {};
Twist.Utils = (function() {



   function ajaxPost(url,data,callback) {

      

      $.ajax({
         type: "POST",
         contentType: "application/x-www-form-urlencoded; charset=UTF-8",
         url: url,
         data: data,
         success: function(data) {
            callback(data);
         },
         error: function(error) {
            alert("error " + JSON.stringify(error));
         },
         dataType: "json"
      });
   }

   function ajaxJsonPost(url,data,callback) {

      $.ajax({
         type: "POST",
         contentType: "application/json; charset=utf-8",
         url: url,
         data: data,
         success: function(data) {
            callback(data);
         },
         error: function(error) {
            alert("error " + JSON.stringify(error));
         },
         dataType: "json"
      });
      

    }

   function ajaxDelete(url,callback) {
         $.ajax({
            url: url,
            type: 'DELETE',
            success: function(data) {
               callback(data);
            },
            fail: function(error) {
               alert("ERROR: " + error);
            },
            error: function(error) {
               alert("ERROR: " + error);
            },
            dataType: "json"
         });
    }


   return {
      ajaxDelete:function(url,callback) {
         ajaxDelete(url,callback);
      },

      ajaxJsonPost:function(url,data,callback) {
         ajaxJsonPost(url,data,callback);
      },

      ajaxPost:function(url,data,callback) {
         ajaxPost(url,data,callback);
      },


   }

})();