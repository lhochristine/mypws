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
        var queryType = "";
        var queryStr = "";

        console.log("In retrieve function... URL:" + $scope.JSON_URL);
        console.log("Query: " + query)
        if (!query.match("all")) {
            queryType = query.split("=")[0];
            queryStr = query.split("=")[1];
            console.log("QueryType: " + queryType + ", QueryStr: " + queryStr)
        }

        $http.get($scope.JSON_URL)
            .then(function successCallback(response) {
            //.success(function(data, status, headers, config) {
                $scope.filteredData = [];
                $scope.number = response.data.length;
                console.log("GET succeed...(" + $scope.number +")" + $scope.manifests)
                angular.forEach(response.data, function(manifest) {
                    console.log("manifest release:" + manifest.release + ", revision:" + manifest.revision)
                    if (queryType) {
                        if (query.startsWith("release")) {
                            console.log("filtering release...")
                            if (manifest.release.match(queryStr))
                                $scope.filteredData.push(manifest);
                        } else if (query.startsWith("revision")) {
                            console.log("filtering revision...")
                            if (queryStr.match("nonrc")) {
                                if (!manifest.revision.startsWith("rc")) {
                                    $scope.filteredData.push(manifest)
                                }
                            } else {
                                if (manifest.revision.startsWith(queryStr)) {
                                    $scope.filteredData.push(manifest)
                                }
                            }
                        }
                        $scope.manifests = $scope.filteredData
                    } else {
                        $scope.manifests = response.data;
                    }
                });
            })
            //.error(function(data, status, headers, config) {
            .catch(function errorCallback(response) {
                console.error("ERROR!!! GET failed.", response.status, response.data);
            })
            .finally(function() {
                console.log("Finally finished GET")
        });
    }

    $scope.MasterFilter = function(query) {
        console.log("In MasterFilter, query=" + query)
        $scope.colorChange();
        if (query.startsWith("ops")) {
            query = query.replace("ops", '');
            $scope.JSON_URL = path + '/release_manifest/api-json/mainfests/?sw_type=OPS';
        } else {
            $scope.JSON_URL = path + '/release_manifest/api-json/mainfests/?sw_type=PROD';
        }
        $scope.retrieve(query);
    }

    $scope.retrieve('');
});