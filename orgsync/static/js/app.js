/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */



(function () {
	"use strict";
	var app = angular.module('port', []);

    app.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    }]);

	app.controller('folioController', function() {
        this.information = "hello";
        this.tab = "index";
	});

	app.controller('viewController', function () {
		this.initial = 0;
		this.setPage = function (value) {
			this.initial = value;
		};
		this.getPage = function (value) {
			if (value === this.initial) {
				return 1;
			}
			return 0;
		};
	});

	app.directive('membershipform', function () {
		return {
			restrict: 'E',
			templateUrl: 'static/html/membership_form.html'
		};
	});
    
    app.directive('grantform', function () {
		return {
			restrict: 'E',
			templateUrl: 'static/html/grant_form.html'
		};
	});
    
        
    app.directive('dashboard', function () {
		return {
			restrict: 'E',
			templateUrl: 'static/html/grants_dashboard.html'
		};
	});
    
    app.directive('navigation', function () {
		return {
			restrict: 'E',
			templateUrl: 'static/html/navigation.html'
		};
	});
    
    app.directive('profile', function () {
		return {
			restrict: 'E',
			templateUrl: 'static/html/profile.html'
		};
	});
    
})();