<template>
  <input :class="classes">
</template>

<script setup>
import {reactive, computed} from 'vue'

const listClasses = reactive([
    'appearance-none',
    'rounded-none',
    'relative',
    'block',
    'w-full',
    'px-3',
    'py-2',
    'border',
    'border-gray-300',
    'placeholder-gray-500',
    'text-gray-900',
    'focus:outline-none',
    'focus:ring-indigo-500',
    'focus:border-indigo-500',
    'focus:z-10',
    'sm:text-sm'
]);

const classes = computed(() => {
  return listClasses.join(' ');
});
</script>

<style scoped>

</style>