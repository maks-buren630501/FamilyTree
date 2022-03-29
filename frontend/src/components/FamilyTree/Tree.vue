<template>
  <main class="flex h-main">
    <aside class="hidden sm:block">
      <side-bar></side-bar>
    </aside>
    <transition name="sidebar">
      <aside
          v-if="mobileSideBar"
          v-click-outside="closeMobileSideBar"
          class="sm:hidden block absolute bg-white h-main z-10"
      >
        <side-bar></side-bar>
      </aside>
    </transition>
    <div class="h-full w-full">
      <router-view></router-view>
      <v-network-graph
          class="!static"
          :nodes="nodes"
          :edges="edges"
          :layouts="layouts"
      />
    </div>
  </main>

</template>

<script setup>
import SideBar from "../../components/UI/SideBar.vue";
import {useStore} from "vuex";
import {computed} from 'vue';

const store = useStore()

const mobileSideBar = computed(() => store.getters.mobileSideBar)

function closeMobileSideBar() {
  store.dispatch('setMobileSideBar', false)
}

const nodes = {
  node1: {name: "Node 1"},
  node2: {name: "Node 2"},
  node3: {name: "Node 3"},
  node4: {name: "Node 4"},
}
const edges = {
  edge1: {source: "node1", target: "node2"},
  edge2: {source: "node2", target: "node3"},
  edge3: {source: "node3", target: "node4"},
}
const layouts = {
  nodes: {
    node1: {x: 0, y: 0},
    node2: {x: 200, y: 200},
    node3: {x: 400, y: 0},
    node4: {x: 600, y: 200},
  },
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

.asdasd {
  position: static!important;
}
</style>