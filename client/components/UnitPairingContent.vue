<template>
  <div>
    <template v-for="(t, i) in tokens">
      <span
        v-if="t.type == 'text'"
      >{{ t.content }}</span>
      <v-img
        v-if="t.type == 'img'"
        :src="`https://picsum.photos/seed/${t.content}/200/300`"
        contain
        max-height="150"
      ></v-img>
      <template
        v-if="t.type == 'video'"
      >
        <div v-if="t.invalid_url">
          <i>Invalid url: {{ t.content }}</i>
        </div>
        <iframe
          v-else
          style="max-height:150px; max-width:100%;"
          :src="t.embed_url"
          title="YouTube video player"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
        ></iframe>
      </template>
    </template>
  </div>
</template>
<script>
export default {
  name: 'UnitPairingContent.vue',
  props: ['text'],
  computed: {
    tokens() {
      return this.text.split(
        RegExp("{((?:img|video):[^}]+)}")
      ).map((t, i) => {
        if (i % 2 == 0) {
          return {
            type: 'text',
            content: t,
          }
        }
        const [type, content] = t.split(/:(.*)/)

        const ret = {
          type, content
        }

        if (type == 'video') {
          const id = this.get_youtube_id(content)
          if (id) {
            ret.embed_url = `https://www.youtube.com/embed/${id}`
          } else {
            ret.invalid_url = true
          }
        }

        return ret

      }).filter(
        t => t.content
      )
    }
  },
  methods: {
    get_youtube_id(url) {

      let id = (new URLSearchParams(
        url.replace(/^[^?]*/, "")
      )).get("v")
      if (id) return id

      id = url.match(/https?:\/\/youtu\.be\/(.*)/)?.[1]
      if (id) return id

      return null
    }
  }
}
</script>
