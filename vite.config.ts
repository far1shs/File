import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite';
import {PrimeVueResolver} from '@primevue/auto-import-resolver';

export default defineConfig({
    server: {
        hmr: true
    },
    plugins: [
        vue(),
        Components({
            resolvers: [
                PrimeVueResolver()
            ]
        })
    ],
})
