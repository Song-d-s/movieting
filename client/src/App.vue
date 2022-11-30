<template>
  <div id="app" class="position-relative">
    <!-- nav bar -->
    <div id="nav" class="sticky-top d-flex flex-column align-items-center" style="min-width: 310px">
      <div class="d-flex justify-content-between" style="width: 80%">
        <!-- left -->
        <div class="" style="text-align: left; height: 40px; margin: -3px;">
          <router-link id="logo" class="me-auto" :to="{ name: 'Home' }" style="text-decoration:none;">무비팅</router-link>
        </div>
        <!-- right -->
        <div class="d-flex flex-column align-items-center justify-content-center">
          <div class="hstack gap-3">
            <div v-if="!isLogin" class=".loginDiv" >
              <!-- 카카오에서 발급 받은 키 입력 -->
              <KakaoLogin 
                style="margin-top: 6px;"
                ref="loginDiv"
                api-key="카카오에서 발급 받은 키 입력"
                image="kakao_login_btn_small"
                :on-success=onSuccess
                :on-failure=onFailure
                />
            </div>
            <div v-if="isLogin">
              <div class="hstack gap-2">
                <div class="d-flex align-items-center" id="profile_thumb">
                  <img :src="imgUrl" alt="profile_thumb" width="40px;">
                </div>
                <router-link :to="{ name: 'MyPage' }" style="text-decoration:none;">{{ username }}님</router-link> 
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- header bg -->
    <div id="header-overlay" class="d-flex justify-content-center">
      <HomeHeader
        :isLogin=isLogin 
        v-show="showBanner"
      />
    </div>
    <div id="header-bg"></div>
    <!-- router-view -->
    <div style="position: relative; min-height: 100%; padding-bottom: 100px">
      <div class="container-fluid d-flex justify-content-center">
        <div id="body">
          <router-view @change="change"/>
        </div>
      </div>
      
      <!-- modals-container -->
      <LoginModal @open-login="modalLogin" @close-modal="modalClose" v-show="modalShow"/>
      <SurveyCompleteModal @go-recommend="goRecommend" @close-modal="surveyCompletedModalClose" v-show="surveyCompletedModalShow"/>
      <inputValidModal @close-modal="inputValidModalClose" v-show="inputValidModalShow"/>

      <!-- footer -->
      <footer>
        <div class="container d-flex flex-row">
          <div class="d-flex align-items-center mt-3 fw-bold opacity-50">
            <div class="team-logo d-flex" >
              <img
                style="width:150px; object-fill: cover;"
                src="@/assets/image/team-logo.png">
            </div>
            <!-- <router-link class="me-auto" :to="{ name: 'SurveyWelcome' }" style="text-decoration:none;">서베이 테스트</router-link> -->
          </div>
          <div class="vstack gap-3 mt-3">
            <div class="hstack gap-3 opacity-50 d-flex w-100 justify-content-end" style="width: 150px;">
              <p class="m-0">송단샘</p>
              <div class="vr"></div>
              <a href="mailto:s2770853@gmail.com"><i class="bi bi-envelope-fill"></i></a>
              <a href="https://github.com/Song-d-s"><i class="bi bi-github"></i></a>
            </div>
            <div class="hstack gap-3 opacity-50 d-flex w-100 justify-content-end" style="width: 150px;">
              <p class="m-0">정민지</p>
              <div class="vr"></div>
              <a href="mailto:wjdalswl0731@gmail.com"><i class="bi bi-envelope-fill"></i></a>
              <a href="https://github.com/jellyKKing"><i class="bi bi-github"></i></a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script>
import LoginModal from '@/components/LoginModal'
import HomeHeader from '@/components/HomeHeader'
import InputValidModal from '@/components/InputValidModal'
import SurveyCompleteModal from '@/components/SurveyCompleteModal'
import KakaoLogin from 'vue-kakao-login'
import axios from 'axios'
const API_URL = 'http://127.0.0.1:8000'

