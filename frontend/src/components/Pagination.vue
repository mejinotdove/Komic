<template>
  <div class="flex justify-center items-center gap-1.5 px-5 py-4 flex-wrap">
    <span class="text-xs text-text-dim mr-2 select-none tabular-nums">
      {{ store.total }} 本 · 第 {{ store.page }}/{{ store.totalPages }} 页
    </span>
    <button
      v-if="store.page > 1"
      @click="store.setPage(store.page - 1)"
      class="flex items-center justify-center w-8 h-8 rounded-full text-sm text-text-dim transition-all duration-200 cursor-pointer bg-transparent border-0 hover:bg-[var(--hover-bg)] hover:text-[var(--hover-text)]"
    >
      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
      </svg>
    </button>

    <template v-for="(p, idx) in store.pages" :key="idx">
      <span v-if="p === null" class="text-text-dim text-sm px-1 select-none">…</span>
      <button
        v-else
        @click="store.setPage(p)"
        class="flex items-center justify-center min-w-[32px] h-8 px-2 rounded-full text-sm font-medium transition-all duration-200 cursor-pointer border-0"
        :class="p === store.page
          ? 'bg-accent text-white shadow-accent'
          : 'text-text-dim bg-transparent hover:bg-[var(--hover-bg)] hover:text-[var(--hover-text)]'"
      >{{ p }}</button>
    </template>

    <button
      v-if="store.page < store.totalPages"
      @click="store.setPage(store.page + 1)"
      class="flex items-center justify-center w-8 h-8 rounded-full text-sm text-text-dim transition-all duration-200 cursor-pointer bg-transparent border-0 hover:bg-[var(--hover-bg)] hover:text-[var(--hover-text)]"
    >
      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
        <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
      </svg>
    </button>
  </div>
</template>

<script setup>
import { useComicStore } from '../stores/comic'
const store = useComicStore()
</script>
