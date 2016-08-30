var AngularApp = angular.module('AngularApp', []);

AngularApp.controller('AngularCtrl', function ($scope) {
    $scope.selectedNumber = 0;
    $scope.avalibleNumbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    $scope.summ = 0;
    $scope.online = 0;

    $scope.handleNewSumm = function (data) {
        $scope.summ = JSON.parse(data).summ;
        $scope.online = JSON.parse(data).online;
        $scope.$apply()
    };

    $scope.setNumber = function (number) {
        $scope.selectedNumber = number;
        $scope.socket.send(number.toString());
    };

    $scope.init = function () {
        var host = window.location.hostname;
        var port = window.location.port;

        $scope.socket = new WebSocket("ws://" + host + ":" + port + "/ws");

        $scope.socket.onopen = function () {
            console.log("Соединение установлено.");
            $scope.socket.send($scope.selectedNumber.toString());
            $scope.$apply()
        };

        $scope.socket.onclose = function (event) {
            if (event.wasClean) {
                console.log('Соединение было закрыто');
            } else {
                console.log('Произошел сбой соединения');
            }
            $scope.$apply()
        };

        $scope.socket.onerror = function (error) {
            console.log("Ошибка " + error.message);
            $scope.$apply()
        };

        $scope.socket.onmessage = function (event) {
            $scope.handleNewSumm(event.data);
        };

        console.log($scope);

    };


});
