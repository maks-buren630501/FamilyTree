<template>
  <list-item>
    <list-item-icon>
      <icon class="text-xs" :icon="props.icon"></icon>
    </list-item-icon>
    <list-item-content>
      <list-item-content-subtitle class="text-xs text-left">{{props.name}}</list-item-content-subtitle>
    </list-item-content>
    <list-item-action>
      <input type="checkbox">
    </list-item-action>
  </list-item>
</template>

<script setup>
import Icon from "../../Icon.vue";
import ListItem from "../../ListItems/ListItem.vue";
import ListItemIcon from "../../ListItems/ListItemIcon.vue";
import ListItemContent from "../../ListItems/ListItemContent.vue";
import ListItemContentSubtitle from "../../ListItems/ListItemContentSubtitle.vue";
import ListItemAction from "../../ListItems/ListItemAction.vue";
const props = defineProps(['name', 'icon'])
</script>

<style scoped>

</style>