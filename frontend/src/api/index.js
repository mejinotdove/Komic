const BASE = '/api'

async function request(url, options = {}) {
  const res = await fetch(`${BASE}${url}`, {
    headers: { 'Accept': 'application/json', ...options.headers },
    ...options,
  })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

export const api = {
  getComics(params = {}) {
    const q = new URLSearchParams()
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') q.set(k, v)
    })
    return request(`/comics?${q}`)
  },

  getComic(id) {
    return request(`/comics/${id}`)
  },

  getCoverUrl(id) {
    return `${BASE}/comics/${id}/cover`
  },

  getPageUrl(id, num, width = 150) {
    return `${BASE}/comics/${id}/page/${num}?width=${width}`
  },

  setRating(id, rating) {
    return request(`/comics/${id}/rating?rating=${rating}`, { method: 'POST' })
  },

  getTags() {
    return request('/tags')
  },

  startScan() {
    return fetch(`${BASE}/scan`, { method: 'POST' })
  },

  getScanStatus() {
    return fetch(`${BASE}/scan/status`).then(r => r.json())
  },
}
