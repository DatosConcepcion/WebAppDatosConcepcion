<script lang="ts">
	import CalendarBlankOutline from 'svelte-material-icons/CalendarBlankOutline.svelte';

	import MonthP from './Month.svelte';

	export let fromYear: number = 2009;
	export let toYear: number = 2020;
	export let selectedFromDate: Date = new Date(2009, 1, 0);
	export let selectedToDate: Date = new Date(2020, 12, 0);

	let hidden: boolean = true;

	const formatter = new Intl.DateTimeFormat('es-AR', { year: 'numeric', month: 'long' });
</script>

<svelte:window
	on:click={() => {
		hidden = true;
	}}
/>

<div class="relative">
	<button
		class="flex p-2 border rounded-md text-coral hover:text-white hover:bg-coral border-coral transition"
		on:click|stopPropagation={() => {
			hidden = !hidden;
		}}
	>
		<span class="pr-2 font-body text-sm"
			>{formatter.format(selectedFromDate)} a {formatter.format(selectedToDate)}</span
		>
		<CalendarBlankOutline width="18" height="18" color="#b00e57" />
	</button>
	<div class="bg-white mt-10 rounded-lg shadow p-4 absolute top-0 right-0" class:hidden>
		<div class="flex gap-4">
			<MonthP {fromYear} {toYear} bind:selectedDate={selectedFromDate} />
			<MonthP {fromYear} {toYear} bind:selectedDate={selectedToDate} />
		</div>
	</div>
</div>

<style lang="scss" scoped>
	button {
		&:hover {
			:global(path) {
				@apply fill-white;
			}
		}
	}
</style>
