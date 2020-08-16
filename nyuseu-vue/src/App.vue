<template>
  <div id="app">
    <SideBar />
    <div v-if="articleId">
      <Article />
    </div>
    <div v-else>
      <Articles />
    </div>
  </div>
</template>

<script>
//import axios from 'axios'
import Articles from  './components/Articles.vue'
import Article from  './components/Article.vue'
import SideBar from './components/SideBar.vue'

export default {
  name: 'App',
  components: {
    Article,
    Articles,
    SideBar
  },
  computed: {
    articleId () {
      if (this.$route.params.articleId) {
        return this.$route.params.articleId
      }
      else {
        return 0
      }
    }
  }   
}
</script>

