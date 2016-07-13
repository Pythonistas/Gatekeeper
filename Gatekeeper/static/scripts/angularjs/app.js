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
        //console.log($scope.dog_types);  // [DEBUG-ONLY]
    }]);


    // --'Experimental' Dogs--
    app.service('exService', function ($http, $q) {

        // Return public API.
        return({
            getDogs: getDogs,
            addDog: addDog,
            //removeDog: removeDog,
        });

        function getDogs() {
            var request = $http({
                method: "get",
                url: 'http://localhost:5555/api/v1/dogs/',
            });

            return (request.then(handleSuccess, handleError));
        }

        function addDog( name ) {
            var request = $http({
                method: "post",
                url: 'http://localhost:5555/api/v1/dogs/',
                data: {
                    "dog": {
                        "name": name
                    }
                }
            });

            return (request.then(handleSuccess, handleError));
        }

        //function removeDog( id ) {
        //    var request = $http({
        //        method: "delete",
        //        url: 'http://localhost:5555/api/v1/dogs/' + id,
        //    })
        //}

        function handleError(response) {
            // The API response from the server should be returned in a
            // nomralized format. However, if the request was not handled by the
            // server (or what not handles properly - ex. server error), then we
            // may have to normalize it on our end, as best we can.
            if (
                !angular.isObject(response.data) ||
                !response.data.message
                ) {
                return ($q.reject("An unknown error occurred."));
            }
            // Otherwise, use expected error message.
            return ($q.reject(response.data.message));
        }

        // I transform the successful response, unwrapping the application data
        // from the API response payload.
        function handleSuccess(response) {
            return (response.data);
        }
    });

    app.controller('exController', function ($scope, exService) {
        $scope.dogs = [];

        $scope.form = {
            name: "",
        };

        loadRemoteData();

        // --Public--
        $scope.addDog = function () {
            exService.addDog($scope.form.name)
            .then(
                loadRemoteData, function (errorMessage) {
                    console.warn(errorMessage);
                }
            );

            // Reset the form once values have been consumed.
            $scope.form.name = "";
        };

        //$scope.removeDog = function (dog) {
        //    exService.removeDog($scope.dog.id)
        //    .then(loadRemoteData);
        //};

        // --Private--
        function loadRemoteData() {
            exService.getDogs()
            .then(
                function (dogs) {
                    applyRemoteData(dogs);
                }
            )
        };

        function applyRemoteData(newDogs) {
            $scope.dogs = newDogs;
        };
    });

    // --Dogs--
    app.factory('Dogs', function ($resource) {
        return $resource('http://localhost:5555/api/v1/dogs/:id', {}, {}, { stripTrailingSlashes: false });
    });

    app.controller('DogsController', ['$scope', 'Dogs', function ($scope, Dogs) {
        $scope.dogs = Dogs.query();
        //console.log($scope.dogs);  // [DEBUG-ONLY]
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
