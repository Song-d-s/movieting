<template>
  <div class="overlay">
    <div class="container">
      <div class="d-flex row gx-3 row-cols-auto justify-content-center">
        <div class="d-flex col justify-content-center"
          v-for="movie in movies"
          :key=movie.id
        >
          <MovieListSurveyItem 
          :movie=movie 
          />
        </div>
      </div>
    </div>
    
    <button class="btn btn-primary rounded-pill mt-3 fw-bold"
      style="color: white;"
      @click="selectDone">
      확 인
    </button>
    
  </div>
</template>

<script>
import axios from 'axios'
import MovieListSurveyItem from '@/components/MovieListSurveyItem'
const API_URL = 'http://127.0.0.1:8000'

export default {
  name: 'MovieListSurvey',
  components: {
    MovieListSurveyItem,
  },
  data() {
    return {
      movies: null,
      moviesSelected: null,
    }
  },
  methods: {
    getRandom() {
      axios({
        method: 'get',
        url: `${API_URL}/movies/random`,
      })
        .then(res => {
          this.movies = res.data
        })
        .catch(err => {
          console.log(err)
        })
    },
    selectDone () {
      const token = this.$cookies.get('jwt')

      let ids = []
      for (let i = 0; i < this.surveySelectMovies.length; i++) {
        ids.push(this.surveySelectMovies[i].id)
      }

      axios({
        method: 'post',
        url: `${API_URL}/movies/surveydone/`,
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        data : {
          surveySelectMovies: ids
        },
      })
        .then(res => {
          console.log(res)
          this.$store.commit('SURVEY_COMPLETED_MODAL_OPEN')
        })
        .catch(err => {
          console.log(err)
        })

    },
    test () {
      this.$store.commit('SURVEY_COMPLETED_MODAL_OPEN')
      console.log(this.$store.state.surveyCompletedModal)
    }
  },
  mounted() {
    this.getRandom()
  },
  computed : {
    surveySelectMovies () {
      return this.$store.state.surveyItemPick
    }
  }
}
</script>


<style lang="scss" scoped>
.container{
  width: 100%;
  max-height: 850px;
  padding: 20px 0px;
  overflow: scroll;
  overflow-x: hidden;
}

/* width */
::-webkit-scrollbar {
  width: 10px;
}

/* Track */
::-webkit-scrollbar-track {
  background: transparent;
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: hsla(210,16.7%,97.6%, 0.2);
  border-radius: 5px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: hsla(210,16.7%,97.6%, 0.5);
}
</style>