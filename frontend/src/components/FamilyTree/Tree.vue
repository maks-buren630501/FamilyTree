<template>
  <div class="px-4 py-6 sm:px-0">
    <router-view></router-view>
    <div class="border-4 border-dashed border-gray-200 rounded-lg">
      <btn @click="logout">Logout</btn>
    </div>
  </div>
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