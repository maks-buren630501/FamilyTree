import axios from "../plugins/axios";
import router from "../router";
import config from "../plugins/config";

export default {
    state: {
        accessToken: null,
        accessTimeOut: null,
    },
    getters: {
        accessToken: state => state.accessToken,
        accessTimeOut: state => state.accessTimeOut
    },
    mutations: {
        setAuthenticationData: (state, {time_out: timeOut, access_token: accessToken}) => {
            state.accessTimeOut = new Date(timeOut * 1000)
            state.accessToken = accessToken
        },
        removeAuthenticationData: (state) => {
            state.accessTimeOut = null
            state.accessToken = false
        }
    },
    actions: {
        async registration({}, user) {
            return await axios.post(config.URL.REGISTRATION, user)
            .then(r => router.push({name: 'RegistrationConfirm'}))
            .catch(e => {})
        },
        async login({commit}, user) {
            await axios.post(config.URL.LOGIN, user)
                .then(r => {
                    commit('setAuthenticationData', r.data)
                    router.push({name: 'Tree'})
                })
                .catch(e => commit('removeAuthenticationData'))
        },
        async logout({commit}) {
            await axios.get(config.URL.LOGOUT)
                .finally(r => {
                    commit('removeAuthenticationData')
                    router.push({name: 'Login'})
                })
        },
        async activate({}, key) {
            return await axios.put(`${config.URL.ACTIVATE}/${key}`)
        },
        async refresh({commit}) {
            await axios.get(config.URL.REFRESH)
                .then(r => commit('setAuthenticationData', r.data))
                .catch(e => commit('removeAuthenticationData'))
        },
        async refreshToken({getters, dispatch}) {
            if(getters.accessToken) {
                if(getters.accessTimeOut - new Date() - 600000 <= 0) {
                    await dispatch('refresh')
                }
            } else if(getters.accessToken === null) {
                await dispatch('refresh')
            }
        },
        async forgotPasswordEmail({}, email) {
            await axios.post(config.URL.FORGOT_PASSWORD_EMAIL, {email})
                .then(r => router.push({name: 'ForgotPasswordConfirm'}))
                .catch(e => {})
        },
        async changePasswordPermission({}, key) {
            return await axios.get(`${config.URL.CHANGE_PASSWORD_PERMISSION}/${key}`)
        },
        async changePassword({}, {password, key}) {
            return await axios.put(`${config.URL.CHANGE_PASSWORD}/${key}`, {password})
                .then(r => {
                    if(r.status === 200) {
                        router.push({name: 'ChangePasswordConfirm', params: {key}})
                    }
                })
        }
    }
}