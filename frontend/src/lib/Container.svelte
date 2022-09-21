<script>
	export let title;
</script>

<div class="font-body bg-zinc-100 container mx-auto rounded-xl p-3 md:p-6 mt-6 shadow-md">
	<header class="flex justify-between gap-4 mb-4">
		<h2 class="flex-1 text-2xl text-gray-333333 font-medium">{title}</h2>
		<slot name="header" />
	</header>
	<slot />
</div>
