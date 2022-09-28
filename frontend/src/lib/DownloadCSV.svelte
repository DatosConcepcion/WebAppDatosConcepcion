<script lang="ts">
	import DownloadOutline from 'svelte-material-icons/DownloadOutline.svelte';

	export let columns: Column[] = [];
	export let data: Row[] = [];
	export let csvName: string = 'data.csv';

	const handleClick = () => {
		const head = columns.map((col) => col.label).join(',');
		const body = data
			.map((row) =>
				columns.map((col) => `"${row[col.key].toString().replaceAll('"', "'")}"`).join(',')
			)
			.join('\n');
		const csvContent = `data:text/csv;charset=utf-8,${head}\n${body}`;

		const encodedUri = encodeURI(csvContent);
		const link = document.createElement('a');
		link.setAttribute('href', encodedUri);
		link.setAttribute('download', csvName);
		document.body.appendChild(link); // Required for FF

		link.click();
	};
</script>

<button
	class="flex items-center gap-2 p-2 bg-coral text-white rounded-md ml-auto"
	on:click={handleClick}
>
	<DownloadOutline width="18" height="18" color="white" />
	Descargar datos
</button>
