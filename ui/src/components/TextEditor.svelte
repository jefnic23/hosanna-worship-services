<script lang="ts">
    import { fly } from "svelte/transition";
    import { eel } from "../main";

    let text: string = '';

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

<div 
    class='container-item'
    in:fly="{{ x: -1000, duration: 300 }}"
    out:fly="{{ x: 1000, duration: 300 }}"
>
    <div class='flex'>
        <textarea bind:value={text} on:change={handleTextChange}></textarea>
        <button on:click={handleSubmit}>Submit</button>
    </div>
</div>

<style>
    .flex {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
</style>