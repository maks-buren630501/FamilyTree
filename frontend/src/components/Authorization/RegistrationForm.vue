<template>
  <form class="mt-8 space-y-6" @submit.prevent="confirmRegistration">
    <div v-if="msgError" class="flex justify-center bg-red-500 px-8 py-2 text-white">
      {{msgError}}
    </div>
    <input type="hidden" name="remember" value="true">
    <div class="rounded-md shadow-sm -space-y-px">
      <text-field
        v-model="username"
        id="username"
        name="username"
        type="text"
        autocomplete="username"
        placeholder="Логин пользователя"
        required
      ></text-field>
      <text-field
        v-model="email"
        id="email-address"
        name="email"
        type="email"
        autocomplete="email"
        placeholder="Email"
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
      <text-field
        v-model="confirmPassword"
        id="confirm-password"
        name="confirm-password"
        type="password"
        autocomplete="confirm-password"
        placeholder="Подтвердите пароль"
        required
      ></text-field>
    </div>

    <btn type="submit">Зарегестрироваться</btn>
  </form>
</template>

<script setup>
import TextField from "../UI/Input/TextField.vue";
import Btn from "../UI/Button/Btn.vue";
import {useRouter} from 'vue-router';
import {useStore} from 'vuex';
import {ref} from "vue";

const router = useRouter()
const store = useStore()

const username = ref("")
const email = ref("")
const password = ref("")
const confirmPassword = ref("")

const msgError = ref(null)

function confirmRegistration() {
  if(password.value === confirmPassword.value) {
    store.dispatch('registration', {
      username: username.value,
      email: email.value,
      password: password.value
    })
    .then(() => router.push({name: 'RegistrationConfirm'}))
    .catch(e => {
      if(e.toJSON().status === 409) {
        msgError.value = 'Данный email уже используется'
      } else {
        msgError.value = e
      }
    })
  } else {
    msgError.value = 'Пароли должны совпадать'
  }
}
</script>

<style scoped>

</style>