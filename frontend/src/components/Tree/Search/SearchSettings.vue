<template>
  <list>
    <search-settings-item
      v-for="setting in settings"
      v-model="setting.state"
      :name="setting.description"
      :icon="setting.icon"
    ></search-settings-item>
  </list>
</template>

<script setup>
import List from "../../UI/ListItems/List.vue";
import SearchSettingsItem from "./SearchSettingsItem.vue";
import {computed, reactive} from "vue";
import {useStore} from "vuex";

const store = useStore()

const graph = computed({
  get() {
    return store.getters.searchGraph
  },
  set(state) {
    store.dispatch('setSearchGraph', state)
  }
});

const self = computed({
  get() {
    return store.getters.searchSelf
  },
  set(state) {
    store.dispatch('setSearchSelf', state)
  }
});

const global = computed({
  get() {
    return store.getters.searchGlobal
  },
  set(state) {
    store.dispatch('setSearchGlobal', state)
  }
});

const settings = reactive([
  {
    description: 'Поиск по графу',
    icon: 'mdi-graph',
    state: graph
  },
  {
    description: 'Поиск по вашим объектам',
    icon: 'mdi-database-search-outline',
    state: self
  },
  {
    description: 'Глобальный поиск',
    icon: 'mdi-account-search-outline',
    state: global
  }
])
</script>

<style scoped>

</style>