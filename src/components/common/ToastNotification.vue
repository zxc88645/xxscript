<template>
  <div
    class="pointer-events-auto w-full max-w-sm overflow-hidden rounded-lg bg-white dark:bg-slate-800 shadow-lg ring-1 ring-black ring-opacity-5 transition-all"
    :class="{
      'bg-red-50 dark:bg-red-900/20 ring-red-500/50': type === 'error',
      'bg-green-50 dark:bg-green-900/20 ring-green-500/50': type === 'success',
      'bg-blue-50 dark:bg-blue-900/20 ring-blue-500/50': type === 'info',
      'bg-yellow-50 dark:bg-yellow-900/20 ring-yellow-500/50': type === 'warning',
    }"
  >
    <div class="p-4">
      <div class="flex items-start">
        <div class="flex-shrink-0">
          <!-- Success Icon -->
          <svg
            v-if="type === 'success'"
            class="h-6 w-6 text-green-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <!-- Error Icon -->
          <svg
            v-if="type === 'error'"
            class="h-6 w-6 text-red-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"
            />
          </svg>
          <!-- Info Icon -->
          <svg
            v-if="type === 'info'"
            class="h-6 w-6 text-blue-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z"
            />
          </svg>
          <!-- Warning Icon -->
          <svg
            v-if="type === 'warning'"
            class="h-6 w-6 text-yellow-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.008v.008H12v-.008z"
            />
          </svg>
        </div>
        <div class="ml-3 w-0 flex-1 pt-0.5">
          <p
            class="text-sm font-medium"
            :class="{
              'text-red-800 dark:text-red-200': type === 'error',
              'text-green-800 dark:text-green-200': type === 'success',
              'text-blue-800 dark:text-blue-200': type === 'info',
              'text-yellow-800 dark:text-yellow-200': type === 'warning',
            }"
          >
            {{ message }}
          </p>
        </div>
        <div class="ml-4 flex flex-shrink-0">
          <button
            type="button"
            class="inline-flex rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            @click="$emit('close')"
            :class="{
              'text-red-500 hover:text-red-600 dark:text-red-300': type === 'error',
              'text-green-500 hover:text-green-600 dark:text-green-300': type === 'success',
              'text-blue-500 hover:text-blue-600 dark:text-blue-300': type === 'info',
              'text-yellow-500 hover:text-yellow-600 dark:text-yellow-300': type === 'warning',
            }"
          >
            <span class="sr-only">Close</span>
            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path
                d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  message: string;
  type?: 'success' | 'error' | 'info' | 'warning';
}

withDefaults(defineProps<Props>(), {
  type: 'info',
});

defineEmits<{
  (e: 'close'): void;
}>();
</script>
