(function () {
    var app = angular.module('dogApi', []);

    app.config(['$interpolateProvider', function($interpolateProvider){
        $interpolateProvider.startSymbol('{-');
        $interpolateProvider.endSymbol('-}');
    }]);

    app.controller('FacilityController', ['$http', function($http){
        var facility = this;

        facility.dogs = [];

        //$http.get('http://localhost:5555/api/v1/dogs/').success(function(data){
        //    facility.dogs = data.dogs;
        //    console.log(facility.dogs);
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

    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": false,
        "progressBar": true,
        "positionClass": "toast-top-right",
        "preventDuplicates": true,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    }

})();
