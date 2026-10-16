import DefaultTheme from 'vitepress/theme'
import { h } from 'vue'
import ReaderTools from './ReaderTools.vue'
import ReaderShelf from './ReaderShelf.vue'
import './style.css'

export default {
  extends: DefaultTheme,
  Layout: () => h(DefaultTheme.Layout, null, { 'doc-before': () => h(ReaderTools) }),
  enhanceApp({ app }) { app.component('ReaderShelf', ReaderShelf) },
}
