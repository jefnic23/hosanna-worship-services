<script lang="ts">
    import { eel } from "@stores";
    import { fly } from "svelte/transition";

    let text: string = '';

    let liturgies: string[] = [];
    eel.list_liturgies()((n: string[]) => {
        liturgies = n;
    });

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
    in:fly="{{ x: 1000, duration: 300 }}"
    out:fly="{{ x: -1000, duration: 300 }}"
>
    {#each liturgies as liturgy}
        <p>{liturgy}</p>
    {/each}
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