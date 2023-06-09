<script lang="ts">
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

<div>
    <textarea bind:value={text} on:change={handleTextChange}></textarea>
    <button on:click={handleSubmit}>Submit</button>
</div>

<style>
    textarea {
        width: 100%;
        height: 100%;
        resize: none;
        overflow: hidden;
    }
</style>