<script lang="ts">
    import { eel } from "@stores";
    import TextEditor from "@components/TextEditor.svelte";

    let season: string;
    let liturgy_file: string;

    let liturgies: string[] = [];
    eel.list_liturgies()((n: string[]) => {
        liturgies = n;
    });

    let files: string[] = [];
    function list_liturgical_files(season: string): void {
        eel.list_liturgical_files(season)((n: string[]) => {
            files = n;
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
<select bind:value={liturgy_file}>
    {#each files as file (file)}
        <option value={file}>
            {file}
        </option>
    {/each}
</select>
<TextEditor />
