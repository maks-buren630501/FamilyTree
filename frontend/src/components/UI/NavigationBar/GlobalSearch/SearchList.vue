<template>
  <list class="border-b">
    <span class="px-2 text-xs text-gray-400">
      <slot></slot>
    </span>
    <list-item v-for="i in 2">
      <list-item-icon class="hidden md:block">
        <img class="w-8 h-8 ml-3 rounded-full" src="../../../../assets/profile.jpg" alt="user photo">
      </list-item-icon>
      <list-item-content>
        <list-item-content-title>Ivanov Ivan Ivanovich</list-item-content-title>
        <list-item-content-subtitle>20.12.1998-25.03.2022</list-item-content-subtitle>
      </list-item-content>
    </list-item>
  </list>
</template>

<script setup>
import List from "../../ListItems/List.vue";
import ListItem from "../../ListItems/ListItem.vue";
import ListItemIcon from "../../ListItems/ListItemIcon.vue";
import ListItemContent from "../../ListItems/ListItemContent.vue";
import ListItemContentTitle from "../../ListItems/ListItemContentTitle.vue";
import ListItemContentSubtitle from "../../ListItems/ListItemContentSubtitle.vue";
</script>

<style scoped>

</style>