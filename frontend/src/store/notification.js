export default {
    state: {
        alerts: []
    },
    getters: {
        alerts: state => state.alerts,
    },
    mutations: {
        addAlert: (state, alert) => {
            state.alerts.push(alert)
        },
        removeAlert: (state, alert) => {
            console.log(state.alerts.findIndex(a => a === alert))
            state.alerts.splice(state.alerts.findIndex(a => a === alert), 1)
        }
    },
    actions: {
        addAlert({commit}, alert) {
            commit('addAlert', alert)
        },
        removeAlert({commit}, alert) {
            commit('removeAlert', alert)
        },
    },
}