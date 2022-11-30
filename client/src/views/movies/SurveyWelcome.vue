<template>
  <div>
    <h3>{{username}} 님, 환영합니다!</h3>
    <p>좋아하는 콘텐츠를 선택해주세요.</p>
    <p class="opacity-50">선택하신 결과를 바탕으로 무비 큐레이터가 취향맞춤 영화를 추천해드립니다.</p>
    <MovieListSurvey 
    />

    <!-- modals-container -->
    
  </div>
</template>

<script>
import MovieListSurvey from '@/components/MovieListSurvey'

export default {
  name: 'SurveyWelcome',
  data: function () {
    return {
      modalShow : false,
    }
  },
  components: {
    MovieListSurvey,
  },
  method: {
  },
  computed : {
    username () {
      return this.$cookies.get("username")
    },
  }
}
</script>

<style lang="scss" scoped>
p {
  border-bottom: 1px solid hsla(210,16.7%,97.6%, 0.1);
  padding-bottom: 1rem;
}
</style>