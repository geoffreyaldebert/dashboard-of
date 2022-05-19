<template>
  <div class="homepage">
    coucou
    <h1>L'annuaire des Organismes de Formation</h1>
    <h2>Retrouvez toutes les informations publiques concernant les organismes français</h2>
    <div class="search-wrapper">
      <input type="text" v-model="search" placeholder="Search title.." v-on:keyup.enter="searchText()"/>
      <button @click="searchText()">Rechercher</button>
    </div>
    <div v-if="result">{{ result.length}} résultats</div>
    <div>
      <div v-bind:key="res.numeroDeclarationActivite" v-for="res in result">
        {{ res.denomination}}
        <br />
      </div>
    </div>
    <pre>{{ result }}</pre>
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
  name: 'HomepageWidget',
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
    console.log('test')
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
  },
  methods: {
    searchText(){
      //this.runSql("SELECT * FROM list_of WHERE denomination LIKE '" + this.search + "%' limit 10")
      this.runSql("SELECT * FROM search WHERE search MATCH '" + this.search + "' LIMIT 10")
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