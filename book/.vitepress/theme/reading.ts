export type Place = { url: string; title: string; time: number }
export const BOOKMARKS = 'cortex-ru:bookmarks:v1'
export const LAST = 'cortex-ru:last:v1'
export function load<T>(key: string, fallback: T): T {
  try { return JSON.parse(localStorage.getItem(key) || 'null') ?? fallback }
  catch { return fallback }
}
export function save(key: string, value: unknown): boolean {
  try { localStorage.setItem(key, JSON.stringify(value)); return true }
  catch { return false }
}
