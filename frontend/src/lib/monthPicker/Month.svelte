<script lang="ts">
	import ChevronLeft from 'svelte-material-icons/ChevronLeft.svelte';

	export let fromYear: number;
	export let toYear: number;
	export let selectedDate: Date;

	let currentYear: number;

	const formatter = new Intl.DateTimeFormat('es-AR', { month: 'short' });
	const setDate = (year: number, month: number) => {
		selectedDate = new Date(year, month);
	};

	$: currentYear = selectedDate.getFullYear();
</script>

<div on:click|stopPropagation={() => {}}>
	<header class="flex justify-between items-center mb-2">
		<button
			type="button"
			class="border rounded-md border-gray p-2 cursor-pointer rotate-0"
			class:cursor-not-allowed={currentYear === fromYear}
			disabled={currentYear === fromYear}
			on:click={() => {
				setDate(selectedDate.getFullYear() - 1, selectedDate.getMonth());
			}}
		>
			<ChevronLeft
				width="24"
				height="24"
				color={currentYear === fromYear ? '#7a7a7a' : '#333333'}
			/>
		</button>
		<span class="mx-2">
			{currentYear}
		</span>
		<button
			type="button"
			class="border rounded-md border-gray p-2 cursor-pointer rotate-180"
			class:cursor-not-allowed={currentYear === toYear}
			disabled={currentYear === toYear}
			on:click={() => {
				setDate(selectedDate.getFullYear() + 1, selectedDate.getMonth());
			}}
		>
			<ChevronLeft width="24" height="24" color={currentYear === toYear ? '#7a7a7a' : '#333333'} />
		</button>
	</header>
	<div class="grid grid-cols-3 gap-1 md:gap-2 w-[140px] md:w-[190px]">
		{#each [...Array(12).keys()] as idx}
			<div
				class="border rounded p-1 md:p-2 text-center cursor-pointer hover:border-coral transition-all"
				class:bg-coral={selectedDate.getMonth() === idx}
				class:text-white={selectedDate.getMonth() === idx}
				on:click={() => {
					setDate(selectedDate.getFullYear(), idx);
				}}
			>
				<span>{formatter.format(new Date(2020, idx))}</span>
			</div>
		{/each}
	</div>
</div>
