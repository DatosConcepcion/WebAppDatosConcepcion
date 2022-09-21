<script lang="ts">
	import Facebook from 'svelte-material-icons/Facebook.svelte';
	import Twitter from 'svelte-material-icons/Twitter.svelte';
	import Instagram from 'svelte-material-icons/Instagram.svelte';
	import Github from 'svelte-material-icons/Github.svelte';
</script>

<footer class="py-8 bg-black text-white font-title font-semibold text-center">
	<a href="https://www.datosconcepcion.com.ar/" target="_blank">
		<img src="datos-logo.png" width="80" alt="logo datos concepción" class="mx-auto block" />
	</a>
	<h2 class="text-2xl mt-8">
		UN PROYECTO DE
		<span class="font-bold">DATOS CONCEPCIÓN</span>
	</h2>
	<p class="text-xl py-2">
		Argentina - Latam | <a href="mailto:datosconcepcion22@gmail.com">datosconcepcion22@gmail.com</a>
	</p>
	<div class="flex justify-center gap-4">
		<a href="https://m.facebook.com/datosconcepcion22/" target="_blank">
			<Facebook width="32" height="32" color="white" />
		</a>
		<a href="https://twitter.com/DataConcepcion" target="_blank">
			<Twitter width="32" height="32" color="white" />
		</a>
		<a href="https://instagram.com/datos.concepcion" target="_blank">
			<Instagram width="32" height="32" color="white" />
		</a>
		<a href="https://github.com/DatosConcepcion/WebScraperDatosConcepcion" target="_blank">
			<Github width="32" height="32" color="white" />
		</a>
	</div>
</footer>
