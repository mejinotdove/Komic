<template>
  <div
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
    @click.self="store.closeDetail()"
  >
    <div
      v-if="store.detailLoading"
      class="modal-content bg-surface border border-surface-border rounded-2xl shadow-modal w-[90vw] max-w-[900px] max-h-[85vh] p-16 flex items-center justify-center bg-text-text-primary/[0.02]"
    >
      <svg class="w-8 h-8 text-accent animate-spin-slow" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
      </svg>
    </div>

    <div
      v-else-if="store.currentComic"
      class="modal-content bg-surface border border-surface-border rounded-2xl shadow-modal w-[90vw] max-w-[900px] max-h-[85vh] flex flex-col overflow-hidden"
    >
      <div class="relative flex gap-6 p-6 border-b border-surface-border">
        <button
          @click="store.closeDetail()"
          class="absolute top-3 right-3 z-10 flex items-center justify-center w-8 h-8 rounded-full text-text-dim transition-all duration-200 hover:text-[var(--hover-text)] hover:bg-[var(--hover-bg)] bg-transparent border-0 cursor-pointer"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

          <div class="flex-shrink-0 w-[160px] md:w-[180px]">
            <div class="w-full rounded-xl overflow-hidden shadow-lg">
              <img
                :src="api.getCoverUrl(store.currentComic.id)"
                :alt="store.currentComic.title"
                class="w-full block"
              />
            </div>
          </div>
        <div class="flex-1 min-w-0 flex flex-col gap-3 pt-0.5">
          <h2 class="text-xl font-semibold text-text-primary leading-tight break-words pr-6">
            {{ store.currentComic.title }}
          </h2>
          <div v-if="store.currentComic.tags && store.currentComic.tags.length" class="flex flex-wrap gap-1.5">
            <span
              v-for="(tag, i) in store.currentComic.tags"
              :key="tag"
              class="text-[11px] font-medium px-2 py-0.5 rounded-md"
              :style="{ background: tagColors[i % tagColors.length].bg, color: tagColors[i % tagColors.length].text }"
            >{{ tag }}</span>
          </div>
          <div class="flex items-center gap-4 text-xs text-text-muted">
            <span v-if="store.currentComic.page_count" class="flex items-center gap-1">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
              </svg>
              {{ store.currentComic.page_count }} 页
            </span>
            <span class="flex items-center gap-1">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3.375 19.5h17.25m-17.25 0a1.125 1.125 0 01-1.125-1.125M3.375 19.5h7.5c.621 0 1.125-.504 1.125-1.125m-9.75 0V5.625m0 12.75v-1.5c0-.621.504-1.125 1.125-1.125m18.375 2.625V5.625m0 12.75c0 .621-.504 1.125-1.125 1.125m1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125m0 3.75h-7.5A1.125 1.125 0 0112 18.375m9.75-12.75c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125m19.5 0v1.5c0 .621-.504 1.125-1.125 1.125M2.25 5.625v1.5c0 .621.504 1.125 1.125 1.125m0 0h17.25m-17.25 0h7.5c.621 0 1.125.504 1.125 1.125M3.375 8.25c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125m17.25-3.75h-7.5c-.621 0-1.125.504-1.125 1.125m8.625-1.125c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125m-17.25 0h7.5m-7.5 0c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125M12 10.875v-1.5m0 1.5c0 .621-.504 1.125-1.125 1.125M12 10.875c0 .621.504 1.125 1.125 1.125m-2.25 0c.621 0 1.125.504 1.125 1.125M13.125 12h7.5m-7.5 0c-.621 0-1.125.504-1.125 1.125M20.625 12c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125m-17.25 0h7.5M12 14.625v-1.5m0 1.5c0 .621-.504 1.125-1.125 1.125M12 14.625c0 .621.504 1.125 1.125 1.125m-2.25 0c.621 0 1.125.504 1.125 1.125m-1.125 0h1.5m-1.5 0c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125m1.5-3.75c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125m-3.75 0h3.75m-3.75 0c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125m3.75 0h1.5m-1.5 0c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125" />
              </svg>
              {{ (store.currentComic.format || '').toUpperCase() }}
            </span>
          </div>
          <StarRating
            :comic-id="store.currentComic.id"
            :rating="store.currentComic.rating"
          />
        </div>
      </div>

      <div class="flex gap-2.5 px-6 py-4 overflow-x-auto overflow-y-hidden flex-1 min-h-0 snap-x snap-mandatory scroll-smooth">
        <div
          v-for="(pageName, idx) in pageNames"
          :key="idx"
          class="flex-shrink-0 snap-start text-center"
        >
          <div class="w-[110px] md:w-[130px] rounded-xl overflow-hidden border border-surface-border transition-all duration-200 hover:border-text-dim hover:shadow-md">
            <img
              :src="api.getPageUrl(store.currentComic.id, idx, 150)"
              :alt="pageName"
              loading="lazy"
              class="w-full aspect-[3/4] object-cover bg-card block"
            />
          </div>
          <span class="text-[10px] text-text-dim block mt-1 tabular-nums">{{ idx + 1 }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useComicStore } from '../stores/comic'
import { api } from '../api'
import StarRating from './StarRating.vue'

const store = useComicStore()
const pageNames = ref([])

watch(() => store.currentComic, async (comic) => {
  if (!comic || !comic.page_count) {
    pageNames.value = []
    return
  }
  pageNames.value = Array.from({ length: comic.page_count }, (_, i) => `page_${i}`)
}, { immediate: true })

const tagColors = [
  { bg: '#2a3a4a', text: '#8ab4d8' },
  { bg: '#3a2a4a', text: '#c8a0e0' },
  { bg: '#2a4a3a', text: '#80c8a0' },
  { bg: '#4a3a2a', text: '#d8b080' },
]
</script>
