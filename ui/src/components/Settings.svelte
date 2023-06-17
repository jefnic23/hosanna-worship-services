<script lang="ts">
    import type { Settings } from "@interfaces/settings";
    import { eel } from "@stores";
    import { fly } from "svelte/transition";

    let settings: Settings = {};

    eel.get_settings()((s: Settings) => {
        settings = s;
    });

    const handleChange = (e: Event) => {
        settings[(e.target as HTMLInputElement).name] = (e.target as HTMLInputElement).value;
    }

    const getDir = async () => {
        let dir = await eel.get_dir()();
        settings.LOCAL_DIR = dir;
    }
</script>

<div 
    class="container-item" 
    in:fly="{{ x: -500, duration: 300 }}"
    out:fly="{{ x: 500, duration: 300 }}"
>
    {#each Object.keys(settings) as setting}
        {@const input_type = setting === "LOCAL_DIR" ? "button" : "text"}
        <span>
            <p>{setting}:</p>
            {#if input_type === "button"}
                <button on:click={getDir}>Choose Directory</button>
            {:else}
                <input type={input_type} name={setting} value={settings[setting]} on:change={handleChange} />
            {/if}
        </span>
    {/each}
    <button on:click={() => eel.update_settings(settings)}>Save</button>
</div>