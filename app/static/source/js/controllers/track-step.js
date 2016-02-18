angular.module('twist.app').controller('trackStepController', ['$scope', '$state', 'Api', '$sce', '$timeout', 'Formatter', 'TypeAhead', 'Maps', 'Constants', 'TransformBuilder', 'FileParser',
    function ($scope, $state, Api, $sce, $timeout, Formatter, TypeAhead, Maps, Constants, TransformBuilder, FileParser) {

        $scope.stepTypeDropdownValue = Constants.STEP_TYPE_DROPDOWN_LABEL;

        $scope.Constants = Constants;

        $scope.transformSpec = TransformBuilder.newTransformSpec();
        $scope.transformSpec.setPlateStepDefaults();

        var setTransformSpecDetails = function (option) {
            $scope.transformSpec.setTransformSpecDetails(option);

            /* this could be a transform spec with requested by default so allow for that */
            if ($scope.transformSpec.requestedDataItems && $scope.transformSpec.requestedDataItems.length) {
                $scope.setShowPresentedRequestedData(true);
            }
        }

        $scope.setShowPresentedRequestedData = function (what) {
            $scope.showPresentedRequestedData = what;
        }

        $scope.selectStepType = function (option) {
            setTransformSpecDetails(option);
            $scope.transformSpec.setTitle(option.text);

            var route = 'root.record_transform.step_type_selected.tab_selected';

            var whichTab = Constants.STANDARD_TEMPLATE;

            if ($scope.transformSpec.map.type == Constants.USER_SPECIFIED_TRANSFER_TYPE) {
                whichTab = Constants.FILE_UPLOAD;
            } else if ($scope.transformSpec.map.type == Constants.HAMILTON_TRANSFER_TYPE) {
                whichTab = Constants.HAMILTON_OPERATION;
            }

            $state.go(route, {
                selected_step_type_id: option.id + '-' + Formatter.lowerCaseAndSpaceToDash(Formatter.stripNonAlphaNumeric(option.text, true, true).trim())
                ,selected_tab: whichTab
            });
        }

        $scope.setSelectedOption = function (optionId) {
            for (var i=0; i< $scope.stepTypeOptions.length;i++) {
                var option = $scope.stepTypeOptions[i];
                if (option.id == optionId) {
                    $scope.submissionResultMessage = '';
                    $scope.submissionResultVisible = 0;
                    $scope.setShowPresentedRequestedData(false);
                    $scope.transformSpec.reset();
                    setTransformSpecDetails(option);
                    $scope.transformSpec.setTitle(option.text);
                    $scope.stepTypeDropdownValue = $scope.transformSpec.details.text;
                    break;
                }
            }

            if ($scope.transformSpec.map.type == Constants.USER_SPECIFIED_TRANSFER_TYPE) {
                $scope.templateTypeSelection = Constants.FILE_UPLOAD;
            } else if ($scope.transformSpec.map.type == Constants.HAMILTON_TRANSFER_TYPE) {
                $scope.templateTypeSelection = Constants.HAMILTON_OPERATION;
            } else {
                $scope.templateTypeSelection = Constants.STANDARD_TEMPLATE;
            }
        }

        $scope.sampleTrackFormReady = function () {

            if (!$scope.transformSpec.details) {
                return false;
            }

            if (!$scope.transformSpec.operations || !$scope.transformSpec.operations.length) {
                return false
            }

            if ($scope.transformSpec.validateRequestedData) {
                var reqDataItems =  $scope.transformSpec.requestedDataItems;
                for (datum in reqDataItems) {
                    if (!reqDataItems[datum].validData) {
                        return false;
                    }
                }
            }

            return true;
        }

        var getSampleTrackSubmitData = function () {
            var data = {
                sampleTransformTypeId: $scope.transformSpec.details.id
                ,sampleTransformTemplateId: $scope.transformSpec.details.transform_template_id
            };

            data.transformMap = $scope.transformSpec.operations;

            return data;
        };

        $scope.submitStep = function () {

            var showError = function (data) {
                $scope.submissionResultMessage = 'Error: ' + data.errors;
                $scope.submissionResultVisible = -1;
                $scope.submittingStep = false;
            }

            var executeNow = true;

            //the newer specs are the ones that save the transform but do not execute it immediately
            if ($scope.transformSpec.details.transform_template_id == 25 ||
                $scope.transformSpec.details.transform_template_id == 26 ||
                $scope.transformSpec.details.transform_template_id == 27 ||
                $scope.transformSpec.details.transform_template_id == 28 ||
                $scope.transformSpec.details.transform_template_id == 29 ||
                $scope.transformSpec.details.transform_template_id == 30 ||
                $scope.transformSpec.details.transform_template_id == 31 ||
                $scope.transformSpec.details.transform_template_id == 35 ||
                $scope.transformSpec.details.transform_type_id == 84) {
                executeNow = false;
            }

            if (!$scope.submitting && $scope.sampleTrackFormReady() && !$scope.transformSpec.updating) {

                $scope.submittingStep = true;

                Api.saveAndConditionallyExecuteTransformSpec($scope.transformSpec.serialize(), executeNow).success(function (data) {

                    if (!data.errors || !data.errors.length) {
                        $scope.submittingStep = false;
                        $scope.submissionResultMessage = 'This <span class="twst-step-text">' + $scope.transformSpec.details.text + '</span> step was successfully recorded.';
                        $scope.submissionResultVisible = 1;
                        $scope.clearForm();
                    } else {
                        showError(data);
                    }

                    $timeout(function () {
                        $scope.submissionResultVisible = 0;
                        $timeout(function () {
                            $scope.submissionResultMessage = null;
                        }, 400);
                    }, 5000);

                }).error(function (data) {
                    $scope.submittingStep = false;
                    showError(data);
                });;
            }
        };

        $scope.clearForm = function (skipGo) {
            $scope.stepTypeDropdownValue = Constants.STEP_TYPE_DROPDOWN_LABEL;
            $scope.transformSpec = TransformBuilder.newTransformSpec();
            $scope.transformSpec.setPlateStepDefaults();
            $scope.templateTypeSelection = null;
            $scope.setShowPresentedRequestedData(false);
            if (!skipGo) {
                $state.go('root.record_transform');
            }
        };

        /* populate the sample types pulldown */
        $scope.initTransformTypes = Api.getSampleTransformTypes();
        $scope.initTransformTypes.success(function (data) {
            if (data.success) {

                var stepTypeOptions = data.results;
                var decoratedStepTypeOptions = [];
                /* lets add some spacers and data the UI can use to decorate the pulldown */
                var lastPrefix = '';
                var group = 0;
                for (var i=0, stoLength = stepTypeOptions.length; i< stoLength;i++) {
                    var thisItem = stepTypeOptions[i];
                    var thisPrefix = thisItem.text.substring(0, thisItem.text.indexOf(' '));

                    if (thisPrefix != lastPrefix) {
                        group++;
                    }
                    thisItem['uid_group'] = group;
                    decoratedStepTypeOptions.push(thisItem);
                    lastPrefix = thisPrefix;
                }
                $scope.stepTypeOptions = decoratedStepTypeOptions;
            }
        });
    }]
)
