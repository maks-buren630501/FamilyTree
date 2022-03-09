import { createWebHistory, createRouter } from "vue-router";
import Authorization from '../views/Authorization.vue';
import LoginForm from '../components/Authorization/LoginForm.vue';
import RegistrationForm from '../components/Authorization/RegistrationForm.vue';

const routes = [
    {
        path: '/',
        component: Authorization,
        redirect: 'Login',
        children: [
            {
                path: '/login',
                name: 'Login',
                component: LoginForm,
                meta: {
                    title: 'Войдите в свой аккаунт',
                    link: 'Registration',
                    textLink: 'Зарегестрируйтесь'
                }
            },
            {
                path: '/registration',
                name: 'Registration',
                component: RegistrationForm,
                meta: {
                    title: 'Зарегестрируйте аккаунт',
                    link: 'Login',
                    textLink: 'Войдите в систему'
                }
            }
        ]
    }
]

export const router = createRouter({
    history: createWebHistory(),
    routes,
})
