type RefArray = Ref<string[] | number[]>
type RefAny = Ref<string | number | object> | RefArray

export const non_empty = (ref_array: Ref<unknown[]>) => ref_array.value.length > 0

export const or_undefined = (ref_var: RefAny) => {
  if (Array.isArray(ref_var.value)) {
    return non_empty(ref_var as RefArray) ? ref_var.value : undefined
  }
  return ref_var.value ? ref_var.value : undefined
}
