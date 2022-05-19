<template>
  <div class="homepage">
      Résultat
      <br />
      <div v-bind:key="res.numeroDeclarationActivite" v-for="res in result">
        {{ res.denomination }}
        <br />
        <br />
        <pre>{{ res }}</pre>
        <br />
      </div>
  </div>
</template>

<script>
import { createDbWorker } from "sql.js-httpvfs";

const publicPath =
  process.env.NODE_ENV === "production" ? "/" : "/";

const workerUrl = new URL(
  `${publicPath}sql.js-httpvfs/sqlite.worker.js`,
  import.meta.url
);
const wasmUrl = new URL(
  `${publicPath}sql.js-httpvfs/sql-wasm.wasm`,
  import.meta.url
);

export default {
  name: 'Test',
  mixins: [],
  components:{
  },
  data(){
    return {
      result: undefined,
      columns: ['denomination','siren',''],
      id: ''
    }
  },
  props: {
  },
  computed: {
  },
  async mounted() {
    this.worker = await createDbWorker(
      [
        {
          from: "inline",
          config: {
            serverMode: "full",
            url: `${publicPath}db/of.sqlite`,
            requestChunkSize: 4096,
          },
        },
      ],
      workerUrl.toString(),
      wasmUrl.toString()
    );
    this.id = this.$route.query.id
    this.searchText();
  },
  methods: {
    searchText(){
      this.runSql("SELECT * FROM complete WHERE numeroDeclarationActivite = '" + this.id + "' LIMIT 1")
    },
    async runSql(sql) {
      this.result = await this.worker.db.query(sql);
    },
  },
  watch:{
  },
  created(){
  },


}
</script>

<style scoped lang="scss">

@import "../../css/custom.css";

</style>