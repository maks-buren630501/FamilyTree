const URL = {
    LOGIN: 'authentication/login',
    REGISTRATION: 'authentication/registration',
    LOGOUT: 'authentication/logout',
    ACTIVATE: 'authentication/activate',
    REFRESH: 'authentication/refresh',
}

const EXTEND_ACCESS_URL = [
    URL.ACTIVATE,
    URL.REFRESH,
    URL.REGISTRATION
]
export default {
    URL,
    EXTEND_ACCESS_URL
}