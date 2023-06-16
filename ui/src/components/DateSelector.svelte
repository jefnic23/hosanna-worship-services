<script lang="ts">
    import { activeTab, eel, serviceDay } from "@stores";
    import { fly } from "svelte/transition";

    let formattedDate: string = formatDate($serviceDay);

    /**
     * Formats the date to the format YYYY-MM-DD.
     * @param date
     */
    function formatDate(date: Date): string {
        let year = date.toLocaleString('default', { year: 'numeric' });
        let month = date.toLocaleString('default', { month: '2-digit' });
        let day = date.toLocaleString('default', { day: '2-digit' });
        return `${year}-${month}-${day}`;
    }

    /**
     * Sets the date to the sunday following the current date.
     * @param day
     */
    function getNextSunday(day: Date): Date {
        day.setDate(day.getDate() + ((0 - day.getDay()) % 7) + 7);
        return day;
    }

    /**
     * Sets the date to the selected date.
     * @param e
     */
    function handleDateChange(e: Event): void {
        let dateParts: string[] = (e.target as HTMLInputElement).value.split('-');
        let newDay = new Date(parseInt(dateParts[0]), parseInt(dateParts[1]) - 1, parseInt(dateParts[2]));
        serviceDay.set(newDay);
        formattedDate = formatDate(newDay);
    }

    /** 
     * Sets the date to the sunday following the current date.
     */
    function handleNextSunday(): void {
        let nextSunday = getNextSunday($serviceDay);
        serviceDay.set(nextSunday);
        formattedDate = formatDate(nextSunday);
    }

    /**
     * Sets the date in the backend to the selected date.
     */
    function handleSubmit(): void {
        eel.set_date(formatDate($serviceDay))();
        activeTab.set('liturgy');
    }
</script>


<div 
    class='container-item'
    in:fly="{{ x: -1000, duration: 300 }}"
    out:fly="{{ x: 1000, duration: 300 }}"
>
    <h1>Build worship plan for {formattedDate}</h1>
    <div class='flex'>
        <input type="date" bind:value={formattedDate} on:change={handleDateChange}/>
        <button on:click={handleNextSunday}>Next sunday</button>
        <button on:click={handleSubmit}>Confirm</button>
    </div>
</div>

<style>
    .flex {
        display: flex;
        flex-direction: row;
        justify-content: center;
        column-gap: 1rem;
    }
</style>