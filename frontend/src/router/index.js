import {createWebHistory, createRouter} from "vue-router";
const Authorization = () => import('../views/Authorization.vue');
const LoginForm = () => import('../components/Authorization/LoginForm.vue');
const RegistrationForm = () => import('../components/Authorization/RegistrationForm.vue');
const RegistrationConfirmForm = () => import('../components/Authorization/RegistrationConfirmForm.vue');
const EmailConfirmForm = () => import('../components/Authorization/EmailConfirmForm.vue');
const WorkSpace = () => import('../views/WorkSpace.vue');
const Tree = () => import('../components/FamilyTree/Tree.vue');
import {store} from "../store";

function confirmRegistration(to, from, next) {
    if(from.name !== 'Registration') {
        next({name: 'Registration'})
    } else {
        next()
    }
}


function activateAccount(to, from, next) {
    store.dispatch('activate', to.params.key)
        .then(r => {
            if(r.status === 204) {
                next({name: 'Login'})
            } else {
                next()
            }
        })
        .catch(e => {
            next({name: 'Login'})
        })
}

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
    {
        path: '/',
        component: Authorization,
        children: [
            {
                path: '/:key',
                name: 'EmailConfirm',
                component: EmailConfirmForm,
                beforeEnter: [activateAccount],
                meta: {
                    isAuth: false,
                    title: 'Ваш аккаунт подтвержден',
                    link: 'Login',
                    textLink: 'Войдите в систему'
                }
            },
            {
                path: '/authentication',
                name: 'Login',
                component: LoginForm,
                meta: {
                    isAuth: false,
                    title: 'Войдите в свой аккаунт',
                    link: 'Registration',
                    textLink: 'или зарегестрируйтесь'
                }
            },
            {
                path: '/registration',
                name: 'Registration',
                component: RegistrationForm,
                meta: {
                    isAuth: false,
                    title: 'Зарегестрируйте аккаунт',
                    link: 'Login',
                    textLink: 'или войдите в систему'
                }
            },
            {
                path: '/registration_confirm',
                name: 'RegistrationConfirm',
                component: RegistrationConfirmForm,
                beforeEnter: [confirmRegistration],
                meta: {
                    isAuth: false,
                    title: 'Успешно. Проверьте свою почту.',
                    link: 'Login',
                    textLink: 'а после войдите в систему'
                }
            },
        ]
    }
    // {
    //     path: '/:catchAll(.*)*',
    //     name: "PageNotFound",
    //     component: PageNotFound,
    // },
]

export const router = createRouter({
    history: createWebHistory(),
    routes,
})


router.beforeEach(async (to, from, next) => {
    if(store.getters.isAuthenticated === null) {
        await store.dispatch('refresh')
    }
    if(store.getters.isAuthenticated) {
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
