<script setup>
	// ref = reactive variables
	// onMounted = run code on load
	import { ref, onMounted } from "vue"

	console.log("Script ran")

	const moon = ref({})
	const loadingData = ref(true)
	const user = ref({})

	onMounted(async () => {

		try {
			const resp = await fetch("/api/moon")
			const data = await resp.json()
			moon.value = data

			const resp1 = await fetch("/api/user", {
				credentials: "include"
			})
			const data1 = await resp1.json()
			user.value = data1

		} catch (err) {
			console.error(err)
		} finally {
			loadingData.value = false
		}

	})

	function login() {
		window.location.href = "/auth/login"
	}

	async function logout() {

		await fetch('/auth/logout', {
			credentials: "include"
		})

		const res = await fetch('/api/user', {
			credentials: "include"
		})
		const dat = await res.json()

		user.value = dat
	}

</script>

<template>
  <div class="app">

    <!-- Navbar -->
    <nav class="navbar">
      <div class="nav-left">
        <div class="logo">MoonLite</div>
      </div>

      <div class="nav-right">
	<div v-if="!user.logged_in">
        	<button class="login-btn" @click="login">Login</button>
	</div>
	<div v-else>
		<p> Hello, {{ user.name }}!</p>
		<button class="login-btn" @click="logout">Logout</button>
	</div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="content">
      	<h1 v-if="!loading"> {{ moon.phase }} </h1>
	<p v-else> LOADING!!!!! </p>
    </main>

  </div>
</template>

<style scoped>
</style>
