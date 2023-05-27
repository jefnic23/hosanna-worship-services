import './app.css'
import App from './App.svelte'

declare global {
	interface Window {
		eel: any;
		showDirectoryPicker: any;
	}
}

export const eel = window.eel
eel.set_host('ws://localhost:8080')

const app = new App({
	target: document.getElementById('app'),
})

export default app
