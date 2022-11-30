<template >
  <div v-if="movie" class="container">
    <div class="row position-relative">
      <div class="col-sm-12 col-md-6 col-lg-5 col-xl-4 col-xxl-3 d-flex flex-column align-items-center align-items-md-end">
        <div id="overlay"></div>
        <div id="poster">
          <img id="poster-here" :src="`https://image.tmdb.org/t/p/original${this.movie.poster_path}`" alt="poster">
        </div>
      </div>
      <div class="col-sm-12 col-md">
        <div id="movie-nametag" class="d-flex flex-column align-items-sm-center align-items-md-start">
          <h1>{{ movie.title }}</h1>
          <p class="opacity-50">{{ movie.original_title }}</p>
        </div>
        <div id="movie-scores" class="d-flex flex-row justify-content-center justify-content-md-start">
          <div class="score tmdb me-3">
            <p>TMDB</p>
            <div class="hstack">
              <i id="star" class="bi bi-star-fill font" style="font-size: 0.8rem;"></i>
              <p>{{ movie.vote_average }}</p>
            </div>
          </div>
          <div class="score naver me-3" v-show="movie.vote_average_naver">
            <p>N</p>
            <div class="hstack">
              <i id="star" class="bi bi-star-fill font" style="font-size: 0.8rem;"></i>
              <p>{{ movie.vote_average_naver }}</p>
            </div>
          </div>
          <!-- 좋아요 -->
          <div class="score likes" @click="likeClick">
            <p style="font-size: 12px; text-align: left; padding-left: 0px; padding-right: 0px">보고싶어요</p>
            <div class="hstack">
              <i id="heart" class="bi bi-heart-fill" style="font-size: 0.8rem;"></i>
              <p>{{ movie.like_users.length }}</p>
            </div>
          </div>
        </div>
      </div>
    <!-- bottom -->
    </div>
    <div class="row">
      <!-- left -->
      <div id="leftSection" class="col-sm-12 col-md-6 col-lg-5 col-xl-4 col-xxl-3 justify-content-start">
        <!-- info left -->
        <!-- director -->
        <div id="info-box">
          <div>
            <p id="title" class="d-flex justify-content-center justify-content-md-start"><i class="bi bi-megaphone-fill me-2"></i>제작</p>
          </div>
          <div
            v-for="director in movie.directors"
            :key=director.id
            class="d-flex flex-row justify-content-center justify-content-md-start"
          >
            <div id="cast-card">
              <div id="profile-pic">
                <img v-show="director.profile_path" :src="`http://image.tmdb.org/t/p/original${director.profile_path}`" alt="">
                <i v-show="!director.profile_path" class="bi bi-person-circle" style="font-size: 50px"></i>
              </div>
              <p>{{ director.name }}</p>
            </div>
          </div>
        </div>
        <!-- actors -->
        <div id="info-box">
          <div>
            <p id="title" class="d-flex justify-content-center justify-content-md-start"><i class="bi bi-person-heart me-2"></i>출연</p>
          </div>
          <div class="d-flex">
            <CastList
              :actors="movie.actors"
            />
          </div>
        </div>
        <!-- keywords -->
        <div id="info-box">
          <div>
            <p id="title" class="d-flex justify-content-center justify-content-md-start"><i class="bi bi-tags-fill me-2"></i>태그</p>
          </div>
          <div class="d-flex flex-wrap">
            <div
              v-for="keyword in movie.keywords"
              :key=keyword.id
              class="btn btn-success m-1 rounded-pill"
              @click="goToKeyword(keyword)"
            >
              {{ keyword.name }}
            </div>
          </div>
        </div>
      </div>
      <!-- right side -->
      <div id="rightSection" class="col-sm-12 col-md">
        <div id="info-box">
          <MovieReview
            :movie=movie
            @refresh-request="refreshAgain"
          />
        </div>
        <br>
      </div>
    </div>
    

    
  </div>
</template>

<script>
import axios from 'axios'
import CastList from '@/components/CastList'
import MovieReview from '@/components/MovieReview'

const API_URL = 'http://127.0.0.1:8000'
// const bodyElem = document.querySelector('body')

