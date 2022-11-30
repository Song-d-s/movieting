<template>
  <div>
    <div id="title" class="d-flex" >
      <h3>{{ username }} 님이 작성한 리뷰</h3>
    </div>
    <br>
    <div id="rightSection" class="col-sm-12 col-md" style="text-align:left;">
      <div class="vstack gap-3 m-2">
        <div
          v-for="comment in comments"
          :key="comment.id">
          <div v-if="comment.is_survey==0" id="review-item" @click="goMovieDetail(comment)">
            {{ comment.content }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MovieListMypage',
  data() {
    return {
    }
  },
  props: {
    comments: Array,
    users: String,
  },
  components: {
  },
  methods: {
    goMovieDetail(comment){
      this.$router.push({ path: `/movies/${comment.movie_id}` })
    }
  },
  created() {
  },
  mounted() {
  },
  computed : {
    username () {
      if (this.users){
        return this.users
      }else{
        return this.$cookies.get("username")
      }
    },
  }
}
</script>

<style lang="scss" scoped>

#title {
  margin: 0rem 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid hsla(210,16.7%,97.6%, 0.1);
}

#review-item{
  padding: 0.5rem;
  border: 1px solid hsla(210,16.7%,97.6%, 0.1);
  border-radius: 5px;
}
</style>