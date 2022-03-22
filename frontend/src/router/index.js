import {createWebHistory, createRouter} from "vue-router";
import authorization from "../router/authorization";
const WorkSpace = () => import('../views/WorkSpace.vue');
const Tree = () => import('../components/FamilyTree/Tree.vue');
import store from "../store";


const routes = [
    {
        path: '/',
        redirect: {name: 'Login'},
        component: WorkSpace,
        children: [
            {
                path: '/tree',
                name: 'Tree',
                component: Tree,
                meta: {
                    isAuth: true,
                }
            }
        ]
    },
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
    if(store.getters.accessToken) {
        if(to.meta.isAuth) {
            next()
        } else {
            next({name: 'Tree'})
        }
    } else {
        if(to.meta.isAuth) {
            next({name: 'Login'})
        } else {
            next()
        }
    }
})

export default router