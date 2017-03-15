'use strict';

app.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/workflows', {
        templateUrl: getPath('js/partials/workflows.html'),
        controller: 'workflowsCtrl'
    });
}]).controller('workflowsCtrl', [
    '$scope',
    '$http',
    '$httpParamSerializer',
    '$location',
    'workflow',
    'namespace',
    '$mdDialog',
    '$mdToast',
    function ($scope, $http, $httpParamSerializer, $location, workflow, namespace, $mdDialog, $mdToast) {
        if (namespace.get() === '') {
            $location.path('namespace');
            return ;
        }

        var updateList = function () {
            $http.get('/ws/workflows/list/' + namespace.get())
                 .then(function (response) {
                    $scope.list = response.data;
                 });
        };
        
        $scope.choose = function (target) {
            workflow.set(target);
            $location.path('workflow');
        };

        $scope.add = function (ev) {
            var confirm = $mdDialog.prompt()
                                   .title('Nom du workflow')
                                   .textContent('Choisissez un nom pour votre nouveau workflow')
                                   .placeholder('Nom')
                                   .ariaLabel('Nom')
                                   .targetEvent(ev)
                                   .ok('Créer')
                                   .cancel('Annuler');
            $mdDialog.show(confirm).then(function (result) {
                $http({
                    method: 'POST',
                    url: '/ws/workflows/create/' + namespace.get(),
                    data: $httpParamSerializer({name: result}),
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                    }
                }).then(function () {
                    $mdToast.show(
                        $mdToast.simple()
                                .textContent('Workflow créé')
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