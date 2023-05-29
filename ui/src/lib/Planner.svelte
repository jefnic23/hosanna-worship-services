<script lang="ts">
    const elements: {} = {
        'confession': 'call_and_response',
        'gathering_song': 'hymn',
        'greeting': 'call_and_response',
        'kyrie': 'congregation',
        'prayer_of_the_day': 'call_and_response',
        'first_reading': 'reading',
        'psalm': 'psalm',
        'second_reading': 'reading',
        'gospel_acclamation': 'congregation',
        'gospel': 'gospel',
        'sermon': 'title',
        'hym_of_the_day': 'hymn',
        'creed': 'congregation',
        'prayers_of_intercession': 'intercessions',
        'dialogue': 'call_and_response',
        'holy_holy_holy': 'congregation',
        'thanksgiving': 'call_and_response',
        'lords_prayer': 'congregation',
        'communion': 'title',
        'communion_song': 'congregation',
        'communion_blessing': 'call_and_response',
        'prayer_after_communion': 'call_and_response',
        'blessing': 'call_and_response',
        'sending_song': 'hymn',
        'dismissal': 'call_and_response'
    }
</script>

{#each Object.keys(elements) as element}
    <div class="planner-element">
        <div class="planner-element-name">{element}</div>
        <div class="planner-element-type">{elements[element]}</div>
    </div>
{/each}