<template>
  <nav class="bg-indigo-800 px-3 sm:px-6 py-2.5 drop-shadow-md">
    <div class="flex flex-nowrap justify-between items-center">
      <router-link :to="{name: 'Tree'}" class="flex items-center">
        <img src="src/assets/logo.png" class="mr-3 h-6" alt="FamilyTree Logo"/>
        <span class="text-xl font-semibold whitespace-nowrap text-white hidden sm:flex">FamilyTree</span>
      </router-link>
      <form @submit.prevent="" class="relative w-1/3">
        <button type="submit" class="flex absolute inset-y-0 left-2 items-center">
          <icon icon="mdi-magnify" class="text-indigo-500"></icon>
        </button>
        <text-field type="text" class="py-2.5 px-10 peer" placeholder="Поиск людей на графе"></text-field>
        <button class="flex absolute inset-y-0 right-2 items-center">
          <icon icon="mdi-tune" class="text-indigo-500"></icon>
        </button>
      </form>
      <drop-down class="flex items-center">
        <template v-slot:activator>
          <button type="button" class="flex items-center text-sm text-white" aria-expanded="false">
            <span class="hidden sm:flex">Стасюк Кирилл Андреевич</span>
            <img class="w-8 h-8 ml-3 rounded-full" src="src/assets/profile.jpg" alt="user photo">
          </button>
        </template>
        <template v-slot:body>
          <list>
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
    </div>
  </nav>
</template>

<script setup>
import Icon from "../Icon.vue";
import DropDown from "../DropDown.vue";
import List from "../ListItems/List.vue";
import TextField from "../Input/TextField.vue";
import ListItem from "../ListItems/ListItem.vue";
import ListItemIcon from "../ListItems/ListItemIcon.vue";
import ListItemContent from "../ListItems/ListItemContent.vue";
import ListItemContentTitle from "../ListItems/ListItemContentTitle.vue";
import ListItemContentSubtitle from "../ListItems/ListItemContentSubtitle.vue";
</script>

<style scoped>

</style>