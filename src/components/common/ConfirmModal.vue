<template>
  <Transition
    enter-active-class="ease-out duration-300"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="ease-in duration-200"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div
      v-if="isVisible"
      class="fixed inset-0 bg-black/50 backdrop-blur-sm z-[60] transition-opacity"
      @click="handleCancel"
    ></div>
  </Transition>

  <Transition
    enter-active-class="ease-out duration-300"
    enter-from-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
    enter-to-class="opacity-100 translate-y-0 sm:scale-100"
    leave-active-class="ease-in duration-200"
    leave-from-class="opacity-100 translate-y-0 sm:scale-100"
    leave-to-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
  >
    <div v-if="isVisible" class="fixed inset-0 z-[60] overflow-y-auto">
      <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
        <div
          class="relative transform overflow-hidden rounded-2xl bg-white dark:bg-slate-800 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg border border-white/10"
          @click.stop
        >
          <div class="bg-white dark:bg-slate-800 px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div
                class="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10"
                :class="{
                  'bg-red-100 dark:bg-red-900/20': options.type === 'danger',
                  'bg-yellow-100 dark:bg-yellow-900/20': options.type === 'warning',
                  'bg-blue-100 dark:bg-blue-900/20': options.type === 'info',
                }"
              >
                <!-- Danger Icon -->
                <svg
                  v-if="options.type === 'danger'"
                  class="h-6 w-6 text-red-600 dark:text-red-400"
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
                <!-- Info Icon -->
                <svg
                  v-else
                  class="h-6 w-6 text-blue-600 dark:text-blue-400"
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
              </div>
              <div class="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                <h3
                  class="text-base font-semibold leading-6 text-gray-900 dark:text-white"
                  id="modal-title"
                >
                  {{ options.title }}
                </h3>
                <div class="mt-2">
                  <p class="text-sm text-gray-500 dark:text-gray-300">
                    {{ options.message }}
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div
            class="bg-gray-50 dark:bg-slate-700/50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6"
          >
            <button
              type="button"
              class="inline-flex w-full justify-center rounded-lg px-3 py-2 text-sm font-semibold text-white shadow-sm sm:ml-3 sm:w-auto transition-colors"
              :class="{
                'bg-red-600 hover:bg-red-500': options.type === 'danger',
                'bg-blue-600 hover:bg-blue-500':
                  options.type === 'info' || options.type === 'warning',
              }"
              @click="handleConfirm"
            >
              {{ options.confirmText }}
            </button>
            <button
              type="button"
              class="mt-3 inline-flex w-full justify-center rounded-lg bg-white dark:bg-slate-600 px-3 py-2 text-sm font-semibold text-gray-900 dark:text-gray-200 shadow-sm ring-1 ring-inset ring-gray-300 dark:ring-gray-500 hover:bg-gray-50 dark:hover:bg-slate-500 sm:mt-0 sm:w-auto transition-colors"
              @click="handleCancel"
            >
              {{ options.cancelText }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { useConfirm } from '../../composables/useConfirm';

const { isVisible, options, handleConfirm, handleCancel } = useConfirm();
</script>
