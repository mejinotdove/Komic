<template>
  <div class="sticky top-[57px] z-30 bg-surface/60 backdrop-blur-md border-b border-surface-border">
    <div class="px-5 py-3">
      <div class="relative mb-2.5">
        <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
        </svg>
        <input
          v-model="searchText"
          type="text"
          placeholder="搜索漫画..."
          class="w-full bg-input text-text-primary border border-surface-border pl-9 pr-3 py-2 rounded-xl text-sm outline-none transition-all duration-200 placeholder:text-text-dim focus:border-accent/50 focus:ring-1 focus:ring-accent/20"
        />
      </div>
      <div class="flex flex-wrap gap-2">
        <select
          v-model="store.rating"
          @change="store.setFilter('rating', store.rating)"
          class="flex-1 min-w-[100px] bg-input text-text-secondary border border-surface-border px-3 py-1.5 rounded-lg text-sm outline-none transition-all duration-200 cursor-pointer focus:border-accent/50 focus:ring-1 focus:ring-accent/20"
        >
          <option value="">全部评分</option>
          <option value="0">未评分</option>
          <option value="5">5 星</option>
          <option value="4">4 星</option>
          <option value="3">3 星</option>
          <option value="2">2 星</option>
          <option value="1">1 星</option>
        </select>
        <select
          v-model="store.tag"
          @change="store.setFilter('tag', store.tag)"
          class="flex-1 min-w-[100px] bg-input text-text-secondary border border-surface-border px-3 py-1.5 rounded-lg text-sm outline-none transition-all duration-200 cursor-pointer focus:border-accent/50 focus:ring-1 focus:ring-accent/20"
        >
          <option value="">全部标签</option>
          <option v-for="t in tags" :key="t.id" :value="t.name">{{ t.name }}</option>
        </select>
        <select
          v-model="store.sortBy"
          @change="store.setFilter('sortBy', store.sortBy)"
          class="flex-1 min-w-[90px] bg-input text-text-secondary border border-surface-border px-3 py-1.5 rounded-lg text-sm outline-none transition-all duration-200 cursor-pointer focus:border-accent/50 focus:ring-1 focus:ring-accent/20"
        >
          <option value="title">按标题</option>
          <option value="file_mtime">按修改时间</option>
        </select>
        <select
          v-model="store.sortDir"
          @change="store.setFilter('sortDir', store.sortDir)"
          class="flex-1 min-w-[80px] bg-input text-text-secondary border border-surface-border px-3 py-1.5 rounded-lg text-sm outline-none transition-all duration-200 cursor-pointer focus:border-accent/50 focus:ring-1 focus:ring-accent/20"
        >
          <option value="asc">升序</option>
          <option value="desc">降序</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useComicStore } from '../stores/comic'
import { api } from '../api'

const store = useComicStore()
const searchText = ref(store.search)
const tags = ref([])

let timer = null
watch(searchText, (val) => {
  if (timer) clearTimeout(timer)
  timer = setTimeout(() => {
    store.setFilter('search', val)
  }, 300)
})

onMounted(async () => {
  try {
    tags.value = await api.getTags()
  } catch (e) {
    // silent
  }
})
</script>
