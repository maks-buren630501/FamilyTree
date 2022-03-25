<template>
  <form>
    <drop-down>
      <template v-slot:activator="{ open }">
        <text-field @focus="open" type="text" class="py-2.5 px-10" placeholder="Поиск людей на графе"></text-field>
      </template>
      <template v-slot:body>
        <button @click="settings = !settings" class="w-full hover:bg-gray-100">
          <span class="px-2 text-xs text-indigo-400">Настройки поиска</span>
        </button>
        <search-settings v-show="settings"></search-settings>
        <search-list>Объекты на графе</search-list>
        <search-list>Ваши объекты</search-list>
        <search-list>Объекты глобального поиска</search-list>
        <btn class="rounded-none">Просмотреть все результаты</btn>
      </template>
    </drop-down>
    <button type="submit" class="flex absolute inset-y-0 left-2 items-center">
      <icon icon="mdi-magnify" class="text-indigo-500"></icon>
    </button>
  </form>
</template>

<script setup>
import Icon from "../../Icon.vue";
import DropDown from "../../DropDown.vue";
import TextField from "../../Input/TextField.vue";
import SearchSettings from "./SearchSettings.vue";
import SearchList from "./SearchList.vue";
import Btn from "../../Button/Btn.vue";
import {ref} from "vue";

const settings = ref(false)
</script>

<style scoped>

</style>