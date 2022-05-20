<template>
  <div class="homepage">
      <head-search
        v-on:search="searchEvent"
        v-on:result="resultEvent"
        ref="headsearch"
      ></head-search>

      <div v-if="showWheel"><br >/<img src="../static/images/S2Ra.gif" width="250" /></div>
      <div class="organismeDetail" v-bind:key="res.numeroDeclarationActivite" v-for="res in result">
        <div class="nomOrganisme">{{ res.denomination.toLowerCase().split(' ').map((s) => s.charAt(0).toUpperCase() + s.substring(1)).join(' ') }}</div>
        <br />

        <div class="infoGenerales">
          <div class="infosFormationTitle">Informations sur les formations</div>
          <br/>
          <div class="boxProperties" v-if="res['informationsDeclarees.specialitesDeFormation.libelleSpecialite1']">
            <div class="nameproperty">Libellé de la spécialité 1</div>
            <div class="property">{{ res['informationsDeclarees.specialitesDeFormation.libelleSpecialite1'] }}</div>
          </div>
          <div class="boxProperties" v-if="res['informationsDeclarees.specialitesDeFormation.libelleSpecialite2']">
            <div class="nameproperty">Libellé de la spécialité 2</div>
            <div class="property">{{ res['informationsDeclarees.specialitesDeFormation.libelleSpecialite2'] }}</div>
          </div>
          <div class="boxProperties" v-if="res['informationsDeclarees.specialitesDeFormation.libelleSpecialite3']">
            <div class="nameproperty">Libellé de la spécialité 3</div>
            <div class="property">{{ res['informationsDeclarees.specialitesDeFormation.libelleSpecialite3'] }}</div>
          </div>
          <div class="boxProperties" v-if="res['informationsDeclarees.effectifFormateurs']">
            <div class="nameproperty">Effectifs Formateurs</div>
            <div class="property">{{ res['informationsDeclarees.effectifFormateurs'] }}</div>
          </div>
          <div class="boxProperties" v-if="res['informationsDeclarees.nbStagiaires']">
            <div class="nameproperty">Stagiaires</div>
            <div class="property">{{ res['informationsDeclarees.nbStagiaires'] }}</div>
          </div>
          <div class="boxProperties" v-if="res['informationsDeclarees.nbStagiairesConfiesParUnAutreOF']">
            <div class="nameproperty">Stagiaires confiés par un autre organisme</div>
            <div class="property">{{ res['informationsDeclarees.nbStagiairesConfiesParUnAutreOF'] }}</div>
          </div>
          <br/>
        </div>
        <br />

        <div class="infoGenerales">
          <div class="infosCertificationTitle">Certifications / Qualiopi</div>
          <br/>
          <div class="boxProperties">
            <div class="nameproperty">Actions de Formation</div>
            <div class="property">
              <span v-if="res['certifications.actionsDeFormation'] == 'true'">
                Oui
              </span>
              <span v-else-if="res['certifications.actionsDeFormation'] == 'false'">
                Non
              </span>
              <span v-else-if="!res['certifications.actionsDeFormation']">
                Non renseigné
              </span>
            </div>
          </div>
          <div class="boxProperties">
            <div class="nameproperty">Bilans de Compétences</div>
            <div class="property">
              <span v-if="res['certifications.bilansDeCompetences'] == 'true'">
                Oui
              </span>
              <span v-else-if="res['certifications.bilansDeCompetences'] == 'false'">
                Non
              </span>
              <span v-else-if="!res['certifications.bilansDeCompetences']">
                Non renseigné
              </span>
            </div>
          </div>
          <div class="boxProperties">
            <div class="nameproperty">Validation des acquis de l'expérience (VAE)</div>
            <div class="property">
              <span v-if="res['certifications.VAE'] == 'true'">
                Oui
              </span>
              <span v-else-if="res['certifications.VAE'] == 'false'">
                Non
              </span>
              <span v-else-if="!res['certifications.VAE']">
                Non renseigné
              </span>
            </div>
          </div>
          <div class="boxProperties">
            <div class="nameproperty">Actions de Formations par Apprentissage</div>
            <div class="property">
              <span v-if="res['certifications.actionsDeFormationParApprentissage'] == 'true'">
                Oui
              </span>
              <span v-else-if="res['certifications.actionsDeFormationParApprentissage'] == 'false'">
                Non
              </span>
              <span v-else-if="!res['certifications.actionsDeFormationParApprentissage']">
                Non renseigné
              </span>
            </div>
          </div>
          <br/>
          <div><i>La marque « Qualiopi » est délivrée par des organismes certificateurs accrédités ou autorisés par le Comité français d’accréditation (Cofrac) sur la base du référentiel national qualité.</i></div>
        </div>
        <br />

        <div class="infoGenerales">
          <div class="infosGeneralesTitle">Informations sur l'entreprise</div>
          <br/>
          <div class="boxProperties" v-if="res.denomination">
            <div class="nameproperty">Dénomination</div>
            <div class="property">{{ res.denomination }}</div>
          </div>
          <div class="boxProperties" v-if="res.siren">
            <div class="nameproperty">SIREN</div>
            <div class="property">{{ res.siren }}</div>
          </div>
          <div class="boxProperties" v-if="res.siretEtablissementDeclarant">
            <div class="nameproperty">SIRET</div>
            <div class="property">{{ res.siretEtablissementDeclarant }}</div>
          </div>
          <div class="boxProperties" v-if="res.numeroDeclarationActivite">
            <div class="nameproperty">N° de Déclaration d'Activité</div>
            <div class="property">{{ res.numeroDeclarationActivite }}</div>
          </div>
          <div class="boxProperties" v-if="res['adressePhysiqueOrganismeFormation.voie']">
            <div class="nameproperty">Adresse</div>
            <div class="property">{{ res['adressePhysiqueOrganismeFormation.voie'] }}</div>
          </div>
          <div class="boxProperties" v-if="res['adressePhysiqueOrganismeFormation.codePostal']">
            <div class="nameproperty">Code Postal</div>
            <div class="property">{{ res['adressePhysiqueOrganismeFormation.codePostal'] }}</div>
          </div>
          <div class="boxProperties" v-if="res['adressePhysiqueOrganismeFormation.ville']">
            <div class="nameproperty">Ville</div>
            <div class="property">{{ res['adressePhysiqueOrganismeFormation.ville'] }}</div>
          </div>
          <div class="boxProperties" v-if="res['adressePhysiqueOrganismeFormation.codeRegion']">
            <div class="nameproperty">Région</div>
            <div class="property">{{ res['adressePhysiqueOrganismeFormation.codeRegion'] }}</div>
          </div>
          <div class="boxProperties" v-if="res['informationsDeclarees.dateDerniereDeclaration']">
            <div class="nameproperty">Date de dernière déclaration</div>
            <div class="property">{{ res['informationsDeclarees.dateDerniereDeclaration'] }}</div>
          </div>
          <br/>
          <div class="button-ae-div">
            <div @click="gotoae(res.siren)" class="button-ae">Plus d'informations sur le site<br />Annuaire des Entreprises</div>
          </div>
        </div>
        <br />
      </div>
  </div>
