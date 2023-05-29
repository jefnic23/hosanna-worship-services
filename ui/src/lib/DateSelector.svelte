<script lang="ts">
    import { eel } from "../main";

    let today: Date = new Date();
    let formattedDate: string = formatDate(today);

    /**
     * Formats the date to the format YYYY-MM-DD
     * @param date
     */
    function formatDate(date: Date): string {
        let year = date.toLocaleString('default', { year: 'numeric' });
        let month = date.toLocaleString('default', { month: '2-digit' });
        let day = date.toLocaleString('default', { day: '2-digit' });
        return `${year}-${month}-${day}`;
    }

    /**
     * Sets the date to the sunday following the current date
     * @param day
     */
    function getNextSunday(day: Date): Date {
        day.setDate(day.getDate() + ((0 - day.getDay()) % 7) + 7);
        return day;
    }

    /**
     * Sets the date to the selected date
     * @param e
     */
    function handleDateChange(e: Event): void {
        let dateParts: string[] = (e.target as HTMLInputElement).value.split('-');
        today = new Date(parseInt(dateParts[0]), parseInt(dateParts[1]) - 1, parseInt(dateParts[2]));
        formattedDate = formatDate(today);
    }

    /** 
     * Sets the date to the sunday following the current date
     */
     function handleNextSunday(): void {
        today = getNextSunday(today);
        formattedDate = formatDate(today);
    }

    /**
     * Prints the date
     */
    function handleSubmit(): void {
        eel.set_date(formatDate(today))();
    }
</script>

<div>
    Select day: <input type="date" bind:value={formattedDate} on:change={handleDateChange}/>
    <button on:click={handleNextSunday}>Next sunday</button>
    <button on:click={handleSubmit}>Submit</button>
</div>
