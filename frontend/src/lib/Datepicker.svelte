<script lang="ts">
	import CalendarBlankOutline from 'svelte-material-icons/CalendarBlankOutline.svelte';
</script>

<div class="relative">
	<button
		class="flex p-2 border rounded-md text-coral hover:text-white hover:bg-coral border-coral transition"
	>
		<span class="pr-2 font-body text-sm">Julio, 2015 a Agosto, 2020</span>
		<CalendarBlankOutline width="18" height="18" color="#b00e57" />
	</button>
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
