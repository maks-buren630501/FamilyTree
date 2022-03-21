<template>
  <btn @click="logout">Logout</btn>
</template>

<script setup>
import Btn from "../UI/Button/Btn.vue";
import {useStore} from "vuex";

const store = useStore()

function logout() {
  store.dispatch('logout')
}
</script>

<style scoped>

</style>