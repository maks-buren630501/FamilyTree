const URL = {
    LOGIN: 'authentication/login',
    REGISTRATION: 'authentication/registration',
    LOGOUT: 'authentication/logout',
    ACTIVATE: 'authentication/activate',
    REFRESH: 'authentication/refresh',
    FORGOT_PASSWORD_EMAIL: 'authentication/start_recovery_password',
    CHANGE_PASSWORD_PERMISSION: 'authentication/check_recovery_password',
    CHANGE_PASSWORD: 'authentication/recovery_password'
}

const EXTEND_ACCESS_URL = [
    URL.ACTIVATE,
    URL.REFRESH,
    URL.REGISTRATION,
    URL.FORGOT_PASSWORD_EMAIL,
    URL.CHANGE_PASSWORD_PERMISSION,
    URL.CHANGE_PASSWORD
]
export default {
    URL,
    EXTEND_ACCESS_URL
}