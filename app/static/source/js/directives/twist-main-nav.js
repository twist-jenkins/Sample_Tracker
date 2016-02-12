angular.module('twist.app').directive('twistMainNav', [ 
    function() {
        return {
            restrict: 'E'
            ,templateUrl: 'twist-main-nav.html'
            ,controller: ['$scope', 
                function ($scope) {
                    $scope.navItems = [
                        {text: 'Record Transform', link: 'root.record_transform'}
                        ,{text: 'Plate Details', link: 'root.plate_details'}
                        ,{text: 'Edit Plate Barcode', link: 'root.edit_barcode'}
                        ,{text: 'Transform Specs', link: 'root.transform_specs.view_manage', match: 'root.transform_specs'}
                        ,{text: 'View Steps', link: 'root.view_steps'} 
                        ,{text: 'Sample Details', link: 'root.sample_details'}
                        ,{text: 'Trash Samples', link: 'root.trash_samples'}
                    ];
                }
            ]
        };
    }
]);
