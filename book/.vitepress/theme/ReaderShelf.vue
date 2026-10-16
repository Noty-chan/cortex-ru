<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { BOOKMARKS, LAST, load, save, type Place } from './reading'
const bookmarks = ref<Place[]>([])
const last = ref<Place | null>(null)
const ready = ref(false)
const error = ref('')
function refresh() {
  bookmarks.value = load<Place[]>(BOOKMARKS, [])
  last.value = load<Place | null>(LAST, null)
}
function remove(url: string) {
  const next = bookmarks.value.filter(i => i.url !== url)
  if (save(BOOKMARKS, next)) bookmarks.value = next
  else error.value = 'Браузер не разрешил изменить закладки'
}
onMounted(() => { refresh(); ready.value = true; window.addEventListener('storage', refresh) })
onUnmounted(() => window.removeEventListener('storage', refresh))
</script>

<template>
  <div v-if="ready" class="reader-shelf">
    <h2>Продолжить чтение</h2>
    <p v-if="last"><a :href="last.url">{{ last.title }} →</a></p>
    <p v-else>Открой раздел книги — последнее место чтения сохранится здесь.</p>
    <h2>Мои закладки</h2>
    <ul v-if="bookmarks.length" class="bookmark-list">
      <li v-for="item in bookmarks" :key="item.url">
        <a :href="item.url">{{ item.title }}</a>
        <button type="button" :aria-label="`Удалить закладку: ${item.title}`" @click="remove(item.url)">Удалить</button>
      </li>
    </ul>
    <p v-else>Закладок пока нет. Добавляй их кнопкой «В закладки» в начале раздела.</p>
    <p role="status">{{ error }}</p>
    <p class="reader-note">Сохранено в этом браузере. При очистке данных сайта закладки удалятся.</p>
  </div>
  <p v-else>Загружаем твоё чтение…</p>
</template>
