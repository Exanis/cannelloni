app.factory('dump', function () {
    var data = {};
    
    return {
        set: function (target) {
            data = target;
        },

        get: function () {
            return data;
        }
    };
});