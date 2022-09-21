<script lang="ts">
	export let page: string | number;
	export let active: boolean = false;
	export let onClick = () => {};
</script>

<button
	type="button"
	class="ml-2 border rounded-md border-gray cursor-pointer hover:border-coral w-[42px] h-[42px]"
	class:bg-coral={active}
	class:border-coral={active}
	class:text-white={active}
	on:click={onClick}
>
	{page}
</button>
