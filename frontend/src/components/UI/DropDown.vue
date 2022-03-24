<template>
  <div class="relative" v-click-outside="closeDropDown">
    <div @click="dropdown = !dropdown">
      <slot name="activator"></slot>
    </div>
    <div v-show="dropdown" class="z-10 absolute top-12 w-content bg-white rounded divide-y divide-gray-100 shadow">
      <slot name="body"></slot>
    </div>
  </div>
</template>

<script setup>
import {ref} from "vue";

const dropdown = ref(false)

function closeDropDown() {
  dropdown.value = false
}
</script>

<style scoped>

</style>