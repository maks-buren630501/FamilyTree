<template>
  <drop-down v-model="dropdown" close-on-click>
    <template v-slot:activator>
      <button @click="switchDropdown" type="button" class="flex items-center text-sm text-white" aria-expanded="false">
        <span class="hidden sm:flex">Ivanov Ivan Ivanovich</span>
        <img class="w-8 h-8 ml-3 rounded-full" src="http://127.0.0.1:3000/src/assets/profile.jpg" alt="user photo">
      </button>
    </template>
    <template v-slot:body>
      <list @click="closeDropdown">
        <list-item>
          <list-item-icon>
            <icon icon="mdi-message-outline"></icon>
          </list-item-icon>
          <list-item-content class="hidden sm:flex">
            <list-item-content-title>Чат</list-item-content-title>
            <list-item-content-subtitle>Ваши переписки</list-item-content-subtitle>
          </list-item-content>
        </list-item>
        <list-item>
          <list-item-icon>
            <icon icon="mdi-account-cog-outline"></icon>
          </list-item-icon>
          <list-item-content class="hidden sm:flex">
            <list-item-content-title>Настройки</list-item-content-title>
            <list-item-content-subtitle>Настройки вашего профиля</list-item-content-subtitle>
          </list-item-content>
        </list-item>
        <list-item>
          <list-item-icon>
            <icon icon="mdi-logout"></icon>
          </list-item-icon>
          <list-item-content class="hidden sm:flex">
            <list-item-content-title>Выход</list-item-content-title>
            <list-item-content-subtitle>Выход из системы</list-item-content-subtitle>
          </list-item-content>
        </list-item>
      </list>
    </template>
  </drop-down>
</template>

<script setup>
import Icon from "../Icon.vue";
import DropDown from "../DropDown.vue";
import List from "../ListItems/List.vue";
import ListItem from "../ListItems/ListItem.vue";
import ListItemIcon from "../ListItems/ListItemIcon.vue";
import ListItemContent from "../ListItems/ListItemContent.vue";
import ListItemContentTitle from "../ListItems/ListItemContentTitle.vue";
import ListItemContentSubtitle from "../ListItems/ListItemContentSubtitle.vue";
import {ref} from 'vue'

const dropdown = ref(false)
function switchDropdown() {
  dropdown.value = !dropdown.value
}
function closeDropdown() {
  dropdown.value = false
}
</script>

<style scoped>

</style>