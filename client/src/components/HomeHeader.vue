<template>
  <div class="banner-box">
    <div class="hstack gap-1" style="font-weight: normal; font-size: 23px;">
      <p v-if="!isLogin">로그인하고 </p>
      <p> 무비 큐레이터</p>
      <p style="font-weight: normal">정민지</p>
      <p>가 추천하는</p>
    </div>
    <div class="hstack gap-1" style="font-size: 25px;">
      <h1 v-show="username">{{ username }}님</h1>
      <h1 v-show="!username">당신</h1>
      <h1>의 취향 맞춤 영화</h1>
      <p v-if="!isLogin" style="font-weight: normal">를 알아보세요!</p>
    </div>
    <br>
    <router-link v-if="isLogin"
      :to="{ name: 'Test' }"
      style="text-decoration:none;"
      class="btn btn-primary rounded-pill"
    >
      바로가기
    </router-link> 
  </div>
</template>

<script>
export default {
  name: 'HomeHeader',
  props: {
    isLogin: Boolean,
  },
  computed: {
    username () {
      return this.$cookies.get("username")
    },
  },
  mounted (){
    console.log('header')
    console.log(this.isLogin)
  }
}
</script>

<style lang="scss" scoped>
  @keyframes fade-left {
    0% {
      transform: translateX(-100px);
      opacity: 0;
    }
    100% {
      transform: translateX(0);
      opacity: 1;
    }
  }

  @keyframes float {
    0% {
      // box-shadow: 0 5px 15px 0px rgba(0,0,0,0.6);
      transform: translatey(0px);
    }
    50% {
      // box-shadow: 0 25px 15px 0px rgba(0,0,0,0.2);
      transform: translatey(-10px);
    }
    100% {
      // box-shadow: 0 5px 15px 0px rgba(0,0,0,0.6);
      transform: translatey(0px);
    }
  }

  .banner-box {
    display: flex;
    flex-direction: column;
    align-items: start;
    justify-content: end;
    font-weight: bolder;
    animation: fade-left 0.5s linear;
    width: 80%;
    height: 100%;
    padding: 5rem;
    h1{
      font-weight: bolder
    }
    p,
    h1{
      text-shadow: rgba(0, 0, 0, 0.4) 0px 20px 30px;
      margin-bottom: 5px;
    }
    .btn{
      color: white;
      font-weight: bolder;
      box-shadow: rgba(0, 0, 0, 0.4) 0px 20px 30px;
      border: 1px solid hsla(210,16.7%,97.6%, 0.1);
    }
    &:hover {
      .btn,
      .hstack,
      h1,
      p{
        animation: float 6s ease-in-out infinite;
      }
    }
  }
</style>