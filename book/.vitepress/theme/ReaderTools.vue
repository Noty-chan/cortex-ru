<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useData, useRoute, withBase } from 'vitepress'
import { BOOKMARKS, LAST, load, save, type Place } from './reading'

const { page } = useData()
const route = useRoute()
const message = ref('')
let timer: ReturnType<typeof setTimeout> | undefined
function place(): Place {
  const headings = Array.from(document.querySelectorAll<HTMLElement>('.vp-doc h2[id], .vp-doc h3[id]'))
  const heading = headings.filter(h => h.getBoundingClientRect().top < innerHeight * 0.4).at(-1)
  const title = page.value.title || 'Cortex на русском'
  const section = heading?.textContent?.replace(/\s*#\s*$/, '').trim()
  return {
    url: location.pathname + (heading ? '#' + encodeURIComponent(heading.id) : ''),
    title: section ? `${title} · ${section}` : title,
    time: Date.now(),
  }
}
function remember() {
  if (page.value.relativePath === 'reader.md' || page.value.relativePath === 'index.md') return
  save(LAST, place())
}
function scroll() {
  if (timer) clearTimeout(timer)
  timer = setTimeout(remember, 250)
}
function bookmark() {
  const current = place()
  const items = load<Place[]>(BOOKMARKS, [])
  const exists = items.some(i => i.url === current.url)
  const ok = save(BOOKMARKS, [current, ...items.filter(i => i.url !== current.url)])
  message.value = ok ? (exists ? 'Закладка обновлена' : 'Закладка сохранена') : 'Браузер не разрешил сохранить закладку'
}
watch(() => route.path, async () => {
  message.value = ''
  await nextTick()
  // The route renderer restores anchor position after navigation.
  if (timer) clearTimeout(timer)
  timer = setTimeout(remember, 500)
})
onMounted(() => {
  timer = setTimeout(remember, 500)
  window.addEventListener('scroll', scroll, { passive: true })
  window.addEventListener('pagehide', remember)
})
onUnmounted(() => {
  if (timer) clearTimeout(timer)
  window.removeEventListener('scroll', scroll)
  window.removeEventListener('pagehide', remember)
})
</script>

<template>
  <div v-if="page.relativePath !== 'reader.md'" class="reader-tools">
    <button type="button" @click="bookmark">☆ В закладки</button>
    <a :href="withBase('/reader')">Моё чтение →</a>
    <span role="status" aria-live="polite">{{ message }}</span>
  </div>
</template>
