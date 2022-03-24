<template>
  <div class="relative" v-click-outside="closeDropDown">
    <div @click="dropdown = !dropdown">
      <slot name="activator"></slot>
    </div>
    <transition name="dropdown">
      <div v-show="dropdown" class="z-10 absolute top-12 w-content bg-white rounded divide-y divide-gray-100 shadow">
        <slot name="body"></slot>
      </div>
    </transition>
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
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.5s ease;
}
.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-35px);
}
</style>