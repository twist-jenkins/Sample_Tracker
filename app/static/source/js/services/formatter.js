var api_base_url = '/api/v1/';
var server_url = twist_api_url;

angular.module('twist.app').factory('Formatter', [
    function () {

        var alphaNumeric = 'abcdefghijklmnopqrstuvwxyz0123456789';

        var stripNonAlphaNumeric = function (inString, dashOk, replaceWithSpace) {

            var okChars = alphaNumeric;
            if (dashOk) {
                okChars += '-';
            }

            var outString = inString;
            if (inString != null) {
                outString = '';
                inString = inString.toLowerCase();
                for (var i=0; i<inString.length;i++) {
                    var thisChar = inString.charAt(i);
                    if (okChars.indexOf(thisChar) != -1) {
                        outString += thisChar;
                    } else if (replaceWithSpace) {
                        outString += ' ';
                    }
                }
            }

            return outString;
        };

        return {
            lowerCaseAndSpaceToDash: function (str) {
                return str.toLowerCase().replace(/\s+/g, '-');
            }
            ,spaceToDash: function (str) {
                return str.replace(/\s+/g, '-');
            }
            ,dashToSpace: function (str) {
                return str.replace('-', ' ');
            }
            ,stripNonAlphaNumeric: function (str, dashOk, replaceWithSpace) {
                return stripNonAlphaNumeric(str, dashOk, replaceWithSpace);
            },
            getPrettyDateString: function (dateString, shortYear) {
                var d = new Date(dateString);
                var date = d.toLocaleString();
                if (shortYear) {
                    date = date.substring(0, date.lastIndexOf('/') + 1) + date.substring(date.lastIndexOf('/') + 3);
                }
                return date;
            }
            ,addLeadingZero: function (number, finalLength) {

                if (finalLength == null) {
                    finalLength = 2;
                }

                numberString = number + '';
                while (numberString.length < finalLength) {
                    numberString = '0' + number;
                }
                return numberString;
            }
        }
    }]
);
