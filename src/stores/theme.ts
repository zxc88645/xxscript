import { defineStore } from 'pinia';
import { ref, watch } from 'vue';

export const useThemeStore = defineStore('theme', () => {
  const isDarkMode = ref(localStorage.getItem('theme') === 'dark');

  const toggleTheme = () => {
    isDarkMode.value = !isDarkMode.value;
  };

  watch(
    isDarkMode,
    (val) => {
      if (val) {
        document.documentElement.classList.add('dark');
        localStorage.setItem('theme', 'dark');
      } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
      }
    },
    { immediate: true },
  );

  return {
    isDarkMode,
    toggleTheme,
  };
});
