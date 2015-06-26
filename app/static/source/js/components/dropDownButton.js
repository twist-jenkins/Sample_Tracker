/*************************************************************************************
 *
 * Copyright (c) 2015 Twist Bioscience
 *
 * File: app/static/source/js/components/dropDownButton.js
 * 
 *************************************************************************************/
 
var DropDownButton = (function() {

   function DropDownButton($elem, $hiddenSelectElem) {
      this.$elem = $elem;
      this.$hiddenSelectElem = $hiddenSelectElem
      this.$buttonLabel = $("button span.label", this.$elem);
      this.unselectedStateButtonLabel = this.$buttonLabel.text();

      this.init();
   }

   DropDownButton.prototype.init = function() {
      var handleClick = function($a) {
         selectedItemId = $a.parent().data("sample-tranfer-type-id");
         if (selectedItemId) {
            this.$hiddenSelectElem.val(selectedItemId);
            this.$buttonLabel.text($a.text());
         }
         this.$elem.trigger("itemSelected", selectedItemId);
      }.bind(this);

      $("li a", this.$elem).click(function() {
         handleClick($(this));
      });
   }

   DropDownButton.prototype.reset = function() {
      this.$buttonLabel.text(this.unselectedStateButtonLabel);
      this.$hiddenSelectElem.val("");
   }

   DropDownButton.prototype.val = function() {
      return this.$hiddenSelectElem.val();
   }


   DropDownButton.prototype.selectItemById = function(itemId) {
      var itemAnchor = $('li[data-sample-tranfer-type-id=' + itemId + '] a ', this.$elem);
      itemAnchor.trigger("click");
   }


   DropDownButton.prototype.on = function(eventType, callback) {
      this.$elem.on(eventType, callback);
   }

   DropDownButton.prototype.off = function(eventType, callback) {
      this.$elem.off(eventType, callback);
   }

   return DropDownButton;

})();