export const useToasts = defineStore("toasts", () => {
  const toasts = ref<Toast[]>([])

  const success = (text: string) => {
    toasts.value.push({ text, color: "success" })
  }
  const warning = (text: string) => {
    toasts.value.push({ text, color: "warning" })
  }
  const error = (text: string) => {
    toasts.value.push({ text, color: "error" })
  }

  return { toasts, error, success, warning }
})
