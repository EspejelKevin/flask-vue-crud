import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "bootstrap/dist/css/bootstrap.css"


const app = createApp(App)
    .use(router)
    .use(store);

router.isReady().then(() => {
    app.mount("#app");
})

import "bootstrap/dist/js/bootstrap.js"
