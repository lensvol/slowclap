var event_blocks = [
    {
        name: "Block 1",
        start: new Date(30, 3, 2014, 12, 0, 0),
        events: [
            {
                duration: 120,
                name: "Event 1",
                id: "event1"
            },
            {
                duration: 160,
                name: "Event 1",
                id: "event2"
            },
            {
                duration: 180,
                name: "Event 1",
                id: "event3"
            }
        ]
    },
    {
        name: "Block 2",
        start: new Date(30, 3, 2014, 15, 0, 0),
        events: [
            {
                duration: 140,
                name: "Event A",
                id: "event1"
            },
            {
                duration: 260,
                name: "Event B",
                id: "event2"
            },
            {
                duration: 380,
                name: "Event C",
                id: "event3"
            }
        ]
    },
];

var BlockComponent = Vue.extend({
    template: '{{ name }}<br><div v-repeat="events" v-component="event" id="event-{{ id }}"></div>'
});

var EventComponent = Vue.extend({
    template: "{{ duration }} - {{ name }}"
});

Vue.component('event', EventComponent);
Vue.component('event-block', BlockComponent);

var roll = new Vue({
    el: "#roll",
    data: {
        blocks: event_blocks
    }
});
