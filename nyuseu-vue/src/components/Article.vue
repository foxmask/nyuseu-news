<template>
<b-col offset-md="1" md="0" lg="10" xs="10">
  <div v-if="article" class="col mb-4">
  <b-card-group deck>
    <b-card>
      <span v-html="article.image"></span>
      <b-card-body>
        <h5 class="card-title">{{ article.title }}</h5>
        <h6 class="card-subtitle mb-2 text-muted">{{ article.date_created }}</h6>
        <p class="card-text" v-html="article.text"></p>
      </b-card-body>
      <article-footer :article="Object.assign({}, article)" />
    </b-card>
  </b-card-group>
  </div>
  <div v-if="loading" class="loading">
    Loading...
  </div>

  <div v-if="error" class="error">
    {{ error }}
  </div>  
</b-col>
</template>

<script>
import axios from 'axios'
import ArticleFooter from './ArticleFooter'

export default {
  name: "Article",
  components: {
    ArticleFooter
  },
  data ()  {
    return { 
      article: Object,
      loading: null,
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
    getArticle(articleId) {
      axios
      .get('/api/nyuseu/articles/' + articleId)
      .then(response => {this.article = response.data})   
    },    
    fetchData () {
      if (this.$route.params.articleId) {
        this.article = null
        this.error = null
        this.loading = true

        this.getArticle(this.$route.params.articleId, (err, article) => {        
          this.loading = false
          
          if (err) {
            this.error = err.toString()
          } else {
            this.article = article
          }

        })
      }
    }
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
