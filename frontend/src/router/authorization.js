const Authorization = () => import('../views/Authorization.vue');
const LoginForm = () => import('../components/Authorization/LoginForm.vue');
const RegistrationForm = () => import('../components/Authorization/RegistrationForm.vue');
const ConfirmEmailForm = () => import('../components/Authorization/ConfirmEmailForm.vue');
const ConfirmForm = () => import('../components/Authorization/ConfirmForm.vue');
const ForgotPasswordForm = () => import('../components/Authorization/ForgotPasswordForm.vue');
const ChangePasswordForm = () => import('../components/Authorization/ChangePasswordForm.vue');
import store from "../store";



function confirmRegistration(to, from, next) {
    if(from.name === 'Registration') {
        next()
    } else {
        next({name: 'Login'})
    }
}

function confirmPassword(to, from, next) {
    if(from.name === 'ForgotPassword') {
        next()
    } else {
        next({name: 'Login'})
    }
}

function changePasswordConfirm(to, from, next) {
    if(from.name === 'ChangePassword') {
        next()
    } else {
        next({name: 'Login'})
    }
}

function changePasswordPermission(to, from, next) {
    store.dispatch('changePasswordPermission', to.params.key)
        .then(r => next())
        .catch(e => next({name: 'Login'}))
}


function activateAccount(to, from, next) {
    store.dispatch('activate', to.params.key)
        .then(r => next())
        .catch(e => next({name: 'Login'}))
}


export default {
    path: '/',
    component: Authorization,
    children: [
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
            component: ConfirmEmailForm,
            beforeEnter: [confirmRegistration],
            meta: {
                isAuth: false,
                title: 'Успешно. Проверьте свою почту.',
                link: 'Login',
                textLink: 'а после войдите в систему'
            }
        },
        {
            path: '/forgot',
            name: 'ForgotPassword',
            component: ForgotPasswordForm,
            meta: {
                isAuth: false,
                title: 'Введите почту, на которую будет отправленна сылка, для смены пароля.'
            }
        },
        {
            path: '/forgot/confirm',
            name: 'ForgotPasswordConfirm',
            component: ConfirmEmailForm,
            beforeEnter: [confirmPassword],
            meta: {
                isAuth: false,
                title: 'Успешно. Проверьте свою почту.',
                link: 'Login',
                textLink: 'а после войдите в систему'
            }
        },
        {
            path: '/forgot/:key',
            name: 'ChangePassword',
            component: ChangePasswordForm,
            beforeEnter: [changePasswordPermission],
            meta: {
                isAuth: false,
                title: 'Введите новый пароль'
            }
        },
        {
            path: '/forgot/:key/success',
            name: 'ChangePasswordConfirm',
            component: ConfirmForm,
            beforeEnter: [changePasswordConfirm],
            meta: {
                isAuth: false,
                title: 'Ваш пароль изменен',
                link: 'Login',
                textLink: 'Войдите в систему'
            }
        }
    ]
}