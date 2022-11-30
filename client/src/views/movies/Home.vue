<template>
  <div class="home">
    <!-- pop row -->
    <MovieListPopular/>
  </div>
</template>

<script>
import MovieListPopular from '@/components/MovieListPopular'

export default {
  name: 'Home', 
  components: {
    MovieListPopular,
  },
  data: function () {
    return {
      
    }
  },
  methods: {
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