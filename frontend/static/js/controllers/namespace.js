'use strict';

app.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/namespace', {
        templateUrl: getPath('js/partials/namespace.html'),
        controller: 'namespaceCtrl'
    });
}]).controller('namespaceCtrl', [
    '$scope',
    '$http',
    '$httpParamSerializer',
    '$location',
    'namespace',
    '$mdDialog',
    '$mdToast',
    function ($scope, $http, $httpParamSerializer, $location, namespace, $mdDialog, $mdToast) {
        var updateList = function () {
            $http.get('/ws/namespaces/list')
                 .then(function (response) {
                    $scope.list = response.data;
                 });
        };
        
        $scope.choose = function (target) {
            namespace.set(target);
            $location.path('workflows');
        };

        $scope.add = function (ev) {
            var confirm = $mdDialog.prompt()
                                   .title('Nom du namespace')
                                   .textContent('Choisissez un nom pour votre nouveau namespace')
                                   .placeholder('Nom')
                                   .ariaLabel('Nom')
                                   .targetEvent(ev)
                                   .ok('Créer')
                                   .cancel('Annuler');
            $mdDialog.show(confirm).then(function (result) {
                $http({
                    method: 'POST',
                    url: '/ws/namespaces/create',
                    data: $httpParamSerializer({name: result}),
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                    }
                }).then(function () {
                    $mdToast.show(
                        $mdToast.simple()
                                .textContent('Namespace créé')
                                .position('bottom right')
                                .hideDelay(3000)
                    );
                    updateList();
                });
            });
        };

        updateList();
    }
]);