'use strict';

app.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/workflow', {
        templateUrl: getPath('js/partials/workflow.html'),
        controller: 'workflowCtrl'
    });
}]).controller('workflowCtrl', [
    '$scope',
    '$http',
    '$httpParamSerializer',
    'namespace',
    'workflow',
    '$mdDialog',
    '$mdToast',
    '$location',
    '$interval',
    '$anchorScroll',
    '$websocket',
    'dump',
    function ($scope, $http, $httpParamSerializer, namespace, workflow, $mdDialog, $mdToast, $location, $interval, $anchorScroll, $websocket, dump) {
        if (namespace.get() === '') {
            $location.path('namespace');
            return ;
        }

        if (workflow.get() === '') {
            $location.path('workflows');
            return ;
        }
        
        $scope.layersData = {};
        $scope.workflow = workflow.get();
        
        $scope.testbutton = function () {
            $websocket.send(0, 'cool', {});
        };

        var typesList = {};
        var allFiltersList = [];

        $http.get('/ws/filters/types')
             .then(function (response) {
                 angular.forEach(response.data, function (type) {
                     typesList[type.slug] = type;
                 });
                 $scope.types = typesList;
             });
        
        $scope.getParameterForConfig = function (target, parameters) {
            for (var i in parameters) {
                if (parameters[i].key == target)
                    return parameters[i];
            }
            return null;
        };
        
        var updateLayersList = function () {
            $scope.layersData = {};
            allFiltersList = [];
            $http.get('/ws/layers/list/' + workflow.get().uuid)
                 .then(function (response) {
                     angular.forEach(response.data, function (value) {
                         $scope.layersData[value.uuid] = {
                             layer: value,
                             filters: []
                         };
                         $http.get('/ws/filters/list/' + value.uuid)
                              .then(function (filters) {
                                  $scope.layersData[value.uuid].filters = filters.data;
                                  allFiltersList = allFiltersList.concat(filters.data);
                              });
                     });
                 });
        };

        $scope.addLayer = function (ev) {
            var confirm = $mdDialog.prompt()
                                   .title('Nom du calque')
                                   .textContent('Choisissez un nom pour le nouveau calque')
                                   .placeholder('Nom')
                                   .ariaLabel('Nom')
                                   .targetEvent(ev)
                                   .ok('Créer')
                                   .cancel('Annuler');
            $mdDialog.show(confirm).then(function (result) {
                $http({
                    method: 'POST',
                    url: '/ws/layers/create/' + workflow.get().uuid,
                    data: $httpParamSerializer({name: result}),
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                    }
                }).then(function () {
                    $mdToast.show(
                        $mdToast.simple()
                                .textContent('Calque créé')
                                .position('bottom right')
                                .hideDelay(3000)
                    );
                    updateLayersList();
                });
            });
        };

        $scope.deleteLayer = function (ev, uuid) {
            var confirm = $mdDialog.confirm()
                                   .title('Voulez-vous vraiment supprimer ce calque ?')
                                   .textContent('Cette opération ne peut pas être annulée.')
                                   .ariaLabel('Supprimer un calque')
                                   .targetEvent(ev)
                                   .ok('Supprimer')
                                   .cancel('Annuler');
            
            $mdDialog.show(confirm).then(function () {
                $http({
                    method: 'DELETE',
                    url: '/ws/layers/delete/' + uuid
                }).then(function () {
                    $mdToast.show(
                        $mdToast.simple()
                                .textContent('Calque supprimé')
                                .position('bottom right')
                                .hideDelay(3000)
                    );
                    updateLayersList();
                });
            });
        };

        $scope.moveLayer = function (uuid, direction) {
            $http({
                method: 'POST',
                url: '/ws/layers/move/' + uuid,
                data: $httpParamSerializer({direction: direction}),
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                }
            }).then(function (result) {
                if (result.data.success) {
                    $mdToast.show(
                        $mdToast.simple()
                                .textContent('Calque déplacé')
                                .position('bottom right')
                                .hideDelay(3000)
                    );
                    updateLayersList();
                }
            });
        };

        var currentLayer;

        function addFilterCtrl($scope, $mdDialog) {
            $scope.types = typesList;

            $scope.cancel = function () {
                $mdDialog.cancel();
            };

            $scope.create = function () {
                $http({
                    method: 'POST',
                    url: '/ws/filters/create/' + currentLayer,
                    data: $httpParamSerializer({
                        name: $scope.name,
                        target: $scope.target.slug
                    }),
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                    }
                }).then(function () {
                    $mdToast.show(
                        $mdToast.simple()
                                .textContent('Filtre ajouté')
                                .position('bottom right')
                                .hideDelay(3000)
                    );
                    updateLayersList();
                    $mdDialog.hide();
                });
            };
        };

        $scope.addFilter = function (ev, layer) {
            currentLayer = layer;

            $mdDialog.show({
                controller: ['$scope', '$mdDialog', addFilterCtrl],
                templateUrl: getPath('js/partials/dialogs/addFilter.html'),
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true
            });
        };

        var targetConfig = {};
        var targetFilter = '';

        function addConfigCtrl($scope, $mdDialog, namespace) {
            $http.get('/ws/variables/all/' + namespace.get())
                 .then(function (response) {
                     $scope.list = [];
                     angular.forEach(response.data, function (variable) {
                         if (variable['type_slug'] == targetConfig['type'])
                            $scope.list.push(variable)
                     });
                 });

            $scope.cancel = function () {
                $mdDialog.cancel();
            };

            $scope.choose = function () {
                $http({
                    method: 'POST',
                    url: '/ws/filters/configure',
                    data: $httpParamSerializer({
                        filter: targetFilter.uuid,
                        variable: $scope.target,
                        key: targetConfig['key']
                    }),
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                    }
                }).then(function () {
                    $mdToast.show(
                        $mdToast.simple()
                                .textContent('Filtre configuré')
                                .position('bottom right')
                                .hideDelay(3000)
                    );
                    updateLayersList();
                    $mdDialog.hide();
                });
            };
        };

        $scope.selectVariable = function (ev, filter, config) {
            targetConfig = config;
            targetFilter = filter;

            $mdDialog.show({
                controller: ['$scope', '$mdDialog', 'namespace', addConfigCtrl],
                templateUrl: getPath('js/partials/dialogs/addConfig.html'),
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true
            });
        }

        $scope.deleteFilter = function (ev, uuid) {
            var confirm = $mdDialog.confirm()
                                   .title('Voulez-vous vraiment supprimer ce filtre ?')
                                   .textContent('Cette opération ne peut pas être annulée.')
                                   .ariaLabel('Supprimer un filtre')
                                   .targetEvent(ev)
                                   .ok('Supprimer')
                                   .cancel('Annuler');

            $mdDialog.show(confirm).then(function () {
                $http({
                    method: 'DELETE',
                    url: '/ws/filters/delete/' + uuid
                }).then(function () {
                    $mdToast.show(
                        $mdToast.simple()
                                .textContent('Filtre supprimé')
                                .position('bottom right')
                                .hideDelay(3000)
                    );
                    updateLayersList();
                });
            });
        };

        $scope.moveFilter = function (uuid, direction) {
            $http({
                method: 'POST',
                url: '/ws/filters/move/' + uuid,
                data: $httpParamSerializer({direction: direction}),
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                }
            }).then(function (result) {
                if (result.data.success) {
                    $mdToast.show(
                        $mdToast.simple()
                                .textContent('Filtre déplacé')
                                .position('bottom right')
                                .hideDelay(3000)
                    );
                    updateLayersList();
                }
            });
        };

        function addLinkCtrl($scope, $mdDialog, namespace) {
            $scope.types = typesList;
            $scope.currentFilter = targetFilter;

            $scope.possibleFilters = allFiltersList;

            $scope.cancel = function () {
                $mdDialog.cancel();
            };

            $scope.link = function () {
                $http({
                    method: 'POST',
                    url: '/ws/filters/link',
                    data: $httpParamSerializer({
                        origin_filter: targetFilter.uuid,
                        target_filter: $scope.targetFilter.uuid,
                        origin_node: $scope.origin,
                        target_node: $scope.targetNode
                    }),
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                    }
                }).then(function () {
                    $mdToast.show(
                        $mdToast.simple()
                                .textContent('Lien créé')
                                .position('bottom right')
                                .hideDelay(3000)
                    );
                    updateLayersList();
                    $mdDialog.hide();
                });
            };
        };

        $scope.addLink = function (ev, filter) {
            targetFilter = filter;

            $mdDialog.show({
                controller: ['$scope', '$mdDialog', 'namespace', addLinkCtrl],
                templateUrl: getPath('js/partials/dialogs/addLink.html'),
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true
            });
        }

        $scope.deleteLink = function (ev, uuid) {
            var confirm = $mdDialog.confirm()
                                   .title('Voulez-vous vraiment supprimer ce lien ?')
                                   .textContent('Cette opération ne peut pas être annulée.')
                                   .ariaLabel('Supprimer un lien')
                                   .targetEvent(ev)
                                   .ok('Supprimer')
                                   .cancel('Annuler');

            $mdDialog.show(confirm).then(function () {
                $http({
                    method: 'DELETE',
                    url: '/ws/filters/unlink/' + uuid
                }).then(function () {
                    $mdToast.show(
                        $mdToast.simple()
                                .textContent('Lien supprimé')
                                .position('bottom right')
                                .hideDelay(3000)
                    );
                    updateLayersList();
                });
            });
        };

        $scope.playing = false;
        $scope.stepping = false;
        $scope.started = false;
        $scope.status = '';
        $scope.currentlyRunning = '';

        var watchId;

        function _runWorkFlow (cmd) {
            $scope.playing = true;
            $scope.status = 'En attente';

            $websocket.hook('started', function (data) {
                $scope.status = 'Démarré';
                watchId = data['id'];
            })

            $websocket.hook('status', function (data) {
                if (data.status !== 'Unchanged') {
                    $scope.status = data.status;

                    if ($scope.status === "Running") {
                        $scope.started = true;
                        $scope.currentlyRunning = data.filter;
                    }
                }
                if (data.status === 'Done' || data.status === 'Error') {
                    $scope.started = true;
                    $scope.playing = false;
                    $scope.stepping = false;
                    $scope.currentlyRunning = '';
                }
                $scope.$apply();
            });

            function dumpHandler($scope, $mdDialog, dump) {
                $scope.data = dump.get();
                $scope.showingFilter = null;
                $scope.displayedNode = false;

                $scope.cancel = function () {
                    $mdDialog.cancel;
                }

                $scope.showFilterNodes = function (filter) {
                    $scope.showingFilter = filter;
                }

                $scope.showNode = function (node) {
                    $scope.displayedNode = node;
                }
            }

            $websocket.hook('dump', function (data) {
                dump.set(data.dump);
                
                $mdDialog.show({
                    controller: ['$scope', '$mdDialog', 'dump', dumpHandler],
                    templateUrl: getPath('js/partials/dialogs/dumpWorkflow.html'),
                    parent: angular.element(document.body),
                    clickOutsideToClose: true
                });
            });

            $websocket.send(workflow.get().uuid, cmd)
        };

        $scope.playWorkflow = function () {
            _runWorkFlow("play");
        };

        $scope.startWorkflow = function () {
            $scope.stepping = true;
            _runWorkFlow("start");
        };

        $scope.stepWorkflow = function () {
            $websocket.send(watchId, "step");
        };

        $scope.runWorkflow = function () {
            $websocket.send(watchId, "run");
        };

        $scope.quitWorkflow = function () {
            $websocket.send(watchId, "quit");
        };

        $scope.dumpWorkflow = function () {
            $websocket.send(watchId, "dump");
        };

        $scope.log = function (ev) {
            $http.get('/ws/workflows/log/' + workflow.get().uuid)
                 .then(function (response) {
                     $mdDialog.show(
                        $mdDialog.alert()
                            .clickOutsideToClose(true)
                            .title('Journal d\'exécution')
                            .htmlContent('<pre>' + response.data['log'] + '</pre>')
                            .ariaLabel('Journal d\'exécution')
                            .ok('Fermer')
                            .targetEvent(ev)
                        );
                 });
        };

        $scope.goto = function (where) {
            $anchorScroll(where);
        }
        $anchorScroll.yOffset = 100;

        updateLayersList();
    }
]);