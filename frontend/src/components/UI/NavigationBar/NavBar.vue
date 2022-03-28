<template>
  <nav class="flex flex-nowrap justify-between items-center h-16 bg-indigo-800 px-3 sm:px-6 py-2.5">
    <button class="block sm:hidden" @click="switchMobileSidebar">
      <icon class="text-white" icon="mdi-menu"></icon>
    </button>
    <router-link :to="{name: 'Tree'}" class="hidden sm:flex items-center">
      <img src="http://127.0.0.1:3000/src/assets/logo.png" class="mr-3 h-6" alt="FamilyTree Logo"/>
      <span class="text-xl font-semibold whitespace-nowrap text-white flex">FamilyTree</span>
    </router-link>
    <search class="grow relative mx-8 sm:mx-16 md:mx-24 lg:mx-48 xl:mx-64 2xl:mx-96"></search>
    <control-menu class="flex items-center"></control-menu>
  </nav>
</template>

<script setup>
import Icon from "../Icon.vue";
import ControlMenu from "./Control/ControlMenu.vue";
import Search from "./GlobalSearch/Search.vue";
import {computed} from 'vue'
import {useStore} from "vuex";


const store = useStore()

const mobileSideBar = computed({
  get() {
    return store.getters.mobileSideBar
  },
  set(value) {
    store.dispatch('setMobileSideBar', value)
  }
})
function switchMobileSidebar() {
  mobileSideBar.value = !mobileSideBar.value
}
</script>

<style scoped>

</style>