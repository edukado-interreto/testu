declare global {
  /* App */
  type VueElement = { [k: string]: Element | ComponentPublicInstance | null }

  /* Auth */
  type User = {
    id: number
    username: string
    email: string
    date_joined: string | Date
    data: { [k: string]: string }
  }

  type LoginCredential = {
    email: string
    password: string
  }

  type LoginResponse = {
    access: string
    refresh: string
    user: User
  }

  /* Models */

  type UnitType = "default" | "open_answer" | "multiple_choice" | "pairing"

  type Cefr = "A1" | "A2" | "B1" | "B2" | "C1" | "C2"

  type Exercise = {
    _key: string
    id: number
    lid: string
    age_min: number
    age_max: number
    created_by: string
    modified: string
    description: string
    name: string
    searchable: boolean
    lang_learn: boolean
    lang_learn_lang: string
    lang_learn_cefr_level_min: number
    lang_learn_cefr_level_max: number
    likes: number
    tags: string[]
    data: {
      sheet: Unit[]
    }
  }

  type DRF<T> = {
    previous: string | null
    next: string | null
    count: number
    results: T[]
  }

  type Unit = {
    _key: string
    code: string
    description: string
    shuffle: boolean
    ignore_case: boolean
    title: string
    type: UnitType
  }

  type Submission = {
    pk: number
    created: Date
    exercise_lid: string
    exam_lid: string | null
    exercise: Exercise
    guest?: string
    data: object
    score: number
  }

  type Option = {
    value?: string
    right?: boolean
    answer?: string
  }

  type Token = {
    token?: string
    options?: Option[]
    value?: string
    right?: boolean
    answer?: string
    errorExplanation?: string
  }

  type MsgBoxOptions = {
    buttons?: {
      value: boolean
      text: string
    }[]
    color?: string
    icon?: string
    max_width?: number
    modal?: boolean
    text?: string
    title?: string
  }
}

declare module "nuxt/schema" {
  interface PublicRuntimeConfig {
    apiBase: string
  }
}

export {}
