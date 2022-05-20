<template>
  <div class="page">
    <div class="search-section">
      <div class="search">
        <div class="head-search">
          <div class="main-title">
            <div class="title-and-image">
              <div>
                <img src="../static/images/mortarboard.png" width="50" />
              </div>
              <div @click="gotohome()" class="only-title">
                Les Organismes de Formation
              </div>
            </div>
          </div>
          <div class="search-wrapper">
            <div>
              <input class="input-text" type="text" v-model="search" placeholder="Retrouver toutes les informations publiques concernant les organismes de formation" v-on:keyup.enter="searchText()"/>
            </div>
            <div class="search-button">
              <div class="image-search-button" @click="searchText()">
                <img src="../static/images/magnifying-glass.png" width="20" />
              </div>
            </div>
          </div>
        </div>
      </div>
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
  name: 'HeadSearch',
  mixins: [],
  components:{
  },
  data(){
    return {
      result: undefined,
      search: '',
      lastSearch: '',
      countResult: 0,
      maxpage: 0,
      page: 1,
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
    this.search = this.$route.params.search
    this.lastSearch = this.search
    this.$emit('lastsearch', this.lastSearch)
    console.log(this.search)
    if(this.$route.params.page){
      this.page = this.$route.params.page
      this.$emit('page', this.page)
    }
    //this.searchText();
    this.runSql();
  },
  methods: {
    searchNewPage(url){

    },
    searchText(){
      this.$router.push('/recherche/'+this.search+'/page/1').catch(() => {});
      this.runSql();
    },
    async runSql() {
      let offset = (this.page - 1) * 10
      let searchSql = "SELECT * FROM search WHERE search MATCH '" + this.search + "*' LIMIT 10 OFFSET "+ offset
      let countSql = "SELECT COUNT(*) as count FROM search WHERE search MATCH '" + this.search + "*'"
      this.result = await this.worker.db.query(searchSql);
      let resultCount = await this.worker.db.query(countSql);
      this.countResult = resultCount[0].count
      this.maxpage = parseInt(this.countResult / 10 + 1)
      console.log(this.maxpage)
      this.$emit('result', this.result)
      this.$emit('countresult', this.countResult)
      this.$emit('maxpage', this.maxpage)
      this.$emit('searchtext')
    },
    previouspage(){
      let newpage = parseInt(this.page) - 1
      this.$router.push('/recherche/'+this.search+'/page/'+newpage);
      this.page = newpage
      this.$emit('page', this.page)
      this.runSql()
    },
    nextpage(){
      let newpage = parseInt(this.page) + 1
      this.$router.push('/recherche/'+this.search+'/page/'+newpage);
      this.page = newpage
      this.$emit('page', this.page)
      this.runSql()
    },
    gotohome(){
       this.$router.push('/').catch(() => {});
    }
  },
  watch:{
  },
  created(){
  },
}
</script>

<style scoped lang="scss">

@import "../../css/custom.css";


@media screen and (max-width: 1100px) {

  .input-text{
    min-width: 300px;
  }
    
}

@media screen and (min-width: 1100px) {
  .head-search{
    display: flex;
  }
  .input-text{
    min-width: 500px;
  }
}

.head-search{
  padding-top: 20px;
  vertical-align: auto;
  max-width: 1000px;
  margin: auto;
  margin-bottom: 20px;
}

.search{
  padding-left: 10px;
}

.main-title{
  font-size: 25px;
  font-family: arial,sans-serif;
  font-style: italic;
  color: #444444
}

.search-wrapper{
  line-height: 50px;
  padding-left: 40px;
    display: flex;
}

.input-text{
  border-top-left-radius: 7px;
  border-top: none;
  border-left: none;
  border-right: none;
  background-color: #F0F0F0;
  border-bottom-color: #365E7C;
  height: 25px;
  font-style: italic;
  padding-left: 10px;
}

.search-button{
  border: none;
}

.image-search-button{
  padding-left: 5px;
  padding-right: 5px;
  line-height: 40px;
  margin-top: 12px;
  height: 30px;
  border: none;
  background-color: #365E7C;
}

.search-section{
  border-bottom: 1px solid #999999;
}

.results{
  max-width: 1000px;
  margin: auto;
  margin-top: 20px;
  padding-left: 20px;
}

.title-and-image{
  display: flex;
}

.only-title{
  cursor: pointer;
  padding-left: 10px;
  line-height: 50px;;
}

</style>