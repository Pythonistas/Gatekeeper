(function () {
    var app = angular.module('dogApi', ['ngResource']);

    app.config(['$interpolateProvider', function($interpolateProvider){
        $interpolateProvider.startSymbol('{-');
        $interpolateProvider.endSymbol('-}');
    }]);

    // --Dog Types--
    app.factory('DogTypes', function ($resource) {
        return $resource('http://localhost:5555/api/v1/types/dogs/', {}, { 'query': { method: 'GET', isArray: true }}, { stripTrailingSlashes: false });
    });

    app.controller('DogTypesController', ['$scope', 'DogTypes', function ($scope, DogTypes) {
        $scope.dog_types = DogTypes.query();
        console.log($scope.dog_types);  // [DEBUG-ONLY]
    }]);

    // --Dogs--
    app.factory('Dogs', function ($resource) {
        return $resource('http://localhost:5555/api/v1/dogs/:id', {}, {}, { stripTrailingSlashes: false });
    });

    app.controller('DogsController', ['$scope', 'Dogs', function ($scope, Dogs) {
        $scope.dogs = Dogs.query();
        //console.log($scope.dogs);  // [DEBUG-ONLY]
    }]);

    // --Dog--
    app.controller('DogController', ['$scope', function ($scope) {
        //$scope.name = null;
        //$scope.gender = null;
        //$scope.group = null;
    }]);

    // --Form--
    app.controller('NewDogFormController', ['$scope', function ($scope) {
        $scope.submit = function () {
            console.log('Submit button pressed!');
        };
    }]);


    app.controller('FacilityController', ['$http', function($http){
        var facility = this;

        facility.dogs = [];

        //$http.get('http://localhost:5555/api/v1/dogs/').success(function(data){
        //    facility.dogs = data.dogs;
        //    console.log(facility.dogs);  // [DEBUG-ONLY]
        //});

        $http({
            method: 'GET',
            url: 'http://localhost:5555/api/v1/dogs/'
        }).then(
            function(response) {
                facility.dogs = response.data.dogs;
                console.log(facility.dogs);  // [DEBUG-ONLY]
            },
            function(reason) { }
        );
    }]);

    app.controller('FormController', ['$http', function($http){
        var facility = this;

        $http({
            method: 'POST',
            url: 'http://localhost:5555/api/v1/dogs/',
            data: {}
        }).then(
            // try / successCallback
            function(response) {
                toastr.success("A new dog was successfully created.", "Success");
            },
            // catch / errorCallback
            function(reason) {
                toastr.error("There was a problem trying to create a new dog.", "Error", { timeOut: 0, extendedTimeOut: 0 });
            },
            // throw / notificationCallback
            function(update) { }
        );
    }]);

    //toastr.options = {
    //    "closeButton": true,
    //    "debug": false,
    //    "newestOnTop": false,
    //    "progressBar": true,
    //    "positionClass": "toast-top-right",
    //    "preventDuplicates": true,
    //    "onclick": null,
    //    "showDuration": "300",
    //    "hideDuration": "1000",
    //    "timeOut": "5000",
    //    "extendedTimeOut": "1000",
    //    "showEasing": "swing",
    //    "hideEasing": "linear",
    //    "showMethod": "fadeIn",
    //    "hideMethod": "fadeOut"
    //}

})();
