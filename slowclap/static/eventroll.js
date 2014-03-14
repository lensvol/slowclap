function EventBlock(name,  start, events) {
    this.name = name;
    this.start = start;
    this.events = events;

    this.filtered_out = false;

    this.recalculate();
};

function Event(event_id, category, name, duration) {
    this.name = name;
    this.category = category;
    this.event_id = event_id;
    this.duration = duration;
    this.active = true;
    this.hidden = false;
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
        this.$on('filter-changed', function(){
            var flt = this.$root.filter_by;

            this.events.replace(function(item){
                if((flt.category && flt.category != item.category)
                    || (flt.text && item.name.toLowerCase().indexOf(flt.text.toLowerCase()) == -1))
                {
                    item.hidden = true;
                }else{
                    item.hidden = false;
                }
                return item;                
            });

            var count = this.events.length;
            for(var i = 0; i < this.events.length; i++){
                if(this.events[i].hidden){
                    count--;
                }
            }
            this.filtered_out = count == 0;
        });
    },
});

var EventComponent = Vue.extend({    
    created: function() {
        this.$on('status-changed', function(ev_id, is_active){
            if(ev_id == this.event_id){
                this.active = is_active;
                console.log("Found on " + this.event_id);
                this.$dispatch('event-changed');
            }
        });
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

var roll = null;

$(document).ready(function(){
    var self = this;
    $("#placeholder").show();

    $.ajax('list/events', {
        success: function(events){
            self.events = {};
            self.blocks = {};
            self.categories = {};

            for(var i= 0; i < events.length; i++){
                ev = events[i];
                self.events[ev.id] = new Event(
                    "event_" + ev.id,
                    ev.category ? ev.category.name : "",
                    ev.description,
                    ev.duration);

                if(ev.category){
                    self.categories[ev.category.id] = ev.category;
                }

                if(ev.block){
                    self.blocks[ev.block.id] = ev.block;
                }
            }
            $.ajax('list/program', {
                 success: function(by_blocks){
                    event_blocks = [];
                    var by_start_date = function(a, b){
                        return a.start - b.start
                    }
                    for(key in by_blocks){
                        if(self.blocks.hasOwnProperty(key)){
                            block_def = self.blocks[key];
                            var in_block = [];
                            var event_ids = by_blocks[key];
                            for(var b_i = 0; b_i < event_ids.length; b_i++){
                                in_block.push(self.events[event_ids[b_i]]);
                            }
                            event_blocks.push(new EventBlock(block_def.name, block_def.start, in_block));
                        }
                    }
                    event_blocks = event_blocks.sort(by_start_date);

                    roll = new Vue({
                        el: "#roll",
                        data: {
                            blocks: event_blocks,
                            categories: self.categories,
                            text_filter: null,
                            filter_by: {
                                category: 'Все категории',
                                text: null
                            }
                        },
                        methods: {
                            setCategoryFilter: function(value){
                                this.filter_by.category = value.name;
                            },
                            clearCategoryFilter: function(){
                                this.filter_by.category = 'Все категории';
                            },
                            filterByText: function(){
                                this.filter_by.text = this.text_filter;
                            }
                        },
                        ready: function(){
                            console.log('Ok!');
                            $("#placeholder").hide();
                            $('#roll').show();
                            this.$watch('filter_by', function(){
                                console.log('Filter changed:' + this.filter_by.text + ' in ' + this.filter_by.category);
                                this.$broadcast('filter-changed');
                            })
                        } 
                    });
                }});
        }
    });
});
