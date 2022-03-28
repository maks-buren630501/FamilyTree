import {createStore} from 'vuex';
import authorization from "./authorization";
import notification from "./notification";
import search from "./search";

export default createStore({
    modules: {
        authorization,
        notification,
        search
    },
    state: {
        mobileSideBar: false
    },
    getters: {
        mobileSideBar: state => state.mobileSideBar
    },
    mutations: {
        setMobileSideBar: (state, status) => state.mobileSideBar = status
    },
    actions: {
        setMobileSideBar: ({commit}, status) => commit('setMobileSideBar', status)
    }
})
