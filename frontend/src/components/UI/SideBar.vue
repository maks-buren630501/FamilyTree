<template>
  <transition name="sidebar">
    <aside v-show="mobileSideBar" class="sm:!block absolute sm:sticky bg-white sm:h-full h-main z-10">
      <slot></slot>
    </aside>
  </transition>
</template>

<script setup>
import {computed} from "vue";
import {useStore} from "vuex";

const store = useStore()
const mobileSideBar = computed(() => store.getters.mobileSideBar)
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