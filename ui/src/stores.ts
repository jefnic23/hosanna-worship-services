import type { Writable } from 'svelte/store';
import { writable } from 'svelte/store';

export const activeTab: Writable<string> = writable('date');
export const pptElements: Writable<string[]> = writable([]);
export const serviceDay: Writable<Date> = writable(new Date());

declare global {
	interface Window {
		eel: any;
		showDirectoryPicker: any;
	}
}

export const eel = window.eel
eel.set_host('ws://localhost:8080')
