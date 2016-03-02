angular.module('twist.app').controller('hamiltonWizardFinishRunController', ['$scope', '$state', '$stateParams', 'Api', '$timeout',
    function ($scope, $state, $stateParams, Api, $timeout) {

        $scope.savedSpecIdToFinish = $stateParams.saved_spec_id;
        $scope.setCurrentStepInstruction('Click "Run Finished" once the Hamilton run is complete.');

        $scope.getPrettySpecDate = function (dateString) {
            var date = new Date(dateString);
            return date.toLocaleString();
        }
        $scope.runFinished = function () {
            if (!$scope.finishiningRun) {
                $scope.finishiningRun = true;
                Api.executeTransformSpec($scope.savedSpecIdToFinish).success(function (data) {
                    $scope.finishiningRun = false;
                    $state.go('root.record_transform.step_type_selected.tab_selected.hamilton_wizard.run_complete', {
                        saved_spec_id: $scope.savedSpecIdToFinish
                    });
                }).error(function (error) {
                    $scope.finishiningRun = false;
                    $scope.clearScannedItemErrorMessage();
                    $scope.showScannedItemErrorMessage('This Hamilton run could not be finished. Please try again.');
                });
            }
        };

        $scope.setWorklistFetched = function () {
            $timeout(function () {
                $scope.worklistFetched = true;
            }, 1200);
        };

        Api.getTransformSpec($scope.savedSpecIdToFinish).success(function (data) {
            $scope.clearScannedItemErrorMessage();
            var savedSpecToFinish = data.data;

            if (savedSpecToFinish.data_json.details.transform_template_id == 42 || savedSpecToFinish.data_json.details.transform_template_id == 46) {
                $scope.displayWorklist = false;
                $scope.worklistFetched = true;
            } else {
                $scope.displayWorklist = true;
                /* create the data for the Hamilton Worklist dragout functionality */
                var now = (new Date()).toLocaleDateString().replace(/^(\d+)\D(\d+)\D(\d+)$/, '$3-$1-$2').replace(/\b(\d)\b/g, '0$1');
                var filename = 'worklist-' + now + '-' + savedSpecToFinish.data_json.sources[0].details.id + '.csv';
                var afterProtocol = document.location.href.substring(document.location.href.indexOf('://') + 3);
                var server = afterProtocol.substring(0, afterProtocol.indexOf('/'));

                var worklistUrl = document.location.href.substring(0, document.location.href.indexOf(':')) + '://' + server + '/api/v1/rest/worklist/' + $scope.savedSpecIdToFinish;

                $scope.dragOutData = 'text/plain|' + filename + '|' + worklistUrl; //'text/plain|worklist.png|http://localhost/static/images/twist.png';
				$scope.worklistFilename = filename;
            }

            $scope.savedSpecToFinish = savedSpecToFinish;

        }).error(function (data) {
            $scope.savedSpecToFinish = null;
        });
        $scope.showFinishRun();
    }]
);
