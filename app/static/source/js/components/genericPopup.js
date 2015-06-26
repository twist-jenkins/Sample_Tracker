
/*************************************************************************************
*
* Copyright (c) 2015 Twist Bioscience
*
* File: app/static/source/js/components/genericPopup.js
* 
*************************************************************************************/


function GenericPopup($elem) {
    this.$elem = $elem;
    this.init();
}


GenericPopup.prototype.show = function(bodyText) {
    if (bodyText) {
        $(".body p",this.$elem).text(bodyText);
    }
    this.$elem.trigger('openModal');
}


GenericPopup.prototype.hide = function() {
    this.$elem.trigger('closeModal');
}

GenericPopup.prototype.on = function(eventType,callback) {
    this.$elem.on(eventType,callback);
}

GenericPopup.prototype.off = function(eventType,callback) {
    this.$elem.off(eventType,callback);
}

GenericPopup.prototype.init = function() {

    var fireEvent = function(eventType) {
        this.$elem.trigger(eventType);
    }.bind(this);

    var hideDialog = function() {
        this.hide();
    }.bind(this);

    this.$elem.easyModal({
        top: 200,
        autoOpen: false,
        overlayOpacity: 0.30,
        overlayColor: "#333",
        overlayClose: true,
        closeOnEscape: true,
        onClose: function(myModal){
            fireEvent("closed");
        }
    });

    $(".btn.ok",this.$elem).click(function() {
        hideDialog();
    });

}

