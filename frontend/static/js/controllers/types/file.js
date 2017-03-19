'use strict';

typesCtrl['file'] = ['$scope', '$mdDialog', 'variable', '$http', '$httpParamSerializer', '$mdToast', 'Upload', function ($scope, $mdDialog, variable, $http, $httpParamSerializer, $mdToast, Upload) {
    $scope.filename = 'Cliquez ou glissez un fichier ici';
    $scope.file = {};
    $scope.showPercent = false;
    $scope.percent = 0;
    
    $scope.cancel = function () {
        $mdDialog.cancel();
    };

    $scope.onSelectFile = function () {
        $scope.filename = $scope.file.name;
    }

    $scope.send = function () {
        var params = {};

        params[variable.get().uuid] = $scope.file;
        $scope.showPercent = true;
        Upload.upload({
            url: '/ws/variables/update/' + variable.get().uuid,
            data: params
        }).then(function () {
            $mdToast.show(
                $mdToast.simple()
                        .textContent('Variable mise à jour')
                        .position('bottom right')
                        .hideDelay(3000)
            );
            $mdDialog.hide();
        }, function () {
            $mdToast.show(
                $mdToast.simple()
                        .textContent('Echec du téléchargement')
                        .position('bottom right')
                        .hideDelay(3000)
            );
            $mdDialog.hide();
        }, function (evt) {
            $scope.percent = parseInt(100.0 * evt.loaded / evt.total);
        });
    };
}];