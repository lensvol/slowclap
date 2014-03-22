function EventBlock(block_id, name,  start, events) {
    this.name = name;
    this.start = new Date(start);
    this.events = events;
    this.block_id = block_id

    this.filtered_out = false;

    this.recalculate();
};

function Event(event_id, category, name, duration, number) {
    this.name = name;
    this.category = category;
    this.event_id = event_id;
    this.duration = duration;
    this.number = number;

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

            // JavaScript is weird :( Hack to compare two dates.
            filtered_by_date = (this.start.setHours(0,0,0,0) == flt.date.setHours(0,0,0,0));
            if(filtered_by_date){
                this.events.replace(function(item){
                    if((flt.category && flt.category != item.category && flt.category != 'Все категории')
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

                this.filtered_out = (count == 0)
            }else{
                this.filtered_out = true
            }
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
});
Vue.filter('shortdate', function(value){
    day = value.getDate();
    month = value.getMonth();
    months = ["Январь", "Февраль", "Март", "Апрель", "Ма",
              "Июнь", "Июль", "Август", "Сентябрь", "Октябрь",
              "Ноябрь", "Декабрь"];

    return months[month] + ', ' + day
})



var roll = null;

$(document).ready(function(){
    var self = this;
    $("#noscript").hide();
    $("#placeholder").show();

    $.ajax('list/events', {
        success: function(events){
            self.events = {};
            self.blocks = {};
            self.categories = {};
            self.dates = [];

            for(var i= 0; i < events.length; i++){
                ev = events[i];
                self.events[ev.id] = new Event(
                    "event_" + ev.id,
                    ev.category ? ev.category.name : "",
                    ev.description,
                    ev.duration,
                    ev.number
                );

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
                    dates = [];
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
                            event_blocks.push(new EventBlock(key, block_def.name, block_def.start, in_block));

                            day_start = new Date(block_def.start);
                            ts = day_start.setHours(0, 0, 0, 0);
                            if(dates.indexOf(ts) == -1){
                                dates.push(ts);
                            }
                        }
                    }
                    self.dates = dates.map(function(ts, ind, arr){
                        return new Date(ts)
                    });
                    event_blocks = event_blocks.sort(by_start_date);
                    roll = new Vue({
                        el: "#roll",
                        data: {
                            blocks: event_blocks,
                            categories: self.categories,
                            dates: self.dates,
                            text_filter: null,
                            filter_by: {
                                category: 'Все категории',
                                text: null,
                                date: null
                            }
                        },
                        methods: {
                            setCategoryFilter: function(value){
                                this.filter_by.category = value.name;
                            },
                            clearCategoryFilter: function(){
                                this.filter_by.category = 'Все категории';
                            },
                            filterByText: function(e){
                                this.filter_by.text = this.text_filter;
                            },
                            filterByDate: function(date) {
                                this.filter_by.date = date;
                            },
                        },
                        created: function(){
                            this.$watch('filter_by', function(){
                                console.log('Filter changed:' + this.filter_by.text + ' in ' + this.filter_by.category + ' on ' + this.filter_by.date);
                                this.$broadcast('filter-changed');
                            });
                            this.filter_by.date = this.dates[0];
                        },
                        ready: function(){
                            this.$broadcast('filter-changed');
                            console.log('Ok!');
                            $("#placeholder").hide();
                            $('#roll').show();
                        }
                    });
                }});
        }
    });
});
