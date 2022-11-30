<template>
  <div class="card-wrapper" @click='goToDetail' @mouseover='changeHeaderBg'>
    <div class="poster-img-box">
      <img class="poster-img"
        :src="`https://image.tmdb.org/t/p/original${movie.poster_path}`"
        alt="poster"
      >
      <div id="like-btn" @click.stop="likeClick">
        <i class="bi bi-heart-fill"></i>
      </div>
    </div>
    <div class="poster-text">
      <p class="poster-movie-title">{{ movie.original_title }}</p>
      <p class="poster-movie-subtitle">{{ movie.title }}</p>
    </div>
  </div>

  
</template>

<script>
import axios from 'axios'
const API_URL = 'http://127.0.0.1:8000'

export default {
  name: 'MovieListItem',
  data () {
    return {
      modalMsg : '',
      modalShow : false,
    }
  },
  props: {
    movie: Object,
  },
  components : {
  },
  methods: {
    goToDetail() {
      this.$router.push({name: 'MovieDetail', params: {movie_id: this.movie.id}})
    },
    changeHeaderBg() {
      const headerBg = document.getElementById('header-bg')
      const backdrop = `url(https://image.tmdb.org/t/p/original${this.movie.backdrop_path})`
      headerBg.style.backgroundImage = backdrop
    },
    likeClick () {
      if (this.isLogin) {
        const token = this.$cookies.get('jwt')
        console.log('좋아요 클릭 -> 로그인 됨')
        // movie 에 좋아요 수가 있어야 되고
        // 내가 좋아요 한 목록이 있어야 되고
        axios({
          method: 'post',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
          url: `${API_URL}/movies/${this.movie.id}/likes/`,
        })
          .then((res) => {
            console.log(res)
          })

      } else {
        console.log('좋아요 클릭 -> 로그인 안됨')
        // this.$emit('change')
        this.$store.commit('LOGIN_MODAL_OPEN')
        
      }
    },
    modalGoToLogin () {

    },
  },
  computed : {
    isLogin () {
      if (this.$cookies.get('jwt')){
        return true
      }else{
        return false
      }

    },
  }
}
</script>

<style lang="scss" scoped>
.card-wrapper {
  display: flex;
  flex-direction: column;
  width: 15rem;
  padding-top: 1rem;
  box-sizing: border-box;
  /* border: 1px solid red; */
}
.poster-img-box{
  display: flex;
  position: relative;
  flex-direction: column;
  width: auto;
  overflow: hidden;
  margin: 0;
  border: 1px solid hsla(210,16.7%,97.6%, 0.1);
  border-radius: 5px;
  transition: scale 0.3s;
  /* box-shadow: rgba(255, 255, 255, 0.1) 0px 1px 1px 0px inset, rgba(50, 50, 93, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px; */
  box-shadow: rgba(0, 0, 0, 0.2) 0px 20px 30px;
  /* max-height: 20rem; */
}
.poster-img-box:hover{
  scale: 102%;
}

.poster-img {
  margin: 0;
  max-width: 100%;
  aspect-ratio: 3/4;
  border-radius: 5px;
  object-fit: cover;
}

.poster-text {
  margin: 0;
  text-align: left;
  padding: 20px 5px;
  
}

.poster-movie-title {
  margin: 0;
  font-size: 15px;
  line-height: 15px;
  font-weight: bold;
  margin-bottom: 1rem;
}

.poster-movie-subtitle {
  margin: 0;
  padding: 0;
  font-size: 12px;
  line-height: 12px;
  opacity: 50%;
}
/* card css */


/* .card {
  display: flex;
  width: 15rem;
  height: 20rem;
  padding: 0;
  box-shadow: 0 2px 4px 0 rgba(0,0,0,0.1);
  border-radius: 8px;
  border-color: none;
  box-sizing: border-box;
  overflow: hidden;
  background-color: #252422;
  color: #F1FAEE;
  border-radius: 0px;
}

.card * {
  transition: 0.3s ease all;
}

.card img {
  margin: 0;
  max-height: 20rem;
  object-fit: cover;
  display: block;
}

.card h3 {
  margin: 0;
  padding: 12px 12px 48px;
  line-height: 32px;
  font-weight: bold;
}

.card .focus-content {
  display: block;
  padding: 8px 12px;
}

.card p {
  text-align: left;
  margin: 0;
  line-height: 1.5;
}

.card:hover img, .card:focus-within img {
  margin-top: -20rem;
}

.card:hover h3, .card:focus-within h3 {
  padding: 8px 12px 0;
} */

#like-btn {
  display: flex;
  position: absolute;
  right: 0;
  width: 30px;
  height: 30px;
  overflow: hidden;
  background: red;
  border-radius: 50%;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0.5rem;
  border: 1px solid hsla(210,16.7%,97.6%, 0.1);
  i{
    margin: 0;
    padding-top: 3px;
  }
  &:hover{
    i{
      transform-origin: center;
      animation: jump .75s linear alternate infinite;
    }
  }
}
</style>