export default {
  name: 'MovieDetail',
  data() {
    return {
      movie_id: this.$route.params.movie_id,
      movie: null,
    }
  },
  components: {
    CastList,
    MovieReview,
  },
  methods: {
    getMovieDetail() {
      axios({
        method: 'get',
        url: `${API_URL}/movies/${this.movie_id}/`,
      })
        .then(res => {
          this.movie = res.data
          console.log(this.movie)
          const headerBg = document.getElementById('header-bg')
          const backdrop = `url(https://image.tmdb.org/t/p/original${this.movie.backdrop_path})`
          headerBg.style.backgroundImage = backdrop
        })
        .catch(err => {
          console.log(err)
        })
    },
    goToKeyword(keyword) {
      this.$router.push({name: 'KeywordDetail', params: {keyword_id: keyword.id}})
    },
    refreshAgain() {
      this.movie = null
      this.getMovieDetail()
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
      this.getMovieDetail()
    },    
  },
  mounted() {
    // console.log(bodyElem)
  },
  created() {
    this.getMovieDetail()
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

#poster {
  display: flex;
  flex-direction: column;
  position: absolute;
  padding: 0;
  top: -10rem;
  // left: 3vw;
  overflow: hidden;
  border: 1px solid hsla(210,16.7%,97.6%, 0.1);
  border-radius: 5px;
  // box-shadow: rgba(255, 255, 255, 0.1) 0px 1px 1px 0px inset, rgba(50, 50, 93, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px;
  box-shadow: rgba(0, 0, 0, 0.2) 0px 20px 30px;
  width: 15rem;
  aspect-ratio: 3/4;
  float: left;
  &img {
    object-fit: cover;
    background-color: red;
  }
}
#poster img{
  object-fit: cover;
  background-color: red;
}

#overlay {
  height: 12rem;
  width: 20rem;
  content: "";
}

#leftSection{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: left;
  // border-right: 1px solid hsla(210,16.7%,97.6%, 0.1);
  overflow: hidden;
  #title {
    border-bottom: 1px solid hsla(210,16.7%,97.6%, 0.2);
    padding-bottom: 0.5rem;
    margin-right: 1rem;
    opacity: 50%;
  }
}

#rightSection{
  display: flex;
  flex-direction: column;
  align-items: left;
  text-align: left;
}

#info-box {
  display: flex;
  flex-direction: column;
  justify-content: left;
  padding: 1rem 0rem 1rem 0rem;
  * {
    display: block;
    color: white;
  }
}

#profile-pic {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  width: 5rem;
  min-height: 5rem;
  border: 1px solid hsla(210,16.7%,97.6%, 0.1);
  box-shadow: rgba(0, 0, 0, 0.4) 0px 20px 30px;
  border-radius: 50%;
  margin-bottom: 1rem;
  img{
    width: 100%;
    aspect-ratio: 1/1;
    object-fit: cover;
  }
  i{
    margin-bottom: -5px;
  }
}

#cast-card {
  width: 100px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  p{
    margin: 0;
    padding: 0;
    line-height: 14px;
    text-align: center;
    min-height: 30px;
    overflow: hidden;
  }
}

.score {
  position: relative;
  text-align: right;
  padding: 0rem 0.5rem;
  font-weight: bold;
  display: flex;
  justify-content: space-between;
  border-radius: 5px;
  width: 8rem;
  border: 1px solid hsla(210,16.7%,97.6%, 0.1);
  background-color: #212529;
  p{
    margin: 0;
    padding: 5px;
    font-size: 15px;
    line-height: 15px;
  }
  &.tmdb{
    background-color: #01baef;
  }
  &.naver{
    background-color: #20bf55;
  }
  &.likes {
    background-color: #e5383b;
    overflow: hidden;
    i{
      margin: 0;
      padding-top: 1px;
    }
    &:hover{
      i{
        transform-origin: center;
        animation: jump .75s linear alternate infinite;
      }
    }
  }
}

.score:hover{
  cursor: pointer;
  #star{
    animation: donut-spin 1.2s linear infinite;
  }
}

// 회전 애니메이션
@keyframes donut-spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

</style>