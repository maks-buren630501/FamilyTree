<template>
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
        <router-view></router-view>
        <div class="border-4 border-dashed border-gray-200 rounded-lg">
          <btn @click="logout">Logout</btn>
        </div>
      </div>
    </div>
  </main>

</template>

<script setup>
import SideBar from "../../components/UI/SideBar.vue";
import Btn from "../UI/Button/Btn.vue";
import {useStore} from "vuex";
import {computed} from 'vue';

const store = useStore()

const mobileSideBar = computed(() => store.getters.mobileSideBar)

function closeMobileSideBar() {
  store.dispatch('setMobileSideBar', false)
}

function logout() {
  store.dispatch('logout')
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