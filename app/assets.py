######################################################################################
#
# Copyright (c) 2015 Twist Bioscience
#
# File: assets.py
#
# This is the configuration for all assets that get bundled up for the web pages to access. 
# 
######################################################################################

from flask_assets import Bundle


common_css = Bundle(
    'css/bootstrap.min.css',
    'css/font-awesome.min.css',
    'source/css/main.css',
    output='css/common.css')

index_css = Bundle(
    'source/css/dropzone.css',
    'source/css/views/index.css',
    filters="cssmin",
    output='css/views/index.css')

editPlate_css = Bundle(
    'source/css/views/editPlate.css',
    filters="cssmin",
    output='css/views/editPlate.css')

sampleReport_css = Bundle(
    'source/css/views/sampleReport.css',
    filters="cssmin",
    output='css/views/sampleReport.css')

plateReport_css = Bundle(
    'source/css/views/plateReport.css',
    filters="cssmin",
    output='css/views/plateReport.css')

index_ie8_css = Bundle(
    'source/css/views/index_ie8.css',
    filters="cssmin",
    output='css/views/index_ie8.css')


index_ie9_css = Bundle(
    'source/css/views/index_ie9.css',
    filters="cssmin",
    output='css/views/index_ie9.css')



common_js = Bundle(
       'js/rlite.min.js', 
       'js/jquery.min.js', 
       'js/jquery.easing.min.js', 
       'js/bootstrap.min.js',
       'js/underscore-min.js',
       'js/handlebars.min.js',
       'js/moment.min.js',
       'js/jquery.easyModal.js',
       'js/bootstrap-typeahead.min.js',
       'source/js/jquery.leanModal.min.js',
       'source/js/components/genericPopup.js', 
       'source/js/utils/utils.js', 
       output='js/common.js')

index_js = Bundle(
       'source/js/components/dropDownButton.js', 
       'source/js/dropzone.js', 
       'source/js/fileDropZone.js', 
       'source/js/views/index.js', 
        output='js/views/index.js')

editPlate_js = Bundle(
       'source/js/components/dropDownButton.js', 
       'source/js/views/editPlate.js', 
        output='js/views/editPlate.js')

sampleReport_js = Bundle(
       'source/js/views/sampleReport.js', 
        output='js/views/sampleReport.js')


plateReport_js = Bundle(
       'source/js/views/plateReport.js', 
        output='js/views/plateReport.js')


