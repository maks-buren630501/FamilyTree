import axios from "../plugins/axios";

export default {
    state: {},
    getters: {},
    mutations: {},
    actions: {
        async registration({}, user) {
            return await axios.post('authentication/registration', user)
        }
    }
}