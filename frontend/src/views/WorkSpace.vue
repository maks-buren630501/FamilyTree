<template>
  <header class="h-15 drop-shadow-md">
    <nav-bar v-model="mobileSideBar"></nav-bar>
  </header>

  <main class="flex h-main">
    <aside class="hidden sm:block">
      <side-bar></side-bar>
    </aside>
    <transition name="sidebar">
      <aside
        v-if="mobileSideBar"
        v-click-outside="closeMobileSideBar"
        class="sm:hidden block absolute bg-white h-main"
      >
        <side-bar></side-bar>
      </aside>
    </transition>
    <div class="h-full max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="border-4 border-dashed border-gray-200 rounded-lg">Test content</div>
      </div>
    </div>
  </main>
</template>

<script setup>
import NavBar from "../components/UI/NavigationBar/NavBar.vue";
import SideBar from "../components/UI/SideBar.vue";
import {ref} from "vue";

const mobileSideBar = ref(false);

function closeMobileSideBar() {
  mobileSideBar.value = false
}
</script>

<style scoped>
.sidebar-enter-active,
.sidebar-leave-active {
  transition: all 0.5s ease;
}
.sidebar-enter-from,
.sidebar-leave-to {
  opacity: 0;
  transform: translateX(-35px);
}
</style>