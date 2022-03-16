import { createWebHistory, createRouter } from "vue-router";
import Authorization from '../views/Authorization.vue';
import LoginForm from '../components/Authorization/LoginForm.vue';
import RegistrationForm from '../components/Authorization/RegistrationForm.vue';
import RegistrationConfirmForm from '../components/Authorization/RegistrationConfirmForm.vue';
import EmailConfirmForm from '../components/Authorization/EmailConfirmForm.vue';
import WorkSpace from '../views/WorkSpace.vue';
import Tree from '../components/FamilyTree/Tree.vue';

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
                }
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
                }
            },
        ]
    }
]

export const router = createRouter({
    history: createWebHistory(),
    routes,
})
