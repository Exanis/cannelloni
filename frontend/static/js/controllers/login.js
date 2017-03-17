'use strict';

app.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/login', {
        templateUrl: getPath('js/partials/login.html'),
        controller: 'loginCtrl'
    });
}]).controller('loginCtrl', [
    '$scope',
    '$http',
    '$httpParamSerializer',
    '$location',
    '$mdToast',
    '$websocket',
    function ($scope, $http, $httpParamSerializer, $location, $mdToast, $websocket) {
        $scope.login = function () {
            $http({
                method: 'POST',
                url: '/ws/auth/login',
                data: $httpParamSerializer({
                    username: $scope.username,
                    password: $scope.password
                }),
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                }
            }).then(function (response) {
                if (response.data.success) {
                    $websocket.connect(function () {
                        $location.path('namespace');
                        $scope.$apply();
                    });
                } else {
                    $mdToast.show(
                        $mdToast.simple()
                                .textContent('Utilisateur ou mot de passe incorrect')
                                .position('bottom right')
                                .hideDelay(3000)
                    );
                }
            });
        };
    }
]);