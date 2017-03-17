'use strict';

app.controller('menuCtrl', ['$scope', '$location', '$http', '$websocket', function ($scope, $location, $http, $websocket) {
    $scope.logout = function () {
        $http.get('/ws/auth/logout')
             .then(function () {
                 $websocket.disconnect();
             });
    };

    $scope.variables = function () {
        $websocket.clear();
        $location.path('variables');
    };

    $scope.namespace = function () {
        $websocket.clear();
        $location.path('namespace')
    };

    $scope.workflow = function () {
        $websocket.clear();
        $location.path('workflows');
    };
}]);