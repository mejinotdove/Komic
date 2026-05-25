<template>
  <div
    class="group relative bg-surface rounded-xl overflow-hidden border border-surface-border transition-all duration-250 cursor-pointer flex flex-col will-change-transform hover:-translate-y-1 hover:shadow-card-hover hover:border-surface-border/60"
    @click="store.openDetail(comic.id)"
  >
    <div class="relative aspect-[3/4] bg-card overflow-hidden">
      <img
        :src="api.getCoverUrl(comic.id)"
        :alt="comic.title"
        loading="lazy"
        class="w-full h-full object-cover transition-all duration-300 group-hover:scale-[1.05]"
      />

      <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-250 flex items-end justify-center pb-4 pointer-events-none">
        <span class="text-xs text-white/80 font-medium tracking-wide bg-white/10 backdrop-blur-sm px-3 py-1 rounded-full">
          查看详情
        </span>
      </div>

      <div v-if="comic.page_count" class="absolute top-2 left-2 bg-black/60 backdrop-blur-sm text-[10px] text-white/80 font-medium px-1.5 py-0.5 rounded-md leading-none">
        {{ comic.page_count }}P
      </div>
    </div>

    <div class="p-2.5 flex-1 flex flex-col gap-1.5">
      <div class="text-xs font-medium leading-snug line-clamp-2 text-text-primary/80 group-hover:text-accent transition-colors duration-200">
        {{ comic.title }}
      </div>
      <div v-if="comic.tags && comic.tags.length" class="flex flex-wrap gap-1">
        <span
          v-for="(tag, i) in comic.tags.slice(0, 3)"
          :key="tag"
          class="text-[10px] font-medium px-1.5 py-0.5 rounded-md"
          :style="{ background: tagColors[i % tagColors.length].bg, color: tagColors[i % tagColors.length].text }"
        >{{ tag }}</span>
        <span v-if="comic.tags.length > 3" class="text-[10px] text-text-dim">+{{ comic.tags.length - 3 }}</span>
      </div>
      <div v-if="comic.page_count" class="text-[10px] text-text-dim">
        {{ comic.page_count }} 页
      </div>
      <StarRating
        :comic-id="comic.id"
        :rating="comic.rating"
        class="mt-auto"
      />
    </div>
  </div>
</template>

<script setup>
import { useComicStore } from '../stores/comic'
import { api } from '../api'
import StarRating from './StarRating.vue'

defineProps({ comic: { type: Object, required: true } })
const store = useComicStore()

const tagColors = [
  { bg: '#2a3a4a', text: '#8ab4d8' },
  { bg: '#3a2a4a', text: '#c8a0e0' },
  { bg: '#2a4a3a', text: '#80c8a0' },
  { bg: '#4a3a2a', text: '#d8b080' },
]
</script>
