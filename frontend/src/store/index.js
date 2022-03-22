import { createStore } from 'vuex';
import authorization from "./authorization";
import notification from "./notification";

export default createStore({
    modules: {
        authorization,
        notification
    }
})
