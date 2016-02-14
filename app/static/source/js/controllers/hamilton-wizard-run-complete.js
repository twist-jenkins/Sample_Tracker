angular.module('twist.app').controller('hamiltonWizardRunCompleteController', ['$scope', '$state', '$stateParams', 'Api', '$timeout',
    function ($scope, $state, $stateParams, Api, $timeout) {
        /* TO DO:  retrieve saved spec so's we know what to mark as executed */
        $scope.savedSpecId = $stateParams.saved_spec_id;
        $scope.setCurrentStepInstruction('Trash any bad wells or plates now.');
        $scope.showFinishRun();

        $scope.hamiltonDone = function () {
            $scope.clearForm();
        };

        $scope.trashSamples = function (transformSpecId) {
            $state.go('root.trash_samples.by_transform_spec', {
                spec_id: transformSpecId
            });
        }

    }]
);
