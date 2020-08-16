<template>
<div>
  <b-btn v-b-toggle.sidebar>Sidebar Menu</b-btn>
  <b-sidebar id="sidebar" title="Nyuseu - 뇨스" shadow>
    <b-nav vertical>
      <b-nav-item href="/">
        <b-icon icon="cup-straw"></b-icon><span class="ml-2">All articles</span>
      </b-nav-item>
      <template v-for="folder in folders">
      <b-nav-item v-if="!folder.feeds" :key="folder.id">
        <b-icon icon="bar-chart-fill"></b-icon><span class="ml-2">{{ folder.title }} ({{ folder.unread }})</span>
      </b-nav-item>
      <b-nav-item v-if="folder.feeds"
                  :key="folder.id" 
                  link-classes="d-flex align-items-center"
                  @click="folder.isOpen = !folder.isOpen">
        <b-icon icon="play"></b-icon>
        <span class="ml-2">{{ folder.title }} ({{ folder.unread }})</span>
        <b-icon class="ml-auto" :icon="folder.isOpen ? 'chevron-up' : 'chevron-down'"></b-icon>
      </b-nav-item>
      <b-collapse v-if="folder.feeds"
                  :key="folder.id"
                  v-model="folder.isOpen"
                  :id="`collapse-folder-${folder.id}`"
                  tag="li">
        <b-nav-item v-for="{ id, title } in folder.feeds"
                  :key="id" 
                  :to="{ name: 'articlesByFeeds', params: {feedId: id }}">
          <span class="ml-2">{{ title }}</span>
        </b-nav-item>
      </b-collapse>
      </template>
    </b-nav>
  </b-sidebar>
</div>
</template>

<script>
import axios from 'axios'

export default {
  name: "SideBar",
  data () {
    return {
      folders: []
    }
  }, 
  mounted () {
    axios
    .get('/api/nyuseu/folders/')
    .then(response => {this.folders = response.data})
  }
}
</script>
