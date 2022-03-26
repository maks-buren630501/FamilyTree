<template>
  <div>
    <drop-down v-model="dropdown" close-on-click>
      <template v-slot:activator>
        <text-field
            v-model="request"
            @focusin="dropdown = true"
            type="text"
            class="py-2.5 px-10"
            placeholder="Поиск"
        ></text-field>
      </template>
      <template v-slot:body="{ close }">
        <div class="hidden sm:block">
          <div>
            <button @click.stop="switchSettings" class="w-full hover:bg-gray-100">
              <span class="px-2 text-xs text-indigo-400">Настройки поиска</span>
            </button>
            <search-settings v-show="settings"></search-settings>
          </div>
          <div @click.prevent="clearRequest">
            <div v-for="result in searchResults">
              <search-list
                  v-if="result.condition"
                  :items="result.items"
                  :variant="result.variant"
                  :limit="result.limit"
              >
                {{ result.title }}
              </search-list>
            </div>

            <router-link :to="requestLink">
              <btn class="rounded-none">Просмотреть все результаты</btn>
            </router-link>
          </div>
        </div>
      </template>
    </drop-down>
    <router-link :to="requestLink">
      <button @click="clearRequest" type="submit" class="flex absolute inset-y-0 left-2 items-center">
        <icon icon="mdi-magnify" class="text-indigo-500"></icon>
      </button>
    </router-link>
  </div>
</template>

<script setup>
import Icon from "../../Icon.vue";
import DropDown from "../../DropDown.vue";
import TextField from "../../Input/TextField.vue";
import SearchSettings from "./SearchSettings.vue";
import SearchList from "./SearchList.vue";
import Btn from "../../Button/Btn.vue";
import {ref, computed} from "vue";
import {useStore} from "vuex";

const store = useStore()

const requestLink = {name: 'Search', params: {variant: 'all'}}
const searchRequest = ref('')
const request = computed({
  get() {
    return searchRequest.value
  },
  set(value) {
    store.dispatch('setSearchRequest', value)
    searchRequest.value = value
  }
})
function clearRequest() {
  searchRequest.value = ''
  closeDropdown()
}

const dropdown = ref(false)
function closeDropdown() {
  dropdown.value = false
}

const settings = ref(false)
function switchSettings() {
  settings.value = !settings.value
}

const searchResults = computed(() => [
  {
    items: [],
    variant: 'graph',
    limit: 2,
    title: 'Объекты на графе',
    condition: store.getters.searchGraph
  },
  {
    items: store.getters.selfPeople,
    variant: 'self',
    limit: 2,
    title: 'Ваши объекты',
    condition: store.getters.searchSelf
  },
  {
    items: store.getters.globalPeople,
    variant: 'global',
    limit: 2,
    title: 'Объекты глобального поиска',
    condition: store.getters.searchGlobal
  },
])
</script>

<style scoped>

</style>