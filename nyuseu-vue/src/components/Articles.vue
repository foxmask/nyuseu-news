<template>
<div>
  <div v-if="articles" class="row row-cols-3 row-cols-md-3">
    <template v-for="article in articles">
    <div class="card-deck mb-4" :key="article.id">
      <div class="card">
        <router-link :to="{ name: 'article', params: { articleId: article.id }}" v-html="article.image"></router-link>
        <div v-if="article.read" class="card-body text-muted">
          <h5 class="card-title">
          <router-link :to="{ name: 'article', params: { articleId: article.id }}" title="View the complete article">{{ article.title }}</router-link>
          </h5>
          <h6 class="card-subtitle mb-2 text-muted">{{ article.date_created }}</h6>
          <p class="card-text" v-html="article.text"></p>
        </div>
        <div v-else class="card-body">
          <h5 class="card-title">
          <router-link :to="{ name: 'article', params: { articleId: article.id }}" title="View the complete article">{{ article.title }}</router-link>
          </h5>
          <h6 class="card-subtitle mb-2 text-muted">{{ article.date_created }}</h6>
          <p class="card-text" v-html="article.text"></p>
        </div>
        <article-footer :article="Object.assign({}, article)" />
      </div>
    </div>
    </template>
  </div>
  <div v-if="loading" class="loading">
    Loading...
  </div>

  <div v-if="error" class="error">
    {{ error }}
  </div>  
</div>
</template>

<script>
import axios from 'axios'

import ArticleFooter from './ArticleFooter'

export default {
  name: "Articles",
  components: {
    ArticleFooter
  },
  data () {
    return {
      articles: [],
      loading: false,
      error: null      
    }
  },
  created () {
    // fetch the data when the view is created and the data is already being observed
    this.fetchData()
  },
  watch: {
    // call again the method if the route changes
    '$route': 'fetchData'
  },
  methods: {
    getArticles(feedId) {
      axios
      .get('/api/nyuseu/feeds/' + feedId + '/articles')
      .then(response => {this.articles = response.data})   
    },
    fetchData () {
      if (this.feedId) {
        this.articles = []
        this.error = null
        this.loading = true

        this.getArticles(this.feedId, (err, articles) => {        
          this.loading = false
          
          if (err) {
            this.error = err.toString()
          } else {
            this.articles = articles
          }

        })
      }
    }
  }, 
  mounted () {
    // get the articles from a given feed
    if (this.feedId) {
      axios
      .get('/api/nyuseu/feeds/' + this.feedId + '/articles')
      .then(response => {this.articles = response.data})
    } 
    // get all the articles
    else {
      axios
      .get('/api/nyuseu/articles/')
      .then(response => {this.articles = response.data})
    }
  },
  filters: {
    truncate (value,  length,  suffix)  {
      if  (value.length  >  length)  {
        value = value.substring(0,  length)  +  suffix;
      }   
      return  value;
    }
  },
  computed: {
    // get the feedId from the router
    feedId () {
      if (this.$route.params.feedId) {
        return this.$route.params.feedId
      }
      else {
        return 0
      }
    }
  }  
}
</script>
