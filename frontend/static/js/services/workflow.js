app.factory('workflow', function () {
    var uuid = '';
    
    return {
        set: function (target) {
            uuid = target;
        },

        get: function () {
            return uuid;
        }
    };
});