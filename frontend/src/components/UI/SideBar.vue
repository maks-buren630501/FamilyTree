<template>
  <div class="h-full overflow-y-auto border">
    <list>
      <list-item v-for="i in 19" class="border-y my-1">
        <list-item-content class="whitespace-nowrap">
          <list-item-content-title>
            Ivanov Ivan Ivanovich
          </list-item-content-title>
          <list-item-content-subtitle>
            27.12.1988 - 20.11.2020
          </list-item-content-subtitle>
        </list-item-content>
        <list-item-action>
          <input type="checkbox" class="w-5 h-5">
        </list-item-action>
      </list-item>
    </list>
  </div>
</template>

<script setup>
import List from "./ListItems/List.vue";
import ListItem from "./ListItems/ListItem.vue";
import ListItemContent from "./ListItems/ListItemContent.vue";
import ListItemContentTitle from "./ListItems/ListItemContentTitle.vue";
import ListItemContentSubtitle from "./ListItems/ListItemContentSubtitle.vue";
import ListItemAction from "./ListItems/ListItemAction.vue";
</script>

<style scoped>

</style>