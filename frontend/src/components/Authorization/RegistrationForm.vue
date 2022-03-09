<template>
  <form class="mt-8 space-y-6" action="#" method="POST">
    <input type="hidden" name="remember" value="true">
    <div class="rounded-md shadow-sm -space-y-px">
      <text-field
        id="username"
        name="username"
        type="text"
        autocomplete="username"
        placeholder="Имя пользователя"
        required
      ></text-field>
      <text-field
        id="email-address"
        name="email"
        type="email"
        autocomplete="email"
        placeholder="Email"
        required
      ></text-field>
      <text-field
        id="password"
        name="password"
        type="password"
        autocomplete="current-password"
        placeholder="Пароль"
        required
      ></text-field>
      <text-field
        id="confirm-password"
        name="confirm-password"
        type="password"
        autocomplete="confirm-password"
        placeholder="Подтвердите пароль"
        required
      ></text-field>
    </div>

    <div>
      <btn type="submit">Зарегестрироваться</btn>
    </div>
  </form>
</template>

<script setup>
import TextField from "../UI/Input/TextField.vue";
import Btn from "../UI/Button/Btn.vue";
</script>

<style scoped>

</style>