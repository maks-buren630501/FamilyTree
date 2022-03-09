<template>
  <div class="min-h-full flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <img class="mx-auto h-24 w-auto" src="../assets/logo.png" alt="Workflow">
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">{{route.meta.title}}</h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Или
          <nav-link :to="{name: route.meta.link}">{{route.meta.textLink}}</nav-link>
        </p>
      </div>
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import {useRoute} from 'vue-router';
import NavLink from "../components/UI/Link/NavLink.vue";

const route = useRoute()
</script>

<style>

</style>
