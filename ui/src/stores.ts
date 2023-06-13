import type { Writable } from 'svelte/store';
import { writable } from 'svelte/store';

export const activeTab: Writable<string> = writable('date');
export const pptElements: Writable<string[]> = writable([]);
