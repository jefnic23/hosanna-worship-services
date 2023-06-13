import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import path from 'path'

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
			'@stores': path.resolve(__dirname, './src/stores'),
			'@interfaces': path.resolve(__dirname, './src/interfaces'),
		}
	}
})
