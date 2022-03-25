<template>
  <div class="relative" v-click-outside="closeDropDown">
    <slot name="activator" :change="changeDropDown" :open="openDropDown" :close="closeDropDown"></slot>
    <transition name="dropdown">
      <div v-show="dropdown" class="z-10 overflow-y-auto max-h-screen-2/3 absolute top-12 bg-white min-w-full divide-y divide-gray-100 shadow">
        <slot name="body"></slot>
      </div>
    </transition>
  </div>
</template>

<script setup>
import {ref} from "vue";

const dropdown = ref(false)

function changeDropDown() {
  dropdown.value = !dropdown.value
}

function openDropDown() {
  dropdown.value = true
}

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