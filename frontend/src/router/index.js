import { createWebHistory, createRouter } from "vue-router";
import Authorization from '../views/Authorization.vue';
import LoginForm from '../components/Authorization/LoginForm.vue';
import RegistrationForm from '../components/Authorization/RegistrationForm.vue';
import EmailConfirmForm from '../components/Authorization/EmailConfirmForm.vue';

const routes = [
    {
        path: '/',
        component: Authorization,
        redirect: 'Login',
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
            }
        ]
    }
]

export const router = createRouter({
    history: createWebHistory(),
    routes,
})
