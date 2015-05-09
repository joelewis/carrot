'use strict';


// Declare app level module which depends on filters, and services
angular.module('carrot', [
  'ngRoute',
  'carrot.controllers',
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/', {templateUrl: '/static/partials/home.html', controller: 'HomeCtrl'});
  $routeProvider.when('/apps/:app_id', {templateUrl: '/static/partials/app.html', controller: 'AppCtrl'});
  $routeProvider.otherwise({redirectTo: '/'});
}]).config(['$locationProvider', function($locationProvider){
    $locationProvider.html5Mode(true).hashPrefix('!');
}]);
