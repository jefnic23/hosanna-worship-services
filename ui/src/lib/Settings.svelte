<script lang="ts">
    import { eel } from "../main";

    let settings: object = {};

    eel.get_settings()((s: object) => {
        settings = s;
    });
</script>

{#each Object.keys(settings) as setting}
    <p>{setting}: {settings[setting]}</p>
{/each}