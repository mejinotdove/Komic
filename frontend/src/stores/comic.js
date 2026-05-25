import { defineStore } from 'pinia'
import { api } from '../api'

export const useComicStore = defineStore('comic', {
  state: () => ({
    comics: [],
    total: 0,
    page: 1,
    pageSize: 30,
    totalPages: 1,

    search: '',
    rating: '',
    tag: '',
    sortBy: 'title',
    sortDir: 'asc',

    loading: false,
    error: '',

    scanRunning: false,
    scanProgress: null,
    scanError: '',
    scanDone: false,

    currentComic: null,
    detailLoading: false,
    detailOpen: false,
  }),

  getters: {
    pages: (state) => {
      const { page, totalPages } = state
      if (totalPages <= 1) return []
      const window = 5
      const start = Math.max(1, page - window)
      const end = Math.min(totalPages, page + window)
      const pages = []
      if (start > 1) {
        pages.push(1)
        if (start > 2) pages.push(null)
      }
      for (let i = start; i <= end; i++) pages.push(i)
      if (end < totalPages) {
        if (end < totalPages - 1) pages.push(null)
        pages.push(totalPages)
      }
      return pages
    },
  },

  actions: {
    async fetchComics() {
      this.loading = true
      this.error = ''
      try {
        const data = await api.getComics({
          page: this.page,
          page_size: this.pageSize,
          search: this.search || undefined,
          rating: this.rating || undefined,
          tag: this.tag || undefined,
          sort_by: this.sortBy,
          sort_dir: this.sortDir,
        })
        this.comics = data.items
        this.total = data.total
        this.totalPages = Math.ceil(data.total / this.pageSize)
      } catch (e) {
        this.error = '加载漫画失败'
      } finally {
        this.loading = false
      }
    },

    setFilter(key, value) {
      this[key] = value
      this.page = 1
      this.fetchComics()
    },

    setPage(page) {
      this.page = page
      this.fetchComics()
    },

    async setRating(id, rating) {
      try {
        await api.setRating(id, rating)
        const comic = this.comics.find(c => c.id === id)
        if (comic) comic.rating = rating
        if (this.currentComic && this.currentComic.id === id) {
          this.currentComic.rating = rating
        }
      } catch (e) {
        // silent
      }
    },

    async openDetail(id) {
      this.detailLoading = true
      this.detailOpen = true
      try {
        this.currentComic = await api.getComic(id)
      } catch (e) {
        this.currentComic = null
      } finally {
        this.detailLoading = false
      }
    },

    closeDetail() {
      this.detailOpen = false
      this.currentComic = null
    },

    async triggerScan() {
      try {
        const res = await api.startScan()
        if (res.status === 409) {
          this.scanError = '扫描正在进行中'
          return
        }
        this.scanRunning = true
        this.scanProgress = null
        this.scanError = ''
        this.scanDone = false
        this.pollScan()
      } catch (e) {
        this.scanError = '启动扫描失败'
      }
    },

    async pollScan() {
      try {
        const data = await api.getScanStatus()
        if (data.error) {
          this.scanError = data.error
          this.scanRunning = false
          this.scanDone = true
          this.fetchComics()
          return
        }
        if (data.running) {
          this.scanProgress = data
          this.scanRunning = true
          setTimeout(() => this.pollScan(), 1000)
        } else {
          this.scanProgress = null
          this.scanRunning = false
          this.scanDone = true
          this.fetchComics()
        }
      } catch (e) {
        this.scanRunning = false
      }
    },
  },
})
