const Authorization = () => import('../views/Authorization.vue');
const LoginForm = () => import('../components/Authorization/LoginForm.vue');
const RegistrationForm = () => import('../components/Authorization/RegistrationForm.vue');
const RegistrationConfirmForm = () => import('../components/Authorization/RegistrationConfirmForm.vue');
const EmailConfirmForm = () => import('../components/Authorization/EmailConfirmForm.vue');
const ForgotPasswordForm = () => import('../components/Authorization/ForgotPasswordForm.vue');
const ChangePasswordForm = () => import('../components/Authorization/ChangePasswordForm.vue');
import store from "../store";



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

function changePasswordConfirm(to, from, next) {
    if(from.name === 'ChangePassword') {
        next()
    } else {
        next({name: 'Login'})
    }
}


export default {
    path: '/',
    component: Authorization,
    children: [
        {
            path: 'email_confirm/:key',
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
        {
            path: '/forgot_password',
            name: 'ForgotPassword',
            component: ForgotPasswordForm,
            meta: {
                isAuth: false,
                title: 'Введите почту, на которую будет отправленна сылка, для смены пароля.'
            }
        },
        {
            path: '/forgot_password/:key',
            name: 'ChangePassword',
            component: ChangePasswordForm,
            // beforeEnter: [activateAccount],
            meta: {
                isAuth: false,
                title: 'Введите новый пароль'
            }
        },
        {
            path: '/forgot_password/:key/success',
            name: 'ChangePasswordConfirm',
            component: EmailConfirmForm,
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