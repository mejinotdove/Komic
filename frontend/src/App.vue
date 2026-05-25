<template>
  <div class="min-h-screen bg-base text-text-primary">
    <AppHeader />
    <ScanProgress />
    <SearchToolbar />
    <main>
      <ComicGrid />
      <Pagination v-if="store.totalPages > 1" />
    </main>
    <Teleport to="body">
      <Transition name="modal">
        <ComicDetailModal v-if="store.detailOpen" />
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useComicStore } from './stores/comic'
import { useThemeStore } from './stores/theme'
import AppHeader from './components/AppHeader.vue'
import ScanProgress from './components/ScanProgress.vue'
import SearchToolbar from './components/SearchToolbar.vue'
import ComicGrid from './components/ComicGrid.vue'
import Pagination from './components/Pagination.vue'
import ComicDetailModal from './components/ComicDetailModal.vue'

const store = useComicStore()
useThemeStore()

onMounted(() => {
  store.fetchComics()
})
</script>

<style>
.modal-enter-active {
  transition: opacity 0.2s ease-out;
}
.modal-enter-active .modal-content {
  transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.2s ease-out;
}
.modal-leave-active {
  transition: opacity 0.15s ease-in;
}
.modal-leave-active .modal-content {
  transition: transform 0.15s ease-in, opacity 0.15s ease-in;
}
.modal-enter-from {
  opacity: 0;
}
.modal-enter-from .modal-content {
  transform: scale(0.93);
  opacity: 0;
}
.modal-leave-to {
  opacity: 0;
}
.modal-leave-to .modal-content {
  transform: scale(0.95);
  opacity: 0;
}
</style>
