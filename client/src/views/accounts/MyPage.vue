<template>
  <div class="container">
    <div class="row position-relative">
      <!-- left -->
      <div id="left" class="d-flex flex-column col-sm-12 col-md-6 col-lg-5 col-xl-4 col-xxl-3">
        <div class="d-flex flex-column align-items-center w-100">
          <div class="profile-overlay"></div>
          <div class="profile">
            <img :src="imgUrl" alt="">
          </div>
          <div id="username-bar" class="hstack gap-2 justify-content-center pb-1 mb-2">
            <div style="font-size: 2rem" class="text-truncate">{{ username }}</div>
            <div id="gender" :class="gender">
              <i v-if="gender === 'male'" class="bi bi-gender-male"></i>
              <i v-if="gender === 'female'" class="bi bi-gender-female"></i>
            </div>
          </div>
          <p class="opacity-50">{{ email }}</p>
        </div>
        <br>
        <div id="profile-card" class="row">
          <div class="col">
            <div class="vstack gap-2 m-2">
              <i class="bi bi-heart-fill"></i>
              <hr>
              <p>{{ user_like_movies_len }}</p>
            </div>
          </div>
          <div class="col">
            <div class="vstack gap-2 m-2">
              <i class="bi bi-pencil-fill"></i>
              <hr>
              <p>{{ user_created_comments_len }}</p>
            </div>
          </div>
          <div class="col">
            <div class="vstack gap-2 m-2">
              <i class="bi bi-person-fill" style="scale: 1.2"></i>
              <hr>
              <p>{{ followers_len }}</p>
            </div>
          </div>
        </div>
        <div class="d-flex flex-column w-100 justify-content-end align-items-end mt-2">
          <a href="https://kauth.kakao.com/oauth/logout?client_id=19909bfbfb8745d6172a4ab6b541c7e8&logout_redirect_uri=http://localhost:8080/movies" @click="logout">Logout</a>
        </div>
      </div>
      <!-- right -->
      
      
      <br>
      <div class="col-sm-12 col-md">
        <div id="title" class="d-flex" >
          <div class="hstack gap-3 fs-3">
            <i class="bi bi-person-hearts"></i>
            <p>회원님과 가장 유사한 추천 회원</p>
          </div>
        </div>
        <!-- {{ similarUserList }} -->
        <div class="d-flex p-3" v-for="u in similarUserList" :key=u.id @click="goUser(u)">
          <div class="d-flex flex-column">
            <img id="profilePic" :src="u.imgUrl" alt="profile_thumb" width="50px;">
            <p>{{ u.username }}</p>
          </div>
        </div>
        <!--좋아요, 내가 쓴 리뷰, 써클, 메신저, 칭구-->
        <!-- 여긴 내용<br>
        -- 좋아요 한 영화들 -- <br>
        {{ user_like_movies }} <br> -->
        <MovieListMypage :movies=user_like_movies />
        <!-- -- 사용자가 쓴 리뷰들 -- <br>
        {{ user_created_comments }}  -->
        <ReviewListMypage :comments=user_created_comments />

        <div id="title" class="d-flex" >
          <h3>팔로워</h3>
        </div>

        <!-- {{ similarUserList }} -->
        <div class="d-flex flex-column"
        v-for="f in followers"
          :key="f.id+1">
          <p @click="goUser(f)"> {{ f.username }}</p>
        </div>
        <br>
      </div>
    </div>
    <br>
  </div>
</template>

<script>
import axios from 'axios'
import ReviewListMypage from '@/components/ReviewListMypage'
import MovieListMypage from '@/components/MovieListMypage'
const API_URL = 'http://127.0.0.1:8000'

export default {
  name: 'Test',
  data(){
    return{
      user_like_movies : null,
      user_created_comments : null,
      user_like_movies_len : 0,
      user_created_comments_len : 0,
      similarUserList : null,
      followers_len : 0,
      followers : null,
    }
  },
  components : {
    MovieListMypage,
    ReviewListMypage,
  },
  methods : {
    goUser (user) {
      this.$router.push({ path: `/accounts/userpage/${user.id}` })
    },
    logout (){
      this.$cookies.set("jwt", '')
      this.$cookies.set("username", '')
      this.$cookies.set("email", '')
      this.$cookies.set("imgUrl", '')
      this.$cookies.set("gender", '')
      this.$cookies.set("userId", '')
      this.isLogin = false
      this.username = ''
      this.imgUrl = ''
      // this.$store.commit('ISLOGIN_CHANGE')
    },
    tesetClick () {
      
    },
  },
  computed : {
    username () {
      return this.$cookies.get("username")
    },
    email () {
      return this.$cookies.get("email")
    },
    gender () {
      return this.$cookies.get("gender")
    },
    imgUrl () {
      return this.$cookies.get("imgUrl")
    },
  },
  mounted(){
    const token = this.$cookies.get('jwt')
      axios({
        method: 'post',
        url: `${API_URL}/accounts/mypage/`,
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
        .then((res) => {
          console.log(res.data)
          this.user_like_movies = res.data.user_like_movies
          this.user_created_comments = res.data.user_created_comments
          this.user_like_movies_len = res.data.user_like_movies_len
          this.user_created_comments_len = res.data.user_created_comments_len
          this.followers = res.data.followers
          this.followers_len = res.data.followers_len

          axios({
            method: 'post',
            url: `${API_URL}/accounts/usersimilarity/`,
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          })
            .then((res) => {
              console.log(res.data)
              this.similarUserList = res.data
            })
        })
  }
}
</script>

<style lang="scss" scoped>
*{
  margin:0;
  padding:0;
}

#title {
  padding: 0;
  margin: 0;
  border-bottom: 1px solid hsla(210,16.7%,97.6%, 0.1);
}

#profilePic{
  border-radius: 50%;
  border: 1px solid hsla(210,16.7%,97.6%, 0.1);
  box-shadow: rgba(0, 0, 0, 0.4) 0px 20px 30px;
}

#left {
  padding: 1rem;
  border-right: 1px solid hsla(210,16.7%,97.6%, 0.1);
  justify-content: center;
  align-items: center;
}
.profile {
  position: absolute;
  top: -6rem;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  width: 10rem;
  min-height: 10rem;
  border: 1px solid hsla(210,16.7%,97.6%, 0.1);
  box-shadow: rgba(0, 0, 0, 0.4) 0px 20px 30px;
  border-radius: 50%;
  margin-bottom: 1rem;
  img{
    width: 100%;
    aspect-ratio: 1/1;
    object-fit: cover;
  }
}
.profile-overlay{
  width: 100%;
  min-height: 5rem;
}

#gender{
  padding: 0;
  margin: 0;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-weight: bolder;
  font-size: 1rem;
  overflow: hidden;
  border: 1px solid hsla(210,16.7%,97.6%, 0.2);
  box-shadow: rgba(0, 0, 0, 0.4) 0px 20px 30px;
  i{
    margin-top: 3px;  
    // margin-right: 2px;
  }
  &.male{
  background-color: #01baef;
  }
  &.female{
  background-color: #e5383b;
  }
}
#username-bar {
  width: 100%;
  border-bottom: 1px solid hsla(210,16.7%,97.6%, 0.2);
}

#profile-card {
  width: 100%;
  border: 1px solid hsla(210,16.7%,97.6%, 0.2);
  border-radius: 5px;
}
</style>