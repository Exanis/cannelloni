'use strict';

app.controller('menuCtrl', ['$scope', '$location', '$http', function ($scope, $location, $http) {
    $scope.logout = function () {
        $http.get('/ws/auth/logout')
             .then(function () {
                 $location.path('login');
             });
    };

    $scope.variables = function () {
        $location.path('variables');
    };

    $scope.namespace = function () {
        $location.path('namespace')
    };

    $scope.workflow = function () {
        $location.path('workflows');
    };
}]);