<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const identifier = ref('')
const password    = ref('')
const rememberMe  = ref(false)
const showPassword = ref(false)
const loading     = ref(false)
const errorMsg    = ref('')

async function handleLogin() {
  errorMsg.value = ''
  if (!identifier.value || !password.value) {
    errorMsg.value = 'Please enter your credentials and password.'
    return
  }

  loading.value = true
  try {
    let res
    try {
      res = await fetch('http://localhost:5555/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: identifier.value,
          password: password.value,
        }),
      })
    } catch (networkErr) {
      errorMsg.value = 'Cannot connect to server. Make sure the backend is running on port 5555.'
      return
    }

    let data
    try {
      data = await res.json()
    } catch {
      errorMsg.value = 'Server returned an unexpected response. Please try again.'
      return
    }

    if (!res.ok) {
      errorMsg.value = data.message || 'Login failed. Please check your credentials.'
      return
    }

    // Store token
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('user', JSON.stringify(data.user))

    // Redirect based on role
    const role = data.user?.role
    if (role === 'admin')          router.push('/admin/dashboard')
    else if (role === 'student')   router.push('/student/dashboard')
    else if (role === 'recruiter') router.push('/company/dashboard')
    else router.push('/')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="lp-login-page d-flex align-items-center justify-content-center min-vh-100">

    <div class="lp-container text-center">

      <!-- Brand Header -->
      <div class="lp-brand mb-4">
        <img src="/Only_logo.png" alt="LaunchPad Logo" class="lp-logo mb-3">
        <h1 class="lp-brand-name">Launch Pad</h1>
        <p class="lp-tagline">Elevate Your Career Trajectory</p>
      </div>

      <!-- Card -->
      <div class="lp-card">
        <h2 class="lp-card-title mb-4">Login to Portal</h2>

        <!-- Error Alert -->
        <div v-if="errorMsg" class="alert lp-alert-error mb-3 d-flex align-items-center gap-2" role="alert">
          <i class="bi bi-exclamation-circle-fill"></i>
          <span>{{ errorMsg }}</span>
        </div>

        <form @submit.prevent="handleLogin" novalidate>

          <!-- Email / Username -->
          <div class="mb-3 text-start">
            <label for="lp-identifier" class="lp-label">Email or Username</label>
            <div class="lp-input-group">
              <span class="lp-input-icon"><i class="bi bi-person"></i></span>
              <input
                id="lp-identifier"
                v-model="identifier"
                type="text"
                class="lp-input"
                placeholder="Enter your credentials"
                autocomplete="username"
                required
              >
            </div>
          </div>

          <!-- Password -->
          <div class="mb-3 text-start">
            <label for="lp-password" class="lp-label">Password</label>
            <div class="lp-input-group">
              <span class="lp-input-icon"><i class="bi bi-lock"></i></span>
              <input
                id="lp-password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                class="lp-input lp-input--has-toggle"
                placeholder="••••••••"
                autocomplete="current-password"
                required
              >
              <button
                type="button"
                class="lp-password-toggle"
                :aria-label="showPassword ? 'Hide password' : 'Show password'"
                @click="showPassword = !showPassword"
              >
                <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
              </button>
            </div>
          </div>

          <!-- Remember Me -->
          <div class="mb-4 text-start d-flex align-items-center gap-2">
            <input
              id="lp-remember"
              v-model="rememberMe"
              type="checkbox"
              class="lp-checkbox"
            >
            <label for="lp-remember" class="lp-label-inline">Remember this device</label>
          </div>

          <!-- Login Button -->
          <button
            id="lp-login-btn"
            type="submit"
            class="lp-btn-primary w-100"
            :disabled="loading"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            {{ loading ? 'Logging in…' : 'Login' }}
          </button>
        </form>

        <!-- Divider -->
        <div class="lp-divider my-4"></div>

        <!-- Sign-up Links -->
        <p class="lp-signup-prompt mb-3">Don't have an account yet?</p>
        <div class="d-flex gap-3 justify-content-center">
          <button
            id="lp-student-signup-btn"
            type="button"
            class="lp-btn-outline flex-fill"
            @click="router.push('/signup/student')"
          >
            Student Sign-up
          </button>
          <button
            id="lp-company-signup-btn"
            type="button"
            class="lp-btn-outline flex-fill"
            @click="router.push('/signup/company')"
          >
            Company Sign-up
          </button>
        </div>
      </div><!-- /.lp-card -->

    </div><!-- /.lp-container -->
  </div>
</template>

<style scoped>


.lp-login-page {
  --lp-eerie:     #27231E;
  --lp-slate:     #3A5253;
  --lp-cambridge: #81B29A;
  --lp-snow:      #FFF5F5;
  --lp-sienna:    #E07A5F;

  background-color: #f5f5f0;
  font-family: 'Inter', system-ui, sans-serif;
  min-height: 100vh;
}

