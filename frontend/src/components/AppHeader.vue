<template>
  <header class="sticky top-0 z-40 flex flex-wrap items-center gap-4 px-5 py-3.5 bg-surface/80 backdrop-blur-xl border-b border-surface-border">
    <div class="flex items-center gap-2.5 mr-2">
      <span class="text-xl">📚</span>
      <h1 class="text-lg font-bold text-text-primary tracking-tight">Komic</h1>
    </div>
    <nav class="flex items-center gap-3 ml-auto sm:ml-0">
      <div class="relative group">
        <button class="flex items-center gap-1.5 text-sm text-text-secondary px-2.5 py-1.5 rounded-lg transition-all duration-200 cursor-pointer bg-transparent border-0 hover:bg-[var(--hover-bg)] hover:text-[var(--hover-text)]">
          <span>{{ theme.themes[theme.name].icon }}</span>
          <svg class="w-3 h-3 transition-transform duration-200 group-hover:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
          </svg>
        </button>
        <div class="absolute right-0 top-full mt-1.5 w-44 py-1.5 bg-surface border border-surface-border rounded-xl shadow-modal opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 origin-top-right z-50 max-h-80 overflow-y-auto">
          <div v-for="(t, key) in theme.themes" :key="key">
            <div v-if="key === 'paper'" class="h-px bg-surface-border mx-3 my-1"></div>
            <button
              @click="theme.setTheme(key)"
              class="flex items-center gap-2.5 w-full text-left px-3.5 py-1.5 text-sm transition-colors duration-150 cursor-pointer bg-transparent border-0"
              :class="theme.name === key ? 'text-accent font-medium' : 'text-text-dim hover:bg-[var(--hover-bg)] hover:text-[var(--hover-text)]'"
            >
              <span>{{ t.icon }}</span>
              {{ t.label }}
              <svg v-if="theme.name === key" class="w-3.5 h-3.5 ml-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      <a
        href="/"
        class="relative text-sm text-text-secondary no-underline px-1 py-0.5 transition-colors duration-200 hover:text-[var(--hover-text)] after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 after:bg-accent after:transition-all after:duration-200 hover:after:w-full"
      >所有漫画</a>
      <button
        @click="store.triggerScan()"
        :disabled="store.scanRunning"
        :class="[
          'relative flex items-center gap-1.5 text-sm font-medium px-4 py-1.5 rounded-lg transition-all duration-200 cursor-pointer',
          store.scanRunning
            ? 'bg-accent/20 text-accent cursor-not-allowed animate-pulse-ring'
            : 'bg-accent text-white hover:bg-accent-hover active:scale-[0.97]'
        ]"
      >
        <svg v-if="store.scanRunning" class="w-3.5 h-3.5 animate-spin-slow" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
        <svg v-else class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182" />
        </svg>
        {{ store.scanRunning ? '扫描中...' : '重新扫描' }}
      </button>
    </nav>
  </header>
</template>

<script setup>
import { useComicStore } from '../stores/comic'
import { useThemeStore } from '../stores/theme'
const store = useComicStore()
const theme = useThemeStore()
</script>
