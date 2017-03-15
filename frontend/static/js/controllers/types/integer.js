'use strict';

typesCtrl['integer'] = ['$scope', '$mdDialog', 'variable', '$http', '$httpParamSerializer', '$mdToast', function ($scope, $mdDialog, variable, $http, $httpParamSerializer, $mdToast) {
    $scope.value = variable.get().value;
    
    $scope.cancel = function () {
        $mdDialog.cancel();
    };

    $scope.send = function () {
        var params = {};
        params[variable.get().uuid] = $scope.value;
        $http({
            method: 'POST',
            url: '/ws/variables/update/' + variable.get().uuid,
            data: $httpParamSerializer(params),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
        }).then(function () {
            $mdToast.show(
                $mdToast.simple()
                        .textContent('Variable mise à jour')
                        .position('bottom right')
                        .hideDelay(3000)
            );
            $mdDialog.hide();
        });
    };
}];