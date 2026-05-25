import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

const STORAGE_KEY = 'komic-theme'

const themes = {
  dark: { label: '暗色', icon: '🌙' },
  ocean: { label: '海洋', icon: '🌊' },
  forest: { label: '森林', icon: '🌿' },
  cherry: { label: '樱花', icon: '🌸' },
  sunset: { label: '日落', icon: '🌅' },
  mint: { label: '薄荷', icon: '🍃' },
  paper: { label: '白纸', icon: '📄' },
  frost: { label: '冰霜', icon: '❄️' },
  cream: { label: '奶油', icon: '🧈' },
}

export const useThemeStore = defineStore('theme', () => {
  const saved = localStorage.getItem(STORAGE_KEY)
  const name = ref(saved && themes[saved] ? saved : 'dark')

  watch(name, (val) => {
    localStorage.setItem(STORAGE_KEY, val)
    document.documentElement.dataset.theme = val
  }, { immediate: true })

  function setTheme(val) {
    if (themes[val]) name.value = val
  }

  return { name, themes, setTheme }
})
