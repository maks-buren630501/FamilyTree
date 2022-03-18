import axios from "../plugins/axios";
import {router} from "../router";

export default {
    state: {
        isAuthenticated: null,
    },
    getters: {
        isAuthenticated: state => state.isAuthenticated
    },
    mutations: {
        setAuthenticatedStatus: (state, status) => state.isAuthenticated = status
    },
    actions: {
        async registration({}, user) {
            return await axios.post('authentication/registration', user)
        },
        async login({}, user) {
            return await axios.post('authentication/login', user)
        },
        async logout({commit}) {
          await axios.get('authentication/logout')
            .finally(r => {
                delete axios.defaults.headers.common['x-access-token']
                commit('setAuthenticatedStatus', false)
                router.push({name: 'Login'})
            })
        },
        async activate({}, key) {
            return await axios.put(`authentication/activate/${key}`)
        },
        async refresh({commit}) {
            await axios.get('authentication/refresh')
                .then(r => {
                    axios.defaults.headers.common['x-access-token'] = r.data
                    commit('setAuthenticatedStatus', true)
                })
                .catch(e => commit('setAuthenticatedStatus', false))
        }
    }
}