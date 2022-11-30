<template>
  <div>
    <div id="surveyBox">
      <RecommendedMovieItem/>
    </div>
  </div>
</template>

<script>
import RecommendedMovieItem from '@/components/RecommendedMovieItem'

import axios from 'axios'
const API_URL = 'http://127.0.0.1:8000'

export default {
  name: 'Test',
  data(){
    return{
      
    }
  },
  components:{
    RecommendedMovieItem,
  },
  methods : {
    getTest() {
      console.log('여기 ss')
      const token = this.$cookies.get('jwt')
      axios({
        method: 'post',
        url: `${API_URL}/movies/test/`,
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        data:{
          'pk' : 436270
        }
      })
        .then((res) => {
          console.log(res.data)
        })
    },
    getTest2 () {
      const token = this.$cookies.get('jwt')
      // 4번 문제
      axios({
        method: 'get',
        url: `${API_URL}/accounts/mypage/`,
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
        .then((res)=>{
          console.log(res)
        })
        .catch((err)=>{
          console.log(err)
        })
    }
  },
  computed : {
    res (){
      return this.$route.params.res
    } 
  }
}
</script>
