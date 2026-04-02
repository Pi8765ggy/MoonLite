<script setup>
	import { ref, onMounted } from "vue"

	const display = ref({})
	const loadingData = ref(true)

	onMounted(async () => {
		try {
			const resp = await fetch("/api/moon_phase")
			const data = await resp.json()
			display.value = data
		} catch (err) {
			console.error(err)
		} finally {
			loadingData.value = false
		}
	})
</script>

<template>
	<img v-if="!loadingData" :src="display.data.imageUrl" />
	<p v-else>Loading data...</p>
</template>
