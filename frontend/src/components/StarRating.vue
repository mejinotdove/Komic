<template>
  <div class="flex gap-0.5" @click.stop>
    <button
      v-for="i in 5"
      :key="i"
      @click="handleClick(i)"
      class="relative text-sm transition-all duration-150 cursor-pointer bg-transparent border-none p-0.5 leading-none outline-none"
      :class="i <= localHover ? 'text-gold scale-110' : i <= rating ? 'text-gold' : 'text-text-dim'"
      @mouseenter="localHover = i"
      @mouseleave="localHover = 0"
      :title="`${i} 星`"
    >
      <svg
        :class="['transition-transform duration-200', clickedStar === i && 'animate-star-pop']"
        @animationend="clickedStar = 0"
        width="14" height="14" viewBox="0 0 24 24"
        :fill="i <= (localHover || rating) ? 'currentColor' : 'none'"
        :stroke="i <= (localHover || rating) ? 'currentColor' : 'currentColor'"
        stroke-width="1.5"
      >
        <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useComicStore } from '../stores/comic'

const props = defineProps({
  comicId: { type: Number, required: true },
  rating: { type: Number, default: 0 },
})
const store = useComicStore()

const localHover = ref(0)
const clickedStar = ref(0)

function handleClick(i) {
  clickedStar.value = i
  store.setRating(props.comicId, i)
}
</script>
