<script setup>
	// ref = reactive variables
	// onMounted = run code on load
	import { ref, onMounted } from "vue"

	console.log("Script ran")

	const moon = ref({})
	const loading = ref(true)

	onMounted(async () => {

		try {
			const resp = await fetch("https://localhost:5000/api/moon")
			const data = await resp.json()

			moon.value = data

		} catch (err) {
			console.error(err)
		} finally {
			loading.value = false
		}

	})

</script>

<template>
  <header>
  </header>

  <main>
	  <h1>{{ moon.phase }}</h1>
  </main>
</template>

<style scoped>
/*
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
*/
</style>
