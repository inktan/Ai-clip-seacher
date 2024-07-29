import { createApp, h } from 'vue'

export default function (cmp, props) {
    const app = createApp(
        {
            render() {
                return h(cmp, props);
            }
        }
    );
    const vm = app.mount(document.createElement('div'));
    return vm.$el;
}