/* Page Container */
.lp-container {
  width: 100%;
  max-width: 520px;
  padding: 2rem 1rem;
}

/* Brand Header */
.lp-logo {
  width: 72px;
  height: 72px;
  object-fit: contain;
  filter: drop-shadow(0 2px 8px rgba(39, 35, 30, 0.12));
}

.lp-brand-name {
  font-size: 2rem;
  font-weight: 800;
  color: var(--lp-eerie);
  letter-spacing: -0.5px;
  margin-bottom: 0.25rem;
}

.lp-tagline {
  font-size: 0.9rem;
  color: var(--lp-slate);
  font-weight: 400;
  letter-spacing: 0.3px;
  margin-bottom: 0;
}

/* Card */
.lp-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 2.4rem 2.2rem;
  box-shadow:
    0 2px 6px rgba(39, 35, 30, 0.06),
    0 8px 30px rgba(39, 35, 30, 0.09);
  text-align: left;
}

.lp-card-title {
  font-size: 1.45rem;
  font-weight: 700;
  color: var(--lp-eerie);
  text-align: center;
  letter-spacing: -0.3px;
}

/* Labels */
.lp-label {
  display: block;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--lp-eerie);
  margin-bottom: 0.4rem;
  letter-spacing: 0.2px;
}

.lp-label-inline {
  font-size: 0.84rem;
  color: var(--lp-eerie);
  cursor: pointer;
  user-select: none;
}

/* Input Group */
.lp-input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.lp-input-icon {
  position: absolute;
  left: 0.9rem;
  color: var(--lp-slate);
  font-size: 1rem;
  pointer-events: none;
  line-height: 1;
}

.lp-input {
  width: 100%;
  padding: 0.7rem 0.9rem 0.7rem 2.6rem;
  border: 1.5px solid #e2e2de;
  border-radius: 10px;
  font-size: 0.9rem;
  font-family: inherit;
  color: var(--lp-eerie);
  background: #fafafa;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
  outline: none;
}

.lp-input--has-toggle {
  padding-right: 2.8rem;
}

.lp-input:focus {
  border-color: var(--lp-cambridge);
  box-shadow: 0 0 0 3px rgba(129, 178, 154, 0.2);
  background: #fff;
}

.lp-input::placeholder {
  color: #b0aba6;
}

/* Password Toggle Button */
.lp-password-toggle {
  position: absolute;
  right: 0.8rem;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--lp-slate);
  padding: 0;
  font-size: 1rem;
  line-height: 1;
  transition: color 0.2s ease;
}

.lp-password-toggle:hover {
  color: var(--lp-sienna);
}

/* Checkbox */
.lp-checkbox {
  width: 16px;
  height: 16px;
  cursor: pointer;
  accent-color: var(--lp-sienna);
  flex-shrink: 0;
  border-radius: 4px;
}

/* Primary Button */
.lp-btn-primary {
  display: block;
  width: 100%;
  padding: 0.75rem 1.5rem;
  background: var(--lp-sienna);
  color: #ffffff;
  font-family: inherit;
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: 0.4px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.12s ease, box-shadow 0.2s ease;
  box-shadow: 0 4px 14px rgba(224, 122, 95, 0.35);
}

.lp-btn-primary:hover:not(:disabled) {
  background: #c96a4e;
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(224, 122, 95, 0.45);
}

.lp-btn-primary:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(224, 122, 95, 0.3);
}

.lp-btn-primary:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

/* Outline Button */
.lp-btn-outline {
  padding: 0.6rem 1rem;
  background: transparent;
  color: var(--lp-eerie);
  font-family: inherit;
  font-size: 0.84rem;
  font-weight: 600;
  border: 1.5px solid #d9d4d0;
  border-radius: 10px;
  cursor: pointer;
  transition: border-color 0.2s ease, color 0.2s ease, background 0.2s ease;
}

.lp-btn-outline:hover {
  border-color: var(--lp-cambridge);
  color: var(--lp-slate);
  background: rgba(129, 178, 154, 0.08);
}

/* Divider */
.lp-divider {
  height: 1px;
  background: #ede8e5;
  border: none;
}

/* Sign-up Prompt */
.lp-signup-prompt {
  font-size: 0.85rem;
  color: var(--lp-eerie);
  text-align: center;
  font-weight: 500;
}

/* Error Alert */
.lp-alert-error {
  background: rgba(224, 122, 95, 0.1);
  border: 1px solid rgba(224, 122, 95, 0.35);
  color: #b05a40;
  border-radius: 10px;
  padding: 0.65rem 1rem;
  font-size: 0.85rem;
}

/* Responsive */
@media (max-width: 576px) {
  .lp-card {
    padding: 1.8rem 1.4rem;
  }
  .lp-brand-name {
    font-size: 1.7rem;
  }
}
</style>
