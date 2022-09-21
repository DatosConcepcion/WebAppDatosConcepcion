<script>
	// import { fromArrow } from "arquero"
	import { onMount } from 'svelte';
	import { tableFromIPC } from 'apache-arrow';
	import parquetModule, { readParquet } from 'parquet-wasm/esm/arrow2';
	import DownloadOutline from 'svelte-material-icons/DownloadOutline.svelte';

	import Container from '$lib/Container.svelte';
	import Datepicker from '$lib/Datepicker.svelte';
	import Table from '$lib/table/Table.svelte';

	const rankingCols = [
		{ name: 'Posición', key: 'index' },
		{ name: 'Nombre de fantasía', key: 'nombreFantasía' },
		{ name: 'CUIL', key: 'cuil' },
		{ name: 'Importe', key: 'total' }
	];
	const contratacionesCols = [
		{ name: 'Nombre de fantasía', key: 'nombreFantasía' },
		{ name: 'Razón social', key: 'razónSocial' },
		{ name: 'CUIL', key: 'cuil' },
		{ name: 'Importe', key: 'total' },
		{ name: 'Cantidad de contratos', key: 'contratos' }
	];

	let totalRanking = [];
	let constructionRanking = [];
	let marketingRanking = [];
	let contratacionesRanking = [];

	const computeRanking = (dt) => {
		return dt
			.groupby('cuil', 'razónSocial', 'nombreFantasía')
			.rollup({
				total: (d) => aq.op.sum(d.importe)
			})
			.orderby(aq.desc((d) => d.total))
			.derive({
				index: (d) => op.row_number()
			})
			.objects();
	};

	onMount(async () => {
		// Need to await the default export first to initialize the WebAssembly code
		await parquetModule();
		// Fetch the parquet -> to arrow -> to arquero data table
		// FIXME: Add dowload progress
		// FIXME: url for production
		const resp = await fetch('http://localhost:3000/data/contrataciones.parquet.brotli');
		const parquetUint8Array = new Uint8Array(await resp.arrayBuffer());
		const arrowUint8Array = readParquet(parquetUint8Array);
		const arrowTable = tableFromIPC(arrowUint8Array);
		const dt = aq.fromArrow(arrowTable).rename({
			razón_social: 'razónSocial',
			nombre_fantasía: 'nombreFantasía',
			cantidad_de_contratados: 'cantidadDeContratados'
		});

		totalRanking = computeRanking(dt);
		constructionRanking = computeRanking(
			dt.filter((d) => op.match(d.rubro, 'SERVICIO OBRA PUBLICA'))
		);
		marketingRanking = computeRanking(dt.filter((d) => op.match(d.rubro, 'PUBLICIDAD')));
		contratacionesRanking = dt
			.groupby('cuil', 'razónSocial', 'nombreFantasía')
			.rollup({
				total: (d) => aq.op.sum(d.importe),
				contratos: (d) => aq.op.sum(d.cantidadDeContratados)
			})
			.orderby(aq.desc((d) => d.contratos))
			.derive({
				index: (d) => op.row_number()
			})
			.objects();
	});
</script>

<svelte:head>
	<title>Concepcion Transparente</title>
	<meta name="description" content="Visualización de las contrataciones de concepción" />
</svelte:head>

<Container title="Ranking de proveedores de acuerdo al gasto total">
	<div class="flex flex-col gap-2" slot="header">
		<Datepicker />
		<button class="flex items-center gap-2 p-2 bg-coral text-white rounded-md ml-auto">
			<DownloadOutline width="18" height="18" color="white" />
			Descargar datos
		</button>
	</div>
	<Table columns={rankingCols} rows={totalRanking} />
</Container>

<Container title="Ranking de contrataciones de obra pública">
	<div class="flex flex-col gap-2" slot="header">
		<Datepicker />
		<button class="flex items-center gap-2 p-2 bg-coral text-white rounded-md ml-auto">
			<DownloadOutline width="18" height="18" color="white" />
			Descargar datos
		</button>
	</div>
	<Table columns={rankingCols} rows={constructionRanking} />
</Container>

<Container title="Ranking de contrataciones de publicidad oficial">
	<div class="flex flex-col gap-2" slot="header">
		<Datepicker />
		<button class="flex items-center gap-2 p-2 bg-coral text-white rounded-md ml-auto">
			<DownloadOutline width="18" height="18" color="white" />
			Descargar datos
		</button>
	</div>
	<Table columns={rankingCols} rows={marketingRanking} />
</Container>

<Container title="Ranking de proveedores">
	<div class="flex flex-col gap-2" slot="header">
		<Datepicker />
		<button class="flex items-center gap-2 p-2 bg-coral text-white rounded-md ml-auto">
			<DownloadOutline width="18" height="18" color="white" />
			Descargar datos
		</button>
	</div>
	<Table columns={contratacionesCols} rows={contratacionesRanking} sortBy="contratos" />
</Container>
