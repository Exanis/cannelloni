'use strict';

app.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/variables', {
        templateUrl: getPath('js/partials/variables.html'),
        controller: 'variablesCtrl'
    });
}]).controller('variablesCtrl', [
    '$scope',
    '$http',
    '$httpParamSerializer',
    'namespace',
    'variable',
    '$mdDialog',
    '$mdToast',
    '$location',
    function ($scope, $http, $httpParamSerializer, namespace, variable, $mdDialog, $mdToast, $location) {
        if (namespace.get() === '') {
            $location.path('namespace');
            return ;
        }
        
        $scope.groupsData = {};
        
        var updateGroupsList = function () {
            $scope.groupsData = {};
            $http.get('/ws/groups/list/' + namespace.get())
                 .then(function (response) {
                     angular.forEach(response.data, function (value) {
                         $scope.groupsData[value.uuid] = {
                             group: value,
                             variables: []
                         };
                         $http.get('/ws/variables/list/' + value.uuid)
                              .then(function (variables) {
                                  $scope.groupsData[value.uuid].variables = variables.data;
                              });
                     });
                 });
        };

        $scope.addGroup = function (ev) {
            var confirm = $mdDialog.prompt()
                                   .title('Nom du groupe')
                                   .textContent('Choisissez un nom pour le nouveau groupe de variables')
                                   .placeholder('Nom')
                                   .ariaLabel('Nom')
                                   .targetEvent(ev)
                                   .ok('Créer')
                                   .cancel('Annuler');
            $mdDialog.show(confirm).then(function (result) {
                $http({
                    method: 'POST',
                    url: '/ws/groups/create/' + namespace.get(),
                    data: $httpParamSerializer({name: result}),
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                    }
                }).then(function () {
                    $mdToast.show(
                        $mdToast.simple()
                                .textContent('Groupe créé')
                                .position('bottom right')
                                .hideDelay(3000)
                    );
                    updateGroupsList();
                });
            });
        };

        $scope.deleteGroup = function (ev, uuid) {
            var confirm = $mdDialog.confirm()
                                   .title('Voulez-vous vraiment supprimer ce groupe ?')
                                   .textContent('Cette opération ne peut pas être annulée.')
                                   .ariaLabel('Supprimer un groupe')
                                   .targetEvent(ev)
                                   .ok('Supprimer')
                                   .cancel('Annuler');
            
            $mdDialog.show(confirm).then(function () {
                $http({
                    method: 'DELETE',
                    url: '/ws/groups/delete/' + uuid
                }).then(function () {
                    $mdToast.show(
                        $mdToast.simple()
                                .textContent('Groupe supprimé')
                                .position('bottom right')
                                .hideDelay(3000)
                    );
                    updateGroupsList();
                });
            });
        };

        var typesList = [];
        var currentGroup = '';

        $http.get('/ws/types/list')
             .then(function (response) {
                 typesList = response.data;
             });

        function addVariableCtrl($scope, $mdDialog) {
            $scope.types = typesList;

            $scope.cancel = function () {
                $mdDialog.cancel();
            };

            $scope.create = function () {
                $http({
                    method: 'POST',
                    url: '/ws/variables/create/' + currentGroup,
                    data: $httpParamSerializer({
                        name: $scope.name,
                        type: $scope.type_class
                    }),
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                    }
                }).then(function () {
                    $mdToast.show(
                        $mdToast.simple()
                                .textContent('Variable créée')
                                .position('bottom right')
                                .hideDelay(3000)
                    );
                    updateGroupsList();
                    $mdDialog.hide();
                });
            };
        };

        $scope.addVariable = function (ev, group) {
            currentGroup = group;

            $mdDialog.show({
                controller: ['$scope', '$mdDialog', addVariableCtrl],
                templateUrl: getPath('js/partials/dialogs/addVariable.html'),
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true
            });
        };

        function getTypeFromId(id) {
            length = typesList.length;
            for(var i = 0; i < length; i++) {
                if (typesList[i].id === id)
                    return typesList[i];
            }
            return {};
        }

        $scope.getTypeClass = function (typeClass) {
            return getTypeFromId(typeClass).name;
        };

        $scope.getTypeIcon = function (typeClass) {
            return getTypeFromId(typeClass).icon;
        };

        $scope.deleteVariable = function (ev, uuid) {
            var confirm = $mdDialog.confirm()
                                   .title('Voulez-vous vraiment supprimer cette variable ?')
                                   .textContent('Cette opération ne peut pas être annulée.')
                                   .ariaLabel('Supprimer une variable')
                                   .targetEvent(ev)
                                   .ok('Supprimer')
                                   .cancel('Annuler');
            
            $mdDialog.show(confirm).then(function () {
                $http({
                    method: 'DELETE',
                    url: '/ws/variables/delete/' + uuid
                }).then(function () {
                    $mdToast.show(
                        $mdToast.simple()
                                .textContent('Variable supprimée')
                                .position('bottom right')
                                .hideDelay(3000)
                    );
                    updateGroupsList();
                });
            });
        };

        $scope.editVariable = function (ev, v) {
            var slug = getTypeFromId(v.type_class).slug;
            variable.set(v);

            $mdDialog.show({
                controller: typesCtrl[slug],
                templateUrl: getPath('js/partials/dialogs/types/' + slug + '.html'),
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true
            }).then(updateGroupsList);
        };

        updateGroupsList();
    }
]);