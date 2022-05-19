<template>
  <div class="homepage">
      Coucou
      <pre>{{ JSON.stringify(result, null, 2) }}</pre>
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
            url: `${publicPath}db/of.db`,
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
      this.runSql("SELECT * FROM mytable WHERE denomination LIKE '%"+this.search+"%' LIMIT 20")
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