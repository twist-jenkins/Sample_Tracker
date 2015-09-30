/*************************************************************************************
 *
 * Copyright (c) 2015 Twist Bioscience
 *
 * File: app/static/source/js/components/fileDropZone.js
 * 
 *************************************************************************************/
 
var FileDropZone = (function() {

   // var myDropzone = new Dropzone("div#myId", { url: "/file/post"});
   function FileDropZone(divId, url) {
      this.divId = divId;
      this.url = url;
      this.$elem = $(divId);
      this.init();
   }

   FileDropZone.prototype.init = function() {

      //$("div#dropzone").dropzone({ url: "/file/post" });

     // $("div#dropzone").dropzone({ url: "/file/post" });

      var myDropzone = new Dropzone(
         this.divId, { url: this.url}
      );

      var fireEvent = function(eventType,extraParms) {
         this.$elem.trigger(eventType,extraParms);
      }.bind(this);

      myDropzone.on("addedfile", function(file) {});

      myDropzone.on("dragenter", function(file) {
         this.$elem.addClass("dragover");
      }.bind(this));
      myDropzone.on("dragover", function(file) {
         this.$elem.addClass("dragover");
      }.bind(this));

      myDropzone.on("dragleave", function(file) {
         this.$elem.removeClass("dragover");
      }.bind(this));
      myDropzone.on("dragend", function(file) {
         this.$elem.removeClass("dragover");
      }.bind(this));
      myDropzone.on("drop", function(file) {
         this.$elem.removeClass("dragover");
      }.bind(this));

      myDropzone.on("sending",function() {
         fireEvent("sending");
         //alert("sending");
      });

      myDropzone.on("complete", function(file,other) {
        // alert("complete");
        // alert("OTHER: " + other);
         myDropzone.removeFile(file);
         fireEvent("complete");
      });


/*
this.emit("error", file, message, xhr);
*/

      myDropzone.on("error", function(file, message, xhr) { 
         //alert("IN FILE DROPZONE Error!");
         //alert("IN FILE DROPZONE message: " + message); 
         fireEvent("error", message);
      });

// this.emit("success", file, responseText, e);

      myDropzone.on("success", function(file, responseJson, e) { 
         //alert("success");
         
         if (!responseJson.success) {
            fireEvent("error", responseJson.errorMessage);
         } else {
            fireEvent("success", responseJson);
         }

         /*
         {"errorMessage":"'ascii' codec can't encode characters in position 3-4: ordinal not in range(128)","success":false}
         */
      });

     // alert("registered success handler");
      
   }

   FileDropZone.prototype.on = function(eventType, callback) {
      this.$elem.on(eventType, callback);
   }

   FileDropZone.prototype.off = function(eventType, callback) {
      this.$elem.off(eventType, callback);
   }


   return FileDropZone;
})();