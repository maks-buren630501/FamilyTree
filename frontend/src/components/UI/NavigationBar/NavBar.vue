<template>
  <nav class="flex flex-nowrap justify-between items-center h-16 bg-indigo-800 px-3 sm:px-6 py-2.5">
    <button class="block sm:hidden" @click="mobileSideBar = !mobileSideBar">
      <icon class="text-white" icon="mdi-menu"></icon>
    </button>
    <router-link :to="{name: 'Tree'}" class="hidden sm:flex items-center">
      <img src="src/assets/logo.png" class="mr-3 h-6" alt="FamilyTree Logo"/>
      <span class="text-xl font-semibold whitespace-nowrap text-white flex">FamilyTree</span>
    </router-link>
    <global-search @submit.prevent="" class="grow relative mx-8 sm:mx-16 md:mx-24 lg:mx-48 xl:mx-64 2xl:mx-96"></global-search>
    <control-menu class="flex items-center"></control-menu>
  </nav>
</template>

<script setup>
import Icon from "../Icon.vue";
import ControlMenu from "./ControlMenu.vue";
import GlobalSearch from "./GlobalSearch/GlobalSearch.vue";

import {computed} from 'vue'

const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue'])

const mobileSideBar = computed({
  get() {
    return props.modelValue
  },
  set(value) {
    emit('update:modelValue', value)
  }
})
</script>

<style scoped>

</style>