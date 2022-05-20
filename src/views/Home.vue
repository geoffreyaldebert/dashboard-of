<template>
  <div class="homepage">
    <div class="image-home">
        <img src="../static/images/mortarboard.png" width="150" />
    </div>
    <div class="title-home">
        Le moteur de recherche des<br />Organismes de Formation
    </div>
    <div class="search-box">
        <div class="head-search">
            <div class="search-wrapper">
            <div>
                <input class="input-text" type="text" v-model="search" placeholder="Rechercher un organisme de formation" v-on:keyup.enter="searchText()"/>
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
</template>

<script>


export default {
  name: 'Home',
  mixins: [],
  components:{
  },
  data(){
    return {
        search: ''
    }
  },
  props: {
  },
  computed: {
  },
  mounted() {
  },
  methods: {
    searchText(){
        this.$router.push('/recherche/'+this.search+'/page/1').catch(() => {});
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

.homepage{
    margin: auto;
    margin-top: 100px;
    max-width: 1000px;
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
  margin: auto;
  line-height: 50px;
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
  min-width: 250px;
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

.image-home{
    margin: auto;
    text-align: center;
}

.title-home{
    margin: auto;
    text-align: center;
    font-size: 40px;
}

.search-box{
    margin: auto;
    text-align: center;
}

</style>