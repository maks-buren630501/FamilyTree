<template>
  <form class="mt-8 space-y-6" @submit.prevent="confirmChangePassword">
    <input type="hidden" name="remember" value="true">
    <div class="rounded-md shadow-sm -space-y-px">
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

    <btn type="submit">Изменить</btn>
  </form>
</template>

<script setup>
import TextField from "../UI/Input/TextField.vue";
import Btn from "../UI/Button/Btn.vue";
import {useStore} from "vuex";
import {ref} from "vue";

const store = useStore()

const password = ref("")
const confirmPassword = ref("")

function confirmChangePassword() {
  if(password.value === confirmPassword.value) {
    console.log('confirmChangePassword')
  }
}
</script>

<style scoped>

</style>