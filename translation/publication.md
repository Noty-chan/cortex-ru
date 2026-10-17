# Публикация GitHub Pages

Пользователь17.10.2026прямо разрешил открыть Noty-chan/cortex-ruиопубликовать читалку.

- URL: https://noty-chan.github.io/cortex-ru/
- Workflow: .github/workflows/deploy.yml, каждыйpushвmainилиручнойзапуск.
- Сборка: npm ci; SITE_BASE=/cortex-ru/ npm run build.
- Артефакт: только book/.vitepress/dist.
- Локальная проверка готового сайта: python translation/tools/check_site.py --base /cortex-ru/.
- Фактические результаты включения Pages, запуска Actions и HTTP-проверок дописываются после выполнения; наличие этого файла само по себе не подтверждает публикацию.
