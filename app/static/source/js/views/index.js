
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


         _.each(responseJson.task_items,function(task_item) {
            

            // $("table#spreadsheet tbody 

            var context = {
                sourcePlateId:task_item.source_plate_id,
                sourceWell:task_item.source_well,
                destinationPlateId:task_item.destination_plate_id,
                destinationWell:task_item.destination_well
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
            var sourcePlateId = null, destinationPlateId = null;
            var postData = null;

            if (sampleTransferTypeId === "") {
               m_errorPopup.show("Please specify a transfer type.");
               return;
            }

            postData = {
               sampleTransferTypeId:sampleTransferTypeId
            }

            if (useSpreadsheetData) {
               postData.wells = [];
               $("table#spreadsheet tbody tr").each(function() {
                  var $tr = $(this);
                  var oneWell = {
                     sourcePlateId:$.trim($("td:eq(0)",$tr).text()),
                     sourceWell:$.trim($("td:eq(1)",$tr).text()),
                     destinationPlateId:$.trim($("td:eq(2)",$tr).text()),
                     destinationWell:$.trim($("td:eq(3)",$tr).text())
                  }
                  postData.wells.push(oneWell);
               });
            } else {
               sourcePlateId = $.trim($("#sourcePlateId").val());
               destinationPlateId = $.trim($("#destinationPlateId").val());

               if (sourcePlateId === "" || destinationPlateId === "") {
                 m_errorPopup.show("Please specify a source plate id and a destination plate id.");
                 return;                  
               }

               postData.sourcePlateId = sourcePlateId;
               postData.destinationPlateId = destinationPlateId;

            }

           // alert("post data: " + postData);
            alert(JSON.stringify(postData));

            alert("URL: " + m_createSampleMovementUrl);

            var data = JSON.stringify(postData);

            Twist.Utils.ajaxJsonPost(m_createSampleMovementUrl,data,function(data) {
               alert("RESPONDED: " + data);
               alert(JSON.stringify(data));

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



    function init() {
       // alert("init");
        
        initDropzone();
        initForm();

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