<template>
  <div v-if="store.scanRunning && store.scanProgress" class="flex items-center gap-3 px-5 py-3 border-b border-surface-border bg-surface/50">
    <svg class="w-4 h-4 text-accent animate-spin-slow shrink-0" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
    </svg>
    <div class="flex-1 h-2 bg-surface-border rounded-full overflow-hidden">
      <div
        class="h-full rounded-full bg-gradient-to-r from-accent to-gold transition-all duration-500 ease-out"
        :style="{ width: pct + '%' }"
      ></div>
    </div>
    <span class="text-xs text-text-dim shrink-0 tabular-nums">
      {{ store.scanProgress.processed }}/{{ store.scanProgress.total }} ({{ pct }}%)
    </span>
  </div>
  <div
    v-else-if="store.scanDone && !store.scanError"
    class="flex items-center gap-2 px-5 py-3 border-b border-surface-border bg-surface/50 text-sm text-green-400"
  >
    <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
      <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
    </svg>
    扫描完成
  </div>
  <div
    v-else-if="store.scanError"
    class="flex items-center gap-2 px-5 py-3 border-b border-surface-border bg-surface/50 text-sm text-red-400"
  >
    <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
      <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
    </svg>
    {{ store.scanError }}
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useComicStore } from '../stores/comic'
const store = useComicStore()

const pct = computed(() => {
  if (!store.scanProgress || !store.scanProgress.total) return 0
  return Math.floor((store.scanProgress.processed / store.scanProgress.total) * 100)
})
</script>
