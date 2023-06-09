<script lang="ts">
    import { eel } from "../main";
    import { activeTab } from "../stores";
    import { fly } from "svelte/transition";

    let text: string = '';
    let isActive: boolean = $activeTab === 'liturgy';

    /**
     * Sets the text to the selected text
     * @param e
     */
    function handleTextChange(e: Event): void {
        text = (e.target as HTMLTextAreaElement).value;
    }

    /**
     * Prints the text
     */
    function handleSubmit(): void {
        eel.print_something(text);
    }
</script>

{#if isActive}
    <div class='grid-item' transition:fly="{{ y: 200, duration: 300 }}">
        <textarea bind:value={text} on:change={handleTextChange}></textarea>
        <button on:click={handleSubmit}>Submit</button>
    </div>
{/if}

<style>
    textarea {
        width: 100%;
        height: 100%;
        resize: none;
        overflow: hidden;
    }
</style>