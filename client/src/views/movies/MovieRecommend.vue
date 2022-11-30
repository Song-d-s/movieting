<template>
  <div class="home">
    <!-- pop row -->
    <MovieListPopular @change="change"/>
  </div>
</template>

<script>
import MovieListPopular from '@/components/MovieListPopular'

export default {
  name: 'MovieRecommend', 
  components: {
    MovieRecommend,
  },
  data: function () {
    return {
      
    }
  },
  methods: {
    change () {
      console.log('에밋 투 됨')
      this.$emit('change')
    },
  },
  created() {

  },
}
</script>

<style scoped>
  .home {
    display: flex;
    flex-direction: column;
    padding: 0rem;
  }
</style>