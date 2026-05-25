<template>
  <div v-if="store.loading" class="px-5 pt-5">
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 2xl:grid-cols-7 gap-3.5">
      <div v-for="n in 14" :key="n" class="bg-surface rounded-xl overflow-hidden border border-surface-border">
        <div class="aspect-[3/4] relative bg-input overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/[0.04] to-transparent animate-shimmer"></div>
        </div>
        <div class="p-2.5 space-y-2">
          <div class="h-3 bg-surface-hover rounded w-3/4 overflow-hidden relative">
            <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/[0.04] to-transparent animate-shimmer"></div>
          </div>
          <div class="h-2.5 bg-surface-hover rounded w-1/2 overflow-hidden relative">
            <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/[0.04] to-transparent animate-shimmer"></div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="store.error" class="flex flex-col items-center justify-center py-24 text-text-muted gap-3">
    <svg class="w-10 h-10 text-text-dim" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
      <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
    </svg>
    <span class="text-sm">{{ store.error }}</span>
  </div>

  <div v-else-if="store.comics.length === 0" class="flex flex-col items-center justify-center py-24 text-text-dim gap-3">
    <svg class="w-12 h-12 text-[#333]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1">
      <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
    </svg>
    <span class="text-sm">没有找到漫画</span>
  </div>

  <div v-else class="px-5 pt-5">
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 2xl:grid-cols-7 gap-3.5">
      <ComicCard
        v-for="comic in store.comics"
        :key="comic.id"
        :comic="comic"
      />
    </div>
  </div>

  <div v-if="!store.loading" class="text-center text-xs text-text-dim py-4 select-none">
    共 {{ store.total }} 本漫画
  </div>
</template>

<script setup>
import { useComicStore } from '../stores/comic'
import ComicCard from './ComicCard.vue'

const store = useComicStore()
</script>
