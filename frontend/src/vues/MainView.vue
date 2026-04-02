<script setup>
	import { ref, onMounted } from "vue"

	const moon_phase = ref({})
	const loadingData = ref(true)
	const error = ref(false)

	onMounted(async () => {
		try {
			const resp = await fetch("/api/moon_img")
			if (!resp.ok) {
			// Catches a bad response code from the flask api
				console.error(resp.status)
				error.value = true
			}
			const data = await resp.json()
			moon_phase.value = data
		} catch (err) {
			console.error(err)
		} finally {
			loadingData.value = false
		}
	})
</script>

<template>
	<div class="error" v-if="error">
		<h1>Something went wrong. Please try again later.</h1>
	</div>
	<div v-else-if="loadingData">
		<h2>Loading data...</h2>
	</div>
	<div class="mainView" v-else>
		<div class="dataView">
			<div>
				<img class="moonImg" :src="moon_phase.imageUrl" />
			</div>
			<div class="moonData">
				<div class="card">
					<h2>Date:</h2>
					<p>{{ moon_phase.date }} (YYYY-MM-DD)</p>
				</div>
				<div class="card">
					<h2>Date:</h2>
					<p>{{ moon_phase.date }} (YYYY-MM-DD)</p>
				</div>
				<div class="card">
					<h2>Date:</h2>
					<p>{{ moon_phase.date }} (YYYY-MM-DD)</p>
				</div>
			</div>
		</div>
		<div class="infoInput">
			hello
		</div>
	</div>
</template>
