function EventBlock(block_id, name,  start, events) {
    this.name = name;
    this.start = new Date(start);
    this.events = events;
    this.block_id = block_id

    console.log("Block " + block_id + " starts on " + start);
    console.log("Date: " + this.start);
    m = moment(start)
    console.log("Moment date: " + m.format())

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
            filtered_by_date = (moment(this.start).dayOfYear() == moment.unix(flt.date).dayOfYear());
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
    var m = moment(value).tz("Europe/Moscow");
    return m.format("hh:mm");
});
Vue.filter('shortdate', function(value){
    return moment.unix(value).format("MMM, D")
})

moment.tz.add({
    "zones": {
        "Europe/Moscow": [
            "2:30:20 - LMT 1880 2:30:20",
            "2:30 - MMT 1916_6_3 2:30",
            "2:30:48 Russia %s 1919_6_1_2 4:30:48",
            "3 Russia MSK/MSD 1922_9 3",
            "2 - EET 1930_5_21 2",
            "3 Russia MSK/MSD 1991_2_31_2 3",
            "2 Russia EE%sT 1992_0_19_2 2",
            "3 Russia MSK/MSD 2011_2_27_2 3",
            "4 - MSK"
        ]
    },
    "rules": {
        "Russia": [
            "1917 1917 6 1 7 23 0 1 MST",
            "1917 1917 11 28 7 0 0 0 MMT",
            "1918 1918 4 31 7 22 0 2 MDST",
            "1918 1918 8 16 7 1 0 1 MST",
            "1919 1919 4 31 7 23 0 2 MDST",
            "1919 1919 6 1 7 2 0 1 S",
            "1919 1919 7 16 7 0 0 0",
            "1921 1921 1 14 7 23 0 1 S",
            "1921 1921 2 20 7 23 0 2 M",
            "1921 1921 8 1 7 0 0 1 S",
            "1921 1921 9 1 7 0 0 0",
            "1981 1984 3 1 7 0 0 1 S",
            "1981 1983 9 1 7 0 0 0",
            "1984 1991 8 0 8 2 2 0",
            "1985 1991 2 0 8 2 2 1 S",
            "1992 1992 2 6 8 23 0 1 S",
            "1992 1992 8 6 8 23 0 0",
            "1993 2010 2 0 8 2 2 1 S",
            "1993 1995 8 0 8 2 2 0",
            "1996 2010 9 0 8 2 2 0"
        ]
    },
    "links": {}
});

var roll = null;

$(document).ready(function(){
    var self = this;
    $("#noscript").hide();
    $("#placeholder").show();

    $.ajax('list/events', {
        success: function(events){
            console.log("Retrieved " + events.length + " events from server.")
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
                    console.log("Ordering events according to program...");
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
                            day_start = moment(block_def.start);
                            ts = day_start.hours(0).minutes(0).seconds(0).unix();
                            if(dates.indexOf(ts) == -1){
                                dates.push(ts);
                            }
                        }
                    }
                    self.dates = dates.map(function(ts, ind, arr){
                        return moment.unix(ts)
                    });
                    event_blocks = event_blocks.sort(by_start_date);
                    console.log("Creating VM...");
                    roll = new Vue({
                        el: "#roll",
                        data: {
                            blocks: event_blocks,
                            categories: self.categories,
                            dates: dates,
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
                            console.log("VM is being created...");
                            this.$watch('filter_by', function(){
                                console.log('Filter changed: "' + (this.filter_by.text || "") + '" in ' + this.filter_by.category + ' on ' + this.filter_by.date);
                                this.$broadcast('filter-changed');
                            });
                            this.filter_by.date = this.dates[0];
                        },
                        ready: function(){
                            this.$broadcast('filter-changed');
                            console.log('VM is ready.');
                            $("#placeholder").hide();
                            $('#main').show();
                        }
                    });
                }});
        }
    });
});
