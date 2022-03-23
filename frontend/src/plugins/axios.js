import axios from "axios";
import store from "../store";
import config from "./config";

const http = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  withCredentials: true
})


http.interceptors.request.use(
    async function (requestConfig) {
        if(!config.EXTEND_ACCESS_URL.includes(requestConfig.url)) {
            await store.dispatch('refreshToken')
            requestConfig.headers.common['x-access-token'] = store.getters.accessToken
        }
        return requestConfig
        },
    function (error) {
        return Promise.reject(error)
    }
);

function findValueByPrefix(object, prefix) {
  for (const property in object) {
    if (object.hasOwnProperty(property) &&
       prefix.startsWith(property)) {
       return object[property];
    }
  }
}

http.interceptors.response.use(
    function (response) {
        return response;
    },
    async function (er) {
        const error = er.toJSON()
        const url = error.config.url
        const status = error.status
        await store.dispatch('addAlert', {
            type: 'error',
            body: findValueByPrefix(config.MESSAGE_STATUS_CODE, url)[status]
        })
        return Promise.reject(er);
    }
);

export default http
