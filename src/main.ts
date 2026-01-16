import './styles/style.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { install as VueMonacoEditorPlugin } from '@guolao/vue-monaco-editor';

import App from './App.vue';
import router from './router';

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(VueMonacoEditorPlugin);

app.mount('#app');
