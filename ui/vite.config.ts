import { svelte } from '@sveltejs/vite-plugin-svelte'
import path from 'path'
import { defineConfig } from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
	build: {
		outDir: '../web',
        emptyOutDir: true,
	},
	plugins: [svelte()],
	resolve: {
		alias: {
			'@components': path.resolve(__dirname, './src/components'),
			'@interfaces': path.resolve(__dirname, './src/interfaces'),
            '@pages': path.resolve(__dirname, './src/pages'),
            '@stores': path.resolve(__dirname, './src/stores')
		}
	}
})
