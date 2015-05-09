'use strict';

/* Controllers */
angular.module('carrot.controllers', [])
  .controller('HomeCtrl', ['$scope', '$http', function($scope, $http) {

    $scope.user = window.user;
  	$scope.apps = [];
  	$scope.appname = '';

  	$scope.get_apps = function() {
  		$http.get('/api/v1/apps').success(function(data, status, headers, config) {
  			console.log(data);
        $scope.apps = data;
  		});
  	}

  	$scope.get_apps();


  	$scope.createApp = function( appname ) {
  		if ( appname == '' )
  			return false;

      $.ajax({
        method: 'post',
        url: '/api/v1/apps',
        data: {'appname': appname},
        dataType: 'json',
        success: function() {
          console.log('success');
        }
      })
  		// $http.put('/api/v1/apps', {'appname':appname}).success(function(data, status, headers, config) {
      //   $scope.apps.push(data);
  		// 	$scope.appname = '';
  		// });
  	}

  }])
   .controller('AppCtrl', ['$scope', '$routeParams', '$http', function($scope, $routeParams, $http) {


  	 $scope.newLogTitle = '';
  	 $scope.newLogDescription = '';
  	 $scope.app_id = $routeParams.app_id;
  	 $scope.logs = [];

  	 $scope.addNewLog = function(title, description) {
    	 	if ( title == '' )
    	 		return false

    	 	if ( description == '' )
    	 		return false

    	 	var data = {
    	 		'title': title,
    	 		'description': description
    	 	}
    	 	$http.post('/api/v1/apps/'+$scope.app_id, data).success(function(data, status, headers, config) {
    	 		console.log(data);
    	 		$scope.logs.unshift(data);
    	 		$scope.newLogTitle = '';
    	 		$scope.newLogDescription =''
    	 	});
  	 }

  	 console.log('/api/v1/apps/'+$scope.app_id);
  	 $scope.get_logs = function() {
  	 	$http.get('/api/v1/apps/'+$scope.app_id).success(function(data, status, headers, config) {
  	 		console.log(data);
  	 		$scope.logs = data.logs;
  	 		$scope.app = data;

  	 	});
  	 }

  	$scope.get_logs();

  }]);
