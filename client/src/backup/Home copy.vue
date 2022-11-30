<template>
  <div>
    <!-- header -->
    <div class="d-flex row mb-4">
      <div class="col-1">
        <!-- left space -->
      </div>
      <!-- center space, carousel here -->
      <div class="col-8">
        <div id="carouselExampleControls" class="carousel slide" data-bs-ride="carousel">
          <div class="carousel-inner">
            <div class="carousel-item active">
              <div style="position: relative; border: 1px solid #252422; border-width: 0px 1px">
                <h1 style="position: absolute; z-index: 1; bottom:0;" >글씨</h1>
                <img src="https://image.tmdb.org/t/p/original/33dV6HAnXBmwKl640gO3U4auqUN.jpg" class="d-block w-100" alt="...">
              </div>
            </div>
            <div class="carousel-item">
              <img src="https://image.tmdb.org/t/p/original/wPjtacig0kIkVcTQmXoNt6jbMwo.jpg" class="d-block w-100" alt="...">
            </div>
            <div class="carousel-item">
              <img src="https://image.tmdb.org/t/p/original/b7xQ5fuyVO4c24igizCfPgF6n7q.jpg" class="d-block w-100" alt="...">
            </div>
          </div>
          <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="prev">
            <!-- <span class="carousel-control-prev-icon" aria-hidden="true"></span> -->
            <span class="visually-hidden">Previous</span>
          </button>
          <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="next">
            <!-- <span class="carousel-control-next-icon" aria-hidden="true"></span> -->
            <span class="visually-hidden">Next</span>
          </button>
        </div>
      </div>
      <!-- right space -->
      <div class="col-3">
        <span>몰라</span>
      </div>
    </div>

    <!-- pop row -->
    <h1>Popular</h1>
    <MovieListPopular/>
    <!-- <h1>Popular</h1>
    <div class="slide-container">
      <div class="slide-content">
        <div class="card-wrapper" v-for="movie in movies_pop" :key="movie.id">
          <div class="card">
            <div class="image-content">
              <span class="overlay"></span>
              <div class="card-image">
                <img class="card-img" :src="`https://image.tmdb.org/t/p/original${movie.poster_path}`" alt="poster">
              </div>
            </div>

            <div class="card-content">
              <h2 class="name">{{ movie.title }}</h2>
              <p class="description">{{ movie.overview }}</p>
              <button class="btn">View More</button>
            </div>
          </div>
        </div>
      </div>
      
    </div> -->

    <!-- random row -->
    <!-- <h1>랜덤 영화</h1>
    <div class="d-flex row g-4 justify-content-center">
      <div
        class="d-flex col-3 justify-content-center"
        v-for="movie in movies"
        @click="goToDetail(movie)"
        :key="movie.id"
      >
        <MovieListItem :movie=movie />
      </div>
    </div> -->
  </div>
</template>

<script>
import axios from 'axios'
// import MovieListItem from '@/components/MovieListItem'
import MovieListPopular from '@/components/MovieListPopular'

const API_URL = 'http://127.0.0.1:8000'

export default {
  name: 'Home', 
  components: {
    // MovieListItem,
    MovieListPopular,
  },
  data: function () {
    return {
      movies: null,
    }
  },
  methods: {
    getMovies() {
      // const token = localStorage.getItem('jwt')
      axios({
        method: 'get',
        url: `${API_URL}/movies/`,
        // headers: {
        //   'Authorization': `Bearer ${token}`,
        // },
      })
        .then(res => {
          console.log(res.data)
          this.movies = res.data
        })
        .catch(err => {
          console.log(err)
        })
    },

  },
  created() {
    this.getMovies()
  },
}
</script>

<style scoped>
  /* .slide-container{
    max-width: 1120px;
    width: 100%;
    background-color: white;

  }
  .slide-content{
    margin: 0 40px;
  }
  .card {
    width: 320px;
    border-radius: 15px;
    background-color: gray;
  }
  .image-content,
  .card-content{
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10px 14px;
  }
  .image-content{
    position: relative;
    row-gap: 5px;
    
  }
  .overlay{
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: 100%;
    background-color: #4070f4;
    border-radius: 15px 15px 0 15px;
  }
  .overlay::before,
  .overlay::after{
    content: '';
    position: absolute;
    right: 0;
    bottom: -40px;
    height: 40px;
    width: 40px;
    background-color: #4070f4;
  }
  .overlay::after{
    border-radius: 0 15px 0 0;
    background-color: gray;
  }
  .card-image{
    position: relative;
    aspect-ratio: 3/4;
    width: 15rem;
  }
  .card-image .card-img{
    height: 100%;
    width: 100%;
    object-fit: cover;
    border-radius: 50%;
  }
  .name{
    font-size: 18px;
    font-weight: 700;
  }
  .overview{
    font-size: 14px;
    text-align: center;
  } */
</style>