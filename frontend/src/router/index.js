import {createWebHistory, createRouter} from "vue-router";
import authorization from "../router/authorization";
import workspace from "./workspace";
import store from "../store";


const routes = [
    workspace,
    authorization,
    // {
    //     path: '/:catchAll(.*)*',
    //     name: "PageNotFound",
    //     component: PageNotFound,
    // },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})


router.beforeEach(async (to, from, next) => {
    await store.dispatch('refreshToken')
    if (store.getters.accessToken) {
        if (to.meta.isAuth) {
            next()
        } else {
            next({name: 'Tree'})
        }
    } else {
        if (to.meta.isAuth) {
            next({name: 'Login'})
        } else {
            next()
        }
    }
})

export default router