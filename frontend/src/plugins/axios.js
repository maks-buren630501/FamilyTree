import axios from "axios";
import store from "../store";
import config from "./config";

const http = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  withCredentials: true
})



http.interceptors.request.use(async function (requestConfig) {
    if(!config.EXTEND_ACCESS_URL.includes(requestConfig.url)) {
        await store.dispatch('refreshToken')
        requestConfig.headers.common['x-access-token'] = store.getters.accessToken
    }
    return requestConfig
  }, function (error) {
    return Promise.reject(error)
  });

export default http
