<template>
  <form class="mt-8 space-y-6" action="#" method="POST">
    <input type="hidden" name="remember" value="true">
    <div class="rounded-md shadow-sm -space-y-px">
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
    </div>

    <div class="flex items-center justify-end text-sm">
      <nav-link :to="{name: 'Registration'}">Забыли свой пароль?</nav-link>
    </div>

    <div>
      <btn type="submit">Войти</btn>
    </div>
  </form>
</template>

<script setup>
import TextField from "../UI/Input/TextField.vue";
import Btn from "../UI/Button/Btn.vue";
import NavLink from "../UI/Link/NavLink.vue";
</script>

<style scoped>

</style>