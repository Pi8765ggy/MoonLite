<script setup>
	// ref = reactive variables
	// onMounted = run code on load
	import { ref, onMounted } from "vue"
	import { useRouter } from "vue-router"

	const loadingData = ref(true)
	const user = ref({})

	const router = useRouter()

	onMounted(async () => {

		try {
			const resp = await fetch("/api/user", {
				credentials: "include"
			})
			const data = await resp.json()
			user.value = data
		} catch (err) {
			console.error(err)
		} finally {
			loadingData.value = false
		}

	})
	
	function login() {
		router.push('/login')
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
	      <router-link class="logo" to="/">MoonLite</router-link>
	      <router-link class="about" to="/about">About</router-link>
      </div>

      <div class="nav-right">
	<div v-if="!user.logged_in">
        	<button class="login-btn" @click="login">Login</button>
	</div>
	<div v-else>
		<img :src="user.picture" height=40px width=40px />
		<p> Hello, {{ user.name }}!</p>
		<button class="login-btn" @click="logout">Logout</button>
	</div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="content">
	    <router-view />
    </main>

  </div>
</template>

