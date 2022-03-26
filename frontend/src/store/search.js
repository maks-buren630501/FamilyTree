export default {
    state: {
        searchRequest: '',
        selfPeople: [
            {
                name: 'Ivanov Ivan Ivanovich',
                date: '12.12.1978-17.06.2003'
            },
            {
                name: 'Vasilev Anatoliy Genadievich',
                date: '12.12.1978-17.06.2003'
            },
            {
                name: 'Klarson Kent Anatolievich',
                date: '12.12.1978-17.06.2003'
            },
            {
                name: 'Slimus Ruslan Andreevich',
                date: '12.12.1978-17.06.2003'
            }
        ],
        globalPeople: [
            {
                name: 'Asmaa O\'Brien Ivanovich',
                date: '12.12.1978-17.06.2003'
            },
            {
                name: 'Isla-Mae Kaye Genadievich',
                date: '12.12.1978-17.06.2003'
            },
            {
                name: 'Jaydon Little Anatolievich',
                date: '12.12.1978-17.06.2003'
            },
            {
                name: 'Barbara Walters Andreevich',
                date: '12.12.1978-17.06.2003'
            },
            {
                name: 'Brent Keller Genaf',
                date: '12.12.1978-17.06.2003'
            }
        ],
        searchGraph: true,
        searchSelf: true,
        searchGlobal: true,
    },
    getters: {
        searchRequest: state => state.searchRequest,
        searchGraph: state => state.searchGraph,
        searchSelf: state => state.searchSelf,
        searchGlobal: state => state.searchGlobal,
        selfPeople: state => state.selfPeople,
        globalPeople: state => state.globalPeople
    },
    mutations: {
        setSearchRequest: (state, request) => state.searchRequest = request,
        setSearchGraph: (state, status) => state.searchGraph = status,
        setSearchSelf: (state, status) => state.searchSelf = status,
        setSearchGlobal: (state, status) => state.searchGlobal = status
    },
    actions: {
        setSearchRequest({commit}, request) {
            commit('setSearchRequest', request)
        },
        setSearchGraph({commit}, status) {
            commit('setSearchGraph', status)
        },
        setSearchSelf({commit}, status) {
            commit('setSearchSelf', status)
        },
        setSearchGlobal({commit}, status) {
            commit('setSearchGlobal', status)
        }
    }
}