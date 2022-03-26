import {createStore} from 'vuex';
import authorization from "./authorization";
import notification from "./notification";
import search from "./search";

export default createStore({
    modules: {
        authorization,
        notification,
        search
    }
})
