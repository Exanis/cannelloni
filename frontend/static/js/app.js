'use strict';

var app = angular.module('cannelloni', [
    'ngRoute',
    'ngMaterial',
    'ngFileUpload',
    'ngSanitize'
]);

app.config([
    '$locationProvider',
    '$routeProvider',
    '$httpProvider',
    function ($locationProvider, $routeProvider, $httpProvider) {
        $locationProvider.hashPrefix('!');
        $routeProvider.otherwise({redirectTo: '/login'});

        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    }
]);