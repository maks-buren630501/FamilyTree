<template>
  <list>
    <search-settings-item icon="mdi-graph" name="Поиск по графу"></search-settings-item>
    <search-settings-item icon="mdi-database-search-outline" name="Поиск по вашим объектам"></search-settings-item>
    <search-settings-item icon="mdi-account-search-outline" name="Глобальный поиск"></search-settings-item>
  </list>
</template>

<script setup>
import List from "../../ListItems/List.vue";
import SearchSettingsItem from "./SearchSettingsItem.vue";
</script>

<style scoped>

</style>