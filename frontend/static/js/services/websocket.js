app.factory('$websocket', ['$location', '$mdToast', function ($location, $mdToast) {
    var ws = null;
    var handlers = {};

    return {
        connect: function (handler) {
            ws = new WebSocket('ws://' + window.location.host + '/');
            ws.onopen = handler;

            ws.onmessage = function (e) {
                var data = JSON.parse(e.data);
                if (typeof handlers[data['command']] !== "undefined")
                    handlers[data['command']](data);
            };

            ws.onclose = function () {
                $mdToast.show(
                    $mdToast.simple()
                            .textContent('Connexion perdue au serveur')
                            .position('bottom right')
                            .hideDelay(3000)
                );
                $location.path('/');
            };

            ws.onerror = function () {
                $mdToast.show(
                    $mdToast.simple()
                            .textContent('Connexion perdue au serveur')
                            .position('bottom right')
                            .hideDelay(3000)
                );
                $location.path('/');
            };
        },

        disconnect: function () {
            if (null == ws) {
                $location.path('/');
            } else
                ws.close();
        },

        send: function (uuid, command, params = {}) {
            if (null == ws) {
                $location.path('/');
            } else
                ws.send(JSON.stringify({
                    uuid: uuid,
                    command: command,
                    params: params
                }));
        },

        hook: function (ev, handler) {
            if (null == ws) {
                $location.path('/');
            } else {
                handlers[ev] = handler;
            }
        },

        clear: function () {
            if (null == ws) {
                $location.path('/');
            } else
                handlers = {};
        }
    };
}]);