export default {
  name: 'App',
  data: function () {
    return {
      isLogin : false,
      username : '',
      imgUrl : '',
      showBanner : true,
      survey : false,
    }
  },
  components: {
    KakaoLogin,
    HomeHeader,
    LoginModal,
    SurveyCompleteModal,
    InputValidModal,
  },
  methods: {
    modalClose(){
      this.$store.commit('LOGIN_MODAL_CLOSE')
    },
    surveyCompletedModalClose () {
      this.$store.commit('SURVEY_COMPLETED_MODAL_CLOSE')
    },
    inputValidModalClose () {
      this.$store.commit('INPUT_VALID_MODAL_CLOSE')
    },
    goRecommend(){
      this.$store.commit('SURVEY_COMPLETED_MODAL_CLOSE')
      this.$router.push({ path: 'RecommendedMovieList' })
    },
    modalLogin(){
      this.modalClose()
      // sss = document.querySelectorAll('.loginDiv')
      // console.log(sss)
      console.log(this.$refs.loginDiv)
      this.$refs.loginDiv.$el.click()
    },
    change () {
      console.log('에밋 쓰리 됨')
      this.$store.commit('LOGIN_MODAL_OPEN')
      // this.modalShow = true
      console.log(this.modalShow)
    },
    onSuccess (res) {
      console.log("success")
      axios({
        method: 'post',
        url: `${API_URL}/accounts/login/`,
        data: {
          res : res,
        }
      })
        .then((response)=>{
          console.log('로그인 성공띠')
          if (response.status == 201){
            this.survey = true
          }
          this.loginToken(response)
        })
    },
    onFailure (data) {
      console.log(data)
      console.log("failure")
    },
    loginToken: function (res) {
      axios({
        method: 'post',
        headers: {
          'Content-Type': 'application/json',
        },
        url: `${API_URL}/api/token/`,
        data: {
          username: res.data.serializer.username,
          password: res.data.serializer.id,
        }
      })
        .then((res) => {
          console.log('쿠키끗')
          const token = res.data.access 
          this.$cookies.set("jwt", token)
          this.$store.commit('ISLOGIN_CHANGE')

          window.Kakao.API.request({
            url: '/v2/user/me',
            data: {
              property_keys: ['kakao_account.email', 'kakao_account.gender', 'kakao_account.profile'],
            },
          })
          .then((response) => {
            console.log(response)
            this.$cookies.set("userId",  response.id)
            this.$cookies.set("username",  response.kakao_account.profile.nickname)
            this.$cookies.set("email",  response.kakao_account.email)
            this.$cookies.set("imgUrl",  response.kakao_account.profile.profile_image_url)
            this.$cookies.set("gender",  response.kakao_account.gender)
            // this.$store.commit('LOGINDATA_IN', response)
            this.isLogin = true
            this.username = response.kakao_account.profile.nickname
            this.imgUrl = response.kakao_account.profile.profile_image_url

            if (this.survey == true){
              this.$router.push({ name: 'SurveyWelcome' })
              this.survey = false
            }
            
          })
          .catch(function(error) {
            console.log(error)
          })
        })
    },
    // logout (){
    //   this.$cookies.set("jwt", '')
    //   this.$cookies.set("username", '')
    //   this.$cookies.set("email", '')
    //   this.$cookies.set("imgUrl", '')
    //   this.$cookies.set("gender", '')
    //   this.isLogin = false
    //   this.username = ''
    //   this.imgUrl = ''
    //   // this.$store.commit('ISLOGIN_CHANGE')
    // }
  },
  computed : {
    surveyCompletedModalShow () {
      return this.$store.state.surveyCompletedModal
    },
    modalShow () {
      return this.$store.state.loginModal
    },
    inputValidModalShow () {
      return this.$store.state.inputValidModalShow
    }
  },
  updated() {
    const headerOverlay = document.getElementById('header-overlay')
    console.log(this.$route.name)
    // header height adjust
    if (this.$route.name === 'SurveyWelcome') {
      headerOverlay.setAttribute('style', 'height: 100px')
    } else {
      headerOverlay.setAttribute('style', 'height: 350px')
    }
    // show header banner
    if (this.$route.name === 'Home') {
      headerOverlay.setAttribute('style', 'margin-bottom: 0px')
      this.showBanner = true
    } else {
      this.showBanner = false
    }
  },
  mounted () {
    this.isLogin = this.$cookies.get("jwt") ? true : false
    this.username = this.$cookies.get("username")
    this.imgUrl = this.$cookies.get("imgUrl")
  }
}
</script>


<style lang="scss">
@font-face {
    font-family: 'IBMPlexSansKR-Regular';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-07@1.0/IBMPlexSansKR-Regular.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}

@font-face {
    font-family: 'PyeongChangPeace-Bold';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2206-02@1.0/PyeongChangPeace-Bold.woff2') format('woff2');
    font-weight: 700;
    font-style: normal;
}

*{
  margin: 0;
  padding: 0;
}

#app {
  font-family: IBMPlexSansKR-Regular, Helvetica, Arial, sans-serif, PyeongChangPeace-Bold;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  display: flex;
  flex-direction: column;
  /* overflow: hidden; */
}

#logo {
  font-family: PyeongChangPeace-Bold;
  font-weight: normal;
  font-size: 35px;
  margin: 0px;
}

#nav {
  padding: 0.5rem 1rem;
  position: sticky;
  min-height: 59px;
  -webkit-backdrop-filter: blur(8px);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid hsla(210,16.7%,97.6%, 0.1);
}

#nav a {
  // font-weight: bold;
  color: #FFFFFF;
}

/* #nav a.router-link-exact-active {
  color: #FCA311;
} */

router-link {
  text-decoration: none;
}

h1 {
  font-weight: bold;
}

#header-bg {
  position: absolute;
  height: 500px;
  max-height: 500px;
  width: 100%;
  margin-top: 50px;
  background-repeat: no-repeat;
  background-size: cover;
  transition: background-image 1s ease;
  z-index: -1;
  &:before,
  &:after {
    display: block;
    position: absolute;
    top: 0;
    width: 100%; // container에 준 여백값보다 크지 않게 사이즈 지정하기 (swiper-slide의 클릭 이벤트에 영향을 주지 않고, 이렇게 지정해야 그라데이션이 영역 내부에 있는 탭이 스크롤 하기 전엔 영향을 주지 않음)
    height: 100%;
    z-index: 0;
    content: "";
  }
  &:before{
    background-color: hsla(210, 11%, 15%, 0.3);
  }
  &:after {
    bottom: 0;
    background: linear-gradient(0deg, #212529 0%, hsla(210, 11%, 15%, 0.2) 25%, hsla(210, 11%, 15%, 0) 50%, hsla(210, 11%, 15%, 0.2) 75%, #212529 100%);
    // background: linear-gradient(180deg, #212529 -20.19%, rgba(33, 37, 41, 0.8) 18.31%, rgba(33, 37, 41, 0) 75%);
  }
}

#header-overlay{
  position: relative;
  // margin-bottom: 350px;
  height: 350px;
}

#body {
  width: 80%;
  min-width: 342px;
  min-height: 400px;
  background-color: #212529;
  border: 1px solid hsla(210,16.7%,97.6%, 0.1);
  padding: 1rem 0rem;
}

@keyframes jump {
  0%   {transform: translate3d(0,0,0) scale3d(1,1,1);}
  25%  {transform: translate3d(0,30%,0) scale3d(.7,1.5,1);}
  50% {transform: translate3d(0,100%,0) scale3d(1.5,.7,1);}
  75%  {transform: translate3d(0,30%,0) scale3d(.7,1.5,1);}
  100%   {transform: translate3d(0,0,0) scale3d(1,1,1);}
}

body.modal-open {
  padding: 0px !important;
  overflow: auto;
}

footer{
  border-top: 1px solid hsla(210,16.7%,97.6%, 0.1);
  position: absolute;
  bottom: -100px;
  background-color: #1b1f22;
  width: 100%;
  height: 100px;
}

#profile_thumb {
  overflow: hidden;
  border-radius: 50%;
  border: 1px solid hsla(210,16.7%,97.6%, 0.1);
}


</style>