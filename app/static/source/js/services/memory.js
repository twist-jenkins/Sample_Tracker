var api_base_url = '/api/v1/';
var server_url = twist_api_url;

angular.module('twist.app').factory('Memory', [
    function () {
        var memory = {};
        var closure = function (enclosee) {
            return enclosee;
        };
        return {
            remember: function (name, what) {
                if (what != null) {
                    memory[name] = what;
                }

                return memory[name];
            }
            ,forget: function (name) {
                var forgotten = closure(memory[name]);
                delete memory[name];
                return forgotten;
            }
        };
    }
]);
