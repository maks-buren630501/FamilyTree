import {createWebHistory, createRouter} from "vue-router";
import Authorization from '../views/Authorization.vue';
import LoginForm from '../components/Authorization/LoginForm.vue';
import RegistrationForm from '../components/Authorization/RegistrationForm.vue';
import RegistrationConfirmForm from '../components/Authorization/RegistrationConfirmForm.vue';
import EmailConfirmForm from '../components/Authorization/EmailConfirmForm.vue';
import WorkSpace from '../views/WorkSpace.vue';
import Tree from '../components/FamilyTree/Tree.vue';
import {store} from "../store";


function activateAccount(to, from, next) {
    console.log(to, from, next)
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
                component: Tree
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
                meta: {
                    title: 'Ваш аккаунт подтвержден',
                    link: 'Login',
                    textLink: 'Войдите в систему'
                },
                beforeEnter: [activateAccount]
            },
            {
                path: '/authentication',
                name: 'Login',
                component: LoginForm,
                meta: {
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
                    title: 'Зарегестрируйте аккаунт',
                    link: 'Login',
                    textLink: 'или войдите в систему'
                }
            },
            {
                path: '/registration_confirm',
                name: 'RegistrationConfirm',
                component: RegistrationConfirmForm,
                meta: {
                    title: 'Успешно. проверьте свою почту.',
                    link: 'Login',
                    textLink: 'а после войдите в систему'
                }
            },
        ]
    }
]

export const router = createRouter({
    history: createWebHistory(),
    routes,
})
