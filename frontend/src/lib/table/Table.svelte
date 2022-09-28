<script lang="ts">
	import { onMount } from 'svelte';
	import ArrowUp from 'svelte-material-icons/ArrowUp.svelte';
	import ChevronUp from 'svelte-material-icons/ChevronUp.svelte';

	import PageButton from './PageButton.svelte';

	export let columns: Column[] = [];
	export let rows: Row[] = [];
	export let sortBy: string = '';
	export let sortAsc: boolean = true;
	export let perPage: number = 15;

	let table: HTMLElement;
	let totalPages: number = 0;
	let currentPage: number = 0;
	let filterRows: Row[] = [];

	const handleSort = (key: string) => {
		if ((sortBy = key)) {
			sortAsc = !sortAsc;
		} else {
			sortBy = key;
			sortAsc = true;
		}

		rows = rows.sort((a, b) => {
			const d = sortAsc ? -1 : 1;
			if (a[sortBy] < b[sortBy]) return 1 * d;
			else return -1 * d;
		});
		currentPage = 0;
	};

	const hadlePaginate = (newPage: number) => {
		currentPage = newPage;
		table.scrollIntoView({
			behavior: 'smooth'
		});
	};

	$: filterRows = rows.slice(currentPage * perPage, (currentPage + 1) * perPage);
	$: totalPages = Math.round(rows.length / perPage) - 1;

	onMount(() => {
		if (sortBy === '') sortBy = columns[0].key;
	});
</script>

<div bind:this={table} class="font-body pt-4">
	<slot />
	<div class="flex md:hidden mb-2">
		<select
			bind:value={sortBy}
			on:change={() => handleSort(sortBy)}
			class="flex-1 px-3 py-1.5 text-gray-999999 font-medium rounded-l-md border border-solid border-gray"
		>
			{#each columns as col}
				<option value={col.key}>
					{col.label}
				</option>
			{/each}
		</select>
		<button on:click={() => handleSort(sortBy)} class="p-2 rounded-r-md bg-coral">
			<div class="w-4 h-4 transition-all" class:rotate-180={!sortAsc}>
				<ArrowUp width="16" height="16" color="white" />
			</div>
		</button>
	</div>

	<table class="w-full mx-auto border-separate border-spacing-y-1 overflow-x-auto">
		<thead class="hidden md:table-header-group">
			<tr class="bg-white shadow-lg">
				{#each columns as col, i}
					<td
						class="text-gray-999999 font-medium text-lg px-3 py-2 cursor-pointer"
						style={'width' in col ? `width: ${col.width}px` : ''}
						class:pl-4={i === 0}
						class:rounded-l-md={i === 0}
						class:pr-4={i === columns.length - 1}
						class:rounded-r-md={i === columns.length - 1}
						on:click={() => handleSort(col.key)}
					>
						<div class="flex items-center justify-start">
							<span>{col.label}</span>
							<div class="w-4 h-4 ml-2 transition-all" class:rotate-180={!sortAsc}>
								{#if sortBy === col.key}
									<ArrowUp width="16" height="16" />
								{/if}
							</div>
						</div>
					</td>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#each filterRows as row}
				<tr
					class="block md:table-row mb-2 rounded-md bg-white text-end md:text-start hover:shadow-lg"
				>
					{#each columns as col, i}
						<td
							data-label={col.label}
							class="text-gray-333333 font-light flex md:table-cell justify-between px-3 py-2"
							class:pl-4={i === 0}
							class:rounded-l-md={i === 0}
							class:pr-4={i === columns.length - 1}
							class:rounded-r-md={i === columns.length - 1}
						>
							{row[col.key]}
						</td>
					{/each}
				</tr>
			{/each}
		</tbody>
	</table>

	<div class="flex justify-end mt-2">
		<PageButton page="1" active={currentPage === 0} onClick={() => hadlePaginate(0)} />
		{#if ![0, totalPages].includes(currentPage)}
			<PageButton page={currentPage + 1} active={true} onClick={() => hadlePaginate(currentPage)} />
		{/if}
		<PageButton
			page={totalPages + 1}
			active={currentPage === totalPages}
			onClick={() => hadlePaginate(totalPages)}
		/>
		<button
			type="button"
			class="ml-2 border rounded-md border-gray p-2 cursor-pointer rotate-[270deg]"
			class:bg-gray={currentPage === 0}
			class:cursor-not-allowed={currentPage === 0}
			disabled={currentPage === 0}
			on:click={() => hadlePaginate(currentPage - 1)}
		>
			<ChevronUp width="24" height="24" color={currentPage === 0 ? '#7a7a7a' : '#333333'} />
		</button>
		<button
			type="button"
			class="ml-2 border rounded-md border-gray p-2 cursor-pointer rotate-90"
			class:bg-gray={currentPage === totalPages}
			class:cursor-not-allowed={currentPage === totalPages}
			disabled={currentPage === totalPages}
			on:click={() => hadlePaginate(currentPage + 1)}
		>
			<ChevronUp
				width="24"
				height="24"
				color={currentPage === totalPages ? '#7a7a7a' : '#333333'}
			/>
		</button>
	</div>
</div>

<style lang="scss" scoped>
	@media screen and (max-width: 768px) {
		td {
			border-bottom: 1px solid #f5f5f5;

			&:before {
				content: attr(data-label);
				@apply pr-2 text-left font-medium text-gray-999999;
			}
		}
	}
</style>
