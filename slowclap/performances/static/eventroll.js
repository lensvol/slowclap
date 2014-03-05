function EventBlock(name, start, events) {
    this.name = name;
    this.start = start;
    this.events = events;

    this.recalculate();
};

function Event(event_id, name, duration) {
    this.name = name;
    this.event_id = event_id;
    this.duration = duration;
    this.active = true;
};

EventBlock.prototype = {
    recalculate: function() {
        var point = new Date(this.start);
        for(var i = 0; i < this.events.length; i++){
            var ev = this.events[i];
            if(ev.active){
                ev.start = new Date(point);
                point.setSeconds(point.getSeconds() + ev.duration);
            }
        }
    }
}


var event_blocks = [];

for(var i = 1; i < 10; i++){
    var new_events = []

    for(var a = 1; a < 31; a++){
        new_events.push(new Event(
            i + "_" + a, 
            "Event #" + i + "-" + a,
            120))
    }
    event_blocks.push(new EventBlock(
        "Block #" + i, 
        new Date(2014, 3, 30, 10 + i, 0, 0),
        new_events))
}

var BlockComponent = Vue.extend({
    created: function(){
        this.$on('event-changed', function(){
            console.log('Recalculating...');
            this.recalculate();
        });
    }
});

var EventComponent = Vue.extend({    
    created: function() {
        this.$on('status-changed', function(ev_id, is_active){
            if(ev_id == this.event_id){
                this.active = is_active;
                console.log("Found on " + this.event_id);
                this.$dispatch('event-changed');
            }
        })
    }
});

Vue.component('event', EventComponent);
Vue.component('event-block', BlockComponent);
Vue.filter('hourmin', function(value){
    hour = value.getHours();
    minutes = value.getMinutes();

    return (hour < 10 ? "0" + hour : hour) + ":" +
           (minutes < 10 ? "0" + minutes : minutes)
})

var roll = new Vue({
    el: "#roll",
    data: {
        blocks: event_blocks
    },
    methods: {
        set_active: function(ev_id, is_active){
            this.$broadcast('status-changed', ev_id, is_active)
            $('html,body').animate({scrollTop:$("#event-" + ev_id).offset().top}, 500);
        }
    }
});
