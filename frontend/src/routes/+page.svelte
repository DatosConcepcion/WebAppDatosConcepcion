<script lang="ts">
	import type ArqueroTable from 'arquero/dist/types/table/table';

	// import { fromArrow } from "arquero"
	import { onMount } from 'svelte';
	import { tableFromIPC } from 'apache-arrow';
	import parquetModule, { readParquet } from 'parquet-wasm/esm/arrow2';

	import Container from '$lib/Container.svelte';
	import Datepicker from '$lib/Datepicker.svelte';
	import Table from '$lib/table/Table.svelte';
	import DownloadCsv from '$lib/DownloadCSV.svelte';
	import MonthPicker from '$lib/monthPicker/MonthPicker.svelte';

	const rankingCols: Column[] = [
		{ label: 'Posición', key: 'index', width: 120 },
		{ label: 'Nombre de fantasía', key: 'nombreFantasía' },
		{ label: 'CUIL', key: 'cuil', width: 150 },
		{ label: 'Importe', key: 'total' }
	];
	const contratacionesCols: Column[] = [
		{ label: 'Nombre de fantasía', key: 'nombreFantasía' },
		{ label: 'Razón social', key: 'razónSocial' },
		{ label: 'CUIL', key: 'cuil', width: 150 },
		{ label: 'Importe', key: 'total' },
		{ label: 'Cantidad de contratos', key: 'contratos' }
	];

	let innerWidth: number;
	let perPage: number = 20;
	let filterStr: string = '';
	//
	let dt: ArqueroTable;
	let totalRanking: Row[] = [];
	let constructionRanking: Row[] = [];
	let marketingRanking: Row[] = [];
	let filterRanking: Row[] = [];

	const computeRanking = ({ filterByMarket = null, filterByName = '' } = {}): Row[] => {
		let dfFilter: ArqueroTable = dt.reify();
		if (filterByMarket !== null)
			dfFilter = dt.filter(`(d) => aq.op.match(d.rubro, '${filterByMarket}')`).reify();
		if (filterByName !== '')
			dfFilter = dfFilter.filter(`(d) =>
				aq.op.match(d.razónSocial, /${filterStr}/gi) ||
				aq.op.match(d.nombreFantasía, /${filterStr}/gi) ||
				aq.op.match(d.cuil, /${filterStr}/gi)
			`);
		return dfFilter
			.groupby('cuil', 'razónSocial', 'nombreFantasía')
			.rollup({
				total: (d) => aq.op.sum(d.importe),
				contratos: (d) => aq.op.sum(d.cantidadDeContratados)
			})
			.orderby(aq.desc((d) => d.total))
			.derive({
				index: (_) => aq.op.row_number()
			})
			.objects();
	};

	// On mobile, show less page on the tables
	$: perPage = innerWidth <= 768 ? 10 : 20;

	onMount(async () => {
		// Need to await the default export first to initialize the WebAssembly code
		await parquetModule();
		// Fetch the parquet -> to arrow -> to arquero data table (dt)
		// FIXME: Add dowload progress
		// FIXME: url for production
		const resp = await fetch('http://localhost:3000/data/contrataciones.parquet.brotli');
		const parquetUint8Array = new Uint8Array(await resp.arrayBuffer());
		const arrowUint8Array = readParquet(parquetUint8Array);
		const arrowTable = tableFromIPC(arrowUint8Array);
		dt = aq.fromArrow(arrowTable).rename({
			razón_social: 'razónSocial',
			nombre_fantasía: 'nombreFantasía',
			cantidad_de_contratados: 'cantidadDeContratados'
		});

		totalRanking = computeRanking();
		constructionRanking = computeRanking({ filterByMarket: 'SERVICIO OBRA PUBLICA' });
		marketingRanking = computeRanking({ filterByMarket: 'PUBLICIDAD' });
		filterRanking = computeRanking();
	});
</script>

<svelte:head>
	<title>Concepcion Transparente</title>
	<meta name="description" content="Visualización de las contrataciones de concepción" />
</svelte:head>

<svelte:window bind:innerWidth />

<Container title="Ranking de proveedores de acuerdo al gasto total">
	<div class="flex flex-col gap-2" slot="header">
		<MonthPicker />
		<DownloadCsv columns={rankingCols} data={totalRanking} />
	</div>
	<Table columns={rankingCols} rows={totalRanking} {perPage} />
</Container>

<Container title="Ranking de contrataciones de obra pública">
	<div class="flex flex-col gap-2" slot="header">
		<Datepicker />
		<DownloadCsv columns={rankingCols} data={constructionRanking} />
	</div>
	<Table columns={rankingCols} rows={constructionRanking} {perPage} />
</Container>

<Container title="Ranking de contrataciones de publicidad oficial">
	<div class="flex flex-col gap-2" slot="header">
		<Datepicker />
		<DownloadCsv columns={rankingCols} data={marketingRanking} />
	</div>
	<Table columns={rankingCols} rows={marketingRanking} {perPage} />
</Container>

<Container title="Ranking de proveedores">
	<div class="flex flex-col gap-2" slot="header">
		<Datepicker />
		<DownloadCsv columns={contratacionesCols} data={totalRanking} />
	</div>
	<Table columns={contratacionesCols} rows={filterRanking} {perPage} sortBy="contratos">
		<input
			placeholder="Buscar por razón social, nombre de fantasía o cuil"
			class="w-full md:w-2/3 mb-4 p-1 border-gray-999999 border rounded transition-all focus:outline-coral"
			bind:value={filterStr}
			on:input={(_) => {
				filterRanking = computeRanking({ filterByName: filterStr });
			}}
		/>
	</Table>
</Container>
