import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

export const user = ref<any>(null)
export const isLogged = computed(() => !!user.value)

export function useAuth() {
  const router = useRouter()

  const initAuth = () => {
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      user.value = JSON.parse(savedUser)
    }
  }

  const login = (userData: any, token: string) => {
    user.value = userData
    localStorage.setItem('user', JSON.stringify(userData))
    localStorage.setItem('access_token', token)
  }

  const logout = () => {
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    router.push('/')
  }

  initAuth()

  return {
    user,
    isLogged,
    login,
    logout,
  }
}
