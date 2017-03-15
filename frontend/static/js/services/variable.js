app.factory('variable', function () {
    var variable = {};
    
    return {
        set: function (target) {
            variable = target;
        },

        get: function () {
            return variable;
        }
    };
});