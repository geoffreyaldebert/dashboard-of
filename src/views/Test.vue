<template>
  <div class="homepage">
      To
      {{ result }}
      <div v-bind:key="res.numeroDeclarationActivite" v-for="res in result">
        {{ res }}
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
      search: '',
      columns: ['denomination','siren','']
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
    this.search = 'world'
    this.searchText();
  },
  methods: {
    searchText(){
      this.runSql("SELECT * FROM complete WHERE siretEtablissementDeclarant = '40100010400034' LIMIT 1")
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