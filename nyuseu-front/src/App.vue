<template>
  <div id="app">
    <b-container>
      <b-button v-b-toggle.sidebar-1><i>H</i></b-button>
      <b-sidebar id="sidebar-1" title="Folders" shadow>
        <div class="px-3 py-2">
          <folders></folders>
        </div>
      </b-sidebar>
      <b-row>
        <b-col></b-col>
        <b-col></b-col>
      </b-row>
      <b-nav>
        <b-nav-item active><router-link to="/">Home</router-link> |</b-nav-item>
        <b-nav-item><router-link to="/about">About</router-link></b-nav-item>
      </b-nav>
      <router-view/>
    </b-container>
  </div>
</template>

<script>
import Folders from '@/components/Folders.vue'
export default {
  components: { Folders },
  data () {
    return {
      folders: ''
    }
  }
}
</script>