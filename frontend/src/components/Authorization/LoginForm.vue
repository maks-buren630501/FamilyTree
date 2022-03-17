<template>
  <form class="mt-8 space-y-6" @submit.prevent="confirmLogin">
    <div v-if="msgError" class="flex justify-center bg-red-500 px-8 py-2 text-white">
      {{msgError}}
    </div>
    <input type="hidden" name="remember" value="true">
    <div class="rounded-md shadow-sm -space-y-px">
      <text-field
        v-model="username"
        id="email-address"
        name="username"
        type="username"
        autocomplete="username"
        placeholder="Username"
        required
      ></text-field>
      <text-field
        v-model="password"
        id="password"
        name="password"
        type="password"
        autocomplete="current-password"
        placeholder="Пароль"
        required
      ></text-field>
    </div>

    <div class="flex items-center justify-end text-sm">
      <nav-link :to="{name: 'Registration'}">Забыли свой пароль?</nav-link>
    </div>

    <btn type="submit">Войти</btn>
  </form>
</template>

<script setup>
import TextField from "../UI/Input/TextField.vue";
import Btn from "../UI/Button/Btn.vue";
import NavLink from "../UI/Link/NavLink.vue";
import {useRouter} from 'vue-router';
import {useStore} from 'vuex';
import {ref} from "vue";

const router = useRouter()
const store = useStore()

const username = ref("")
const password = ref("")

const msgError = ref(null)

function confirmLogin() {
  store.dispatch('login', {
      username: username.value,
      password: password.value
    })
  .then(() => router.push({name: 'Tree'}))
  .catch(e => {
    if(e.toJSON().status === 403) {
      msgError.value = 'Проверьте введенные данные'
    } else {
      msgError.value = e
    }
  })
}
</script>

<style scoped>

</style>