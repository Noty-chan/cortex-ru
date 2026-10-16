import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'ru-RU',
  title: 'Cortex на русском',
  description: 'Книга правил: перевод, поиск, закладки и чтение с телефона',
  base: process.env.SITE_BASE || '/',
  cleanUrls: true,
  lastUpdated: true,
  themeConfig: {
    nav: [
      { text: 'Книга', link: '/contents' },
      { text: 'Моё чтение', link: '/reader' },
      { text: 'Глоссарий', link: '/glossary' },
    ],
    sidebar: [
      { text: 'Книга', items: [
        { text: 'Начало', link: '/' },
        { text: 'Оглавление', link: '/contents' },
        { text: 'Глоссарий', link: '/glossary' },
      ] },
      { text: 'Читателю', items: [
        { text: 'Моё чтение', link: '/reader' },
        { text: 'О переводе', link: '/about' },
      ] },
    ],
    search: {
      provider: 'local',
      options: { locales: { root: { translations: {
        button: { buttonText: 'Поиск', buttonAriaLabel: 'Поиск по книге' },
        modal: {
          noResultsText: 'Ничего не найдено',
          resetButtonTitle: 'Очистить поиск',
          displayDetails: 'Показать подробности',
          footer: { selectText: 'выбрать', navigateText: 'перейти', closeText: 'закрыть' },
        },
      } } } },
    },
    outline: { label: 'В этом разделе', level: [2, 3] },
    docFooter: { prev: 'Предыдущий раздел', next: 'Следующий раздел' },
    lastUpdated: { text: 'Обновлено' },
    sidebarMenuLabel: 'Разделы книги',
    returnToTopLabel: 'К началу',
    darkModeSwitchLabel: 'Тема оформления',
    lightModeSwitchTitle: 'Светлая тема',
    darkModeSwitchTitle: 'Тёмная тема',
    socialLinks: [{ icon: 'github', link: 'https://github.com/Noty-chan/cortex-ru' }],
  },
})
