<template>
  <div class="page">
    <head-search
      v-on:search="searchEvent"
      v-on:lastsearch="lastsearchEvent"
      v-on:result="resultEvent"
      v-on:countresult="countResultEvent"
      v-on:maxpage="maxpageEvent"
      v-on:page="pageEvent"
      v-on:searchtext="searchText"
      ref="headsearch"
    ></head-search>
    <div class="resultPage">
      <div class="results">
        <div>{{ countResult }} résultats trouvés pour <b><i>{{ lastSearch }}</i></b>. </div>
        <br />
        <div class="nextprevious">
          <div v-if="this.countResult" class="actual-page">Page {{ this.page }}</div>
          <div v-if="this.page >= 2" @click="previouspage()" class="page-precedente">Page précédente</div>
          <div v-if="parseInt(this.page) < parseInt(this.maxpage)" @click="nextpage()" class="page-suivante">Page suivante</div>
        </div>
        <br />
        <div>
          <div v-bind:key="res.numeroDeclarationActivite" v-for="res in result">
            <a class="result-link" href="" @click="goto(res.id) ">{{ res.denomination.toLowerCase().split(' ').map((s) => s.charAt(0).toUpperCase() + s.substring(1)).join(' ') }}</a>
            <br />
            <br />
          </div>
          <br />
        </div>
      </div>
      <div v-if="boxvisibility" class="boxInfo">
        <div class="crossbox" @click="closeBox()"><img src="../static/images/close.png" width="10" /></div>
        <div class="textbox"><b><i>D'où proviennent ces données ?</i></b><br /><br /><i>Ces données proviennent directement des données <a href="https://www.data.gouv.fr/fr/datasets/liste-publique-des-organismes-de-formation-l-6351-7-1-du-code-du-travail/">publiées en open data</a> par le ministère du travail.</i></div>
      </div>
    </div>
  </div>
</template>

<script>
import HeadSearch from '../components/HeadSearch.vue';

export default {
  name: 'Search',
  mixins: [],
  components:{
      HeadSearch
  },
  data(){
    return {
      result: undefined,
      search: '',
      lastSearch: '',
      countResult: 0,
      maxpage: 0,
      page: 1,
      boxvisibility: true,
      columns: ['denomination','siren','']
    }
  },
  props: {
  },
  computed: {
  },
  mounted() {
    
  },
  methods: {
    lastsearchEvent(res){
      this.lastSearch = res;
    },
    resultEvent(res){
      this.result = res;
    },
    pageEvent(res){
      this.page = res;
    },
    searchEvent(res){
      this.search = res;
    },
    maxpageEvent(res){
      this.maxpage = res;
    },
    countResultEvent(res){
      this.countResult = res;
    },
    searchText(){
      console.log('search')
      console.log(this.search)
    },
    goto(id){
      this.$router.push('/organisme/'+id);
    },
    previouspage(){
      this.$refs.headsearch.previouspage()
    },
    nextpage(){
      this.$refs.headsearch.nextpage()
    },
    closeBox(){
      console.log('close')
      this.boxvisibility = false;
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
  .boxInfo{
    visibility: hidden;
  }

}

@media screen and (min-width: 1100px) {

}


.head-search{
  padding-top: 20px;
  display: flex;
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
  min-width: 500px;
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

.boxInfo{
  width: 350px;
  height: 150px;
  position: absolute;
  top: 150px; right: 15%;
  background-color: #FFE07D;
  border-radius: 10px;
}

.title-and-image{
  display: flex;
}

.only-title{
  padding-left: 10px;
  line-height: 50px;;
}

.result-link{
  color: #365E7C;
  text-decoration: none;
  font-size: 18px;
}

.result-link:hover{
  text-decoration: underline;
  cursor: pointer;
}

.page-suivante{
  line-height: 30px;
  border-radius: 10px;
  padding-left: 10px;
  padding-right: 10px;
  background-color: #477C9E;
  color: white;
  cursor: pointer;
}
.page-precedente{
  margin-right: 20px;
  line-height: 30px;
  border-radius: 10px;
  padding-left: 10px;
  padding-right: 10px;
  background-color: #477C9E;
  color: white;
  cursor: pointer;
}

.actual-page{
  margin-right: 20px;
  line-height: 30px;
  border-radius: 10px;
  padding-left: 10px;
  padding-right: 10px;
  background-color: #FFE07D;
  border-radius: 10px;
  color: black;
}
.page-suivante:hover{
  background-color: #365E7C;
}
.page-precedente:hover{
  background-color: #365E7C;
}


.nextprevious{
  display: flex;
}

.crossbox{
  margin-left: 10px;
  margin-top: 10px;
  cursor: pointer;
}
.textbox{
  padding: 10px;
}

</style>