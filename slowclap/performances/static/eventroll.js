function EventBlock(name, start, events) {
    this.name = name;
    this.start = start;
    this.events = events;

    this.recalculate();
};

function Event(event_id, category, name, duration) {
    this.name = name;
    this.category = category;
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

/*
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
*/


function loadProgram(){
    var self = this;

    $.ajax('/performances/list/blocks', {
        success: function(blocks){
            self.blocks = {};
            for(var bl_id = 0; bl_id < blocks.length; bl_id++){
                self.blocks[blocks[bl_id].id] = blocks[bl_id];
            }

            $.ajax('/performances/list/categories', {
                success: function(categories){
                    self.categories = {};
            
                    for(var cat_id = 0; cat_id < categories.length; cat_id++){
                        self.categories[categories[cat_id].id] = categories[cat_id];
                    }

                    $.ajax('/performances/list/events', {
                        success: function(events){
                            self.events = {};
                            for(var i= 0; i < events.length; i++){
                                ev = events[i];
                                self.events[ev.id] = new Event(
                                    "event_" + ev.id,
                                    ev.category ? ev.category.name : "(неизвестно)",
                                    ev.description,
                                    ev.duration);
                            }
                            $.ajax('/performances/list/program', {
                                 success: function(by_blocks){
                                    event_blocks = [];
                                    var by_start_date = function(a, b){
                                        return a.start - b.start
                                    }
                                    for(key in by_blocks){
                                        if(by_blocks.hasOwnProperty(key)){
                                            console.log(key);
                                            block_def = self.blocks[key];
                                            var in_block = [];
                                            var event_ids = by_blocks[key];
                                            for(var b_i = 0; b_i < event_ids.length; b_i++){
                                                in_block.push(self.events[event_ids[b_i]]);
                                            }
                                            event_blocks.push(new EventBlock(
                                                block_def.name,
                                                block_def.start,
                                                in_block));
                                        }
                                    }
                                    event_blocks = event_blocks.sort(by_start_date);
                                    var roll = new Vue({
                                        el: "#roll",
                                        data: {
                                            blocks: event_blocks
                                        }});

                                }});
                        }
                    });
                    // $.ajax('/performances/list/program', {
                    //     success: function(program){
                    //         // var roll = new Vue({
                    //         //     el: "#roll",
                    //         //     data: {
                    //         //         blocks: event_blocks
                    //         //     },
                    //         //     methods: {
                    //         //         set_active: function(ev_id, is_active){
                    //         //             this.$broadcast('status-changed', ev_id, is_active)
                    //         //             //$('html,body').animate({scrollTop:$("#event-" + ev_id).offset().top}, 500);
                    //         //         }
                    //         //     }
                    //         // });

                    //     }});

                }
            });
        }
    });
}

loadProgram();