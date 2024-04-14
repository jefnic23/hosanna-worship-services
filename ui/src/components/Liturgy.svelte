<script lang="ts">
    import { onMount } from "svelte";
    import { eel } from "@stores";
    import TextEditor from "@components/TextEditor.svelte";

    let season: string;
    let liturgy_file: string;

    let liturgies: string[] = [];
    onMount(async () => {
        await eel.list_liturgies()((n: string[]) => {
            liturgies = n;
        });
    });

    let files: string[] = [];
    async function list_liturgical_files(season: string): Promise<void> {
        await eel.list_liturgical_files(season)((n: string[]) => {
            files = n;
        });
    }

    let text: string;
    async function get_liturgical_file(filename: string): Promise<void> {
        await eel.get_liturgical_file(filename)((n: string) => {
            text = n;
        });
    }
</script>

<select bind:value={season} on:change={() => list_liturgical_files(season)}>
    {#each liturgies as liturgy (liturgy)}
        <option value={liturgy}>
            {liturgy}
        </option>
    {/each}
</select>
<select bind:value={liturgy_file} on:change={() => get_liturgical_file(liturgy_file) }>
    {#each files as file (file)}
        <option value={file}>
            {file}
        </option>
    {/each}
</select>
<TextEditor text={text} />
