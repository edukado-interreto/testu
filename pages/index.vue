<template>
  <div>
    <v-navigation-drawer
      app
      right
      bottom
      clipped
      v-model="drawer"
      :mini-variant.sync="mini"
    >
      <v-list-item dense v-if="!$vuetify.breakpoint.mobile">
        <v-btn @click.stop="mini = !mini" icon><v-icon>mdi-chevron-{{ mini ? 'left' : 'right' }}</v-icon></v-btn>
      </v-list-item>
      <v-container v-show="!mini">
        <p>
        Elit vero incidunt ad at natus Quos facilis quae exercitationem earum tempore beatae? Odit molestiae veniam voluptatum error neque! Blanditiis quibusdam odio magni aliquam quaerat? Ipsum laborum quia accusamus ipsam temporibus deserunt! Facilis totam hic amet eum porro, libero. Ducimus nihil eos rem corporis tenetur Quod officia voluptatibus ipsum vel sed pariatur? Quaerat quaerat debitis alias odit rerum, at nobis nobis exercitationem Possimus voluptatibus officiis at repudiandae vero? Voluptatem voluptate beatae possimus deleniti aut alias Ipsam pariatur corporis assumenda consequatur soluta harum tempore ea Facilis sapiente natus inventore voluptatum voluptatibus Sequi natus placeat ut natus neque dignissimos odit Fuga in deleniti cumque eos aut Mollitia repudiandae accusamus dignissimos labore neque quidem! Minima aut maiores dolorum maiores reprehenderit est quibusdam assumenda? Quasi eius voluptatem quo soluta esse labore itaque culpa? Error quia perferendis est error maxime Suscipit accusamus labore dignissimos voluptas autem quis. Provident nihil ullam quidem iusto nobis obcaecati Ea quos molestiae vero odio sequi maiores vitae modi consectetur Aliquid temporibus aut mollitia quibusdam quod voluptatum Dolor cum eos similique exercitationem deserunt Nobis ipsam ad quis deserunt corrupti. Blanditiis ab accusamus eligendi eum dicta facere commodi deserunt nesciunt Porro expedita optio rem pariatur consequatur? Est dolor eligendi ducimus assumenda corrupti Vel vero tenetur laboriosam veritatis reiciendis. Quisquam earum sunt velit hic quae. Ipsum iusto numquam iusto quidem nostrum odit corrupti Odio cupiditate sed doloribus ducimus id nostrum A quibusdam sit aut dicta est voluptatum blanditiis quos! Molestiae autem adipisci quisquam sapiente optio. Soluta a officia cumque sed ex Accusamus porro non harum consequatur harum. Eum enim reprehenderit debitis enim recusandae. Laborum aperiam eum minima placeat et qui. Autem atque quod aut vero dolorum. Quo quae harum et facilis ipsa Rem provident quibusdam neque dolorem ducimus fuga in Cupiditate aut nam totam non deserunt ratione! Dolorem aliquid itaque odit sapiente fugit. Molestiae temporibus veritatis dolore itaque dignissimos? Culpa laudantium perspiciatis temporibus inventore labore distinctio accusamus Ratione ipsam ex saepe praesentium praesentium? Magnam ipsa quaerat commodi perferendis magnam dolorum Esse rerum soluta rem odio impedit. Fugit dolorum nemo perspiciatis inventore culpa nam, nemo Non quas sed aspernatur iure unde perspiciatis Dicta recusandae illo consequatur doloremque et aperiam. Culpa odit culpa dolore labore dolorem a Ab itaque dignissimos harum at modi Ratione quisquam dolor a quae possimus illum? Minus nihil fugit reiciendis quisquam eum? Tempora accusamus aspernatur quas eos sunt. Magni illum quaerat eos deleniti quis Laborum nam vero explicabo velit deserunt. At?
        </p>
      </v-container>
    </v-navigation-drawer>
    <v-container>
      <v-card>
        <v-card-title class="headline">
          Editor
        </v-card-title>
        <v-card-text>
          <GapsEditor />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="primary"
            nuxt
            to="/inspire"
          >
            Publish
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
  </div>
</template>
<script>
  export default {
    methods: {
    },
    data: () => ({
      mini: false,
      drawer: true,
    })
  }
</script>