</template>

<script>
import HeadSearch from '../components/HeadSearch.vue';

export default {
  name: 'Organisme',
  mixins: [],
  components:{
    HeadSearch
  },
  data(){
    return {
      result: undefined,
      id: '',
      showWheel: true
    }
  },
  props: {
  },
  computed: {
  },
  async mounted() {
  },
  methods: {
    searchEvent(res){
      this.search = res;
    },
    resultEvent(res){
      this.result = res;
      this.showWheel = false;
    },
    gotoae(siren){
      window.location.href = 'https://annuaire-entreprises.data.gouv.fr/entreprise/'+siren
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


@media screen and (max-width: 1100px) {

}

@media screen and (min-width: 1100px) {
  .boxProperties{
    display: flex;
  }
  .nameproperty{
    width: 45%;
  }
  .property{
    width: 45%;    
  }
}

.organismeDetail{
  margin: auto;
  margin-top: 40px;
  max-width: 1000px;
  font-size: 18px;
}

.infoGenerales{
  border: 2px solid #365E7C;
  border-radius: 5px;
  margin-left: 10px;
  margin-right: 10px;
  padding: 10px;
}

.infosGeneralesTitle{
  padding: 5px;
  padding-left: 10px;
  width: 210px;
  background-color: #365E7C;
  border-radius: 5px;;
  color: white;
}

.nomOrganisme{
  font-size: 25px;
  margin-left: 10px;
}

.boxProperties{
  margin-top: 5px;
  padding-left: 10px;
  width: 100%;
}

.nameproperty{
  padding-top: 5px;
  padding-bottom: 5px;
  font-weight: bold;
  cursor: pointer;

}

.property{
  padding-top: 5px;
  padding-bottom: 5px;
  cursor: pointer;
}

.infosFormationTitle{
  padding: 5px;
  padding-left: 10px;
  width: 230px;
  background-color: #365E7C;
  border-radius: 5px;;
  color: white;
}

.infosCertificationTitle{
  padding: 5px;
  padding-left: 10px;
  width: 180px;
  background-color: #365E7C;
  border-radius: 5px;;
  color: white;
}

.button-ae{
  margin: auto;
  padding: 5px;
  padding-left: 10px;
  width: 250px;
  background-color: #365E7C;
  border-radius: 5px;;
  color: white;
  text-align: center;
  cursor: pointer;
}

</style>