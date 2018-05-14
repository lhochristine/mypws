var manifestApp = angular.module('manifestApp', []);

manifestApp.controller('ManifestController', function($scope, $http) {
    var path;

    $scope.sortType = 'date_added';
    $scope.sortReverse = true;
    $scope.searchManifest = '';

    console.log("location host:" + location.host + ', JSON_URL: ' + $scope.JSON_URL)

    if (location.host.startsWith('binbin')) {
        path = 'https://' + location.host
    } else {
        path = 'http://' + location.host
    }

    // default URL
    $scope.JSON_URL = path + '/release_manifest/api-json/mainfests/?sw_type=PROD';
    console.log("get URL: " + $scope.JSON_URL);

    $scope.colorChange = function () {
        $(document).on('click', '.nav-list li', function() {
            $(".nav-list li").removeClass("active");
            $(this).addClass("active");
        });
    }

    // retrieve function
    $scope.retrieve = function (query) {
        console.log("In retrieve function... URL:" + $scope.JSON_URL)
        $http.get($scope.JSON_URL)
            .then(function successCallback(response) {
            //.success(function(data, status, headers, config) {
                $scope.manifests = response.data;
                $scope.number = response.data.length;
                console.log("GET succeed...(" + $scope.number +")" + $scope.manifests)
                angular.forEach(response.data, function(manifest) {
                    console.log("manifest release:" + manifest.release)
                });
            })
            //.error(function(data, status, headers, config) {
            .catch(function errorCallback(response) {
                console.error("ERROR!!! GET failed.", resonse.status, response.data);
            })
            .finally(function() {
                console.log("Finally finished GET")
        });
    }

    $scope.MasterFilter = function(query) {
        console.log("In MasterFilter, query=" + query)
        $scope.colorChange();
        if (query.startsWith("ops")) {
            $scope.JSON_URL = path + '/release_manifest/api-json/mainfests/?sw_type=OPS';
        } else {
            $scope.JSON_URL = path + '/release_manifest/api-json/mainfests/?sw_type=PROD';
        }
        $scope.retrieve(query);
    }

    $scope.retrieve();
});