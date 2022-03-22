<template>
  <div class="flex items-center w-full max-w-xs p-4 text-gray-800 backdrop-blur-sm bg-white/50 rounded-lg shadow my-2"
       role="alert">
    <div :class="classes">
      <Icon :icon="type"></Icon>
    </div>
    <div class="ml-3 text-sm font-normal">{{ body }}</div>
  </div>
</template>

<script setup>
import Icon from "../Icon.vue";
import {computed} from "vue";

const props = defineProps(['alert']);
const type = props.alert.type;
const body = props.alert.body;


const alertSettings = {
  error: [
    'text-orange-500',
    'bg-orange-100'
  ],
  success: [
    'text-green-500',
    'bg-green-100'
  ]
}

const listClasses = [
  'inline-flex',
  'items-center',
  'justify-center',
  'flex-shrink-0',
  'w-8',
  'h-8',
  'rounded-lg'
];

const classes = computed(() => {
  return listClasses.concat(alertSettings[type]).join(' ');
});
</script>

<style scoped>

</style>