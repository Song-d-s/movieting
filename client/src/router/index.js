import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '@/views/movies/Home'
import MovieDetail from '@/views/movies/MovieDetail'
// import KeywordDetail from '@/views/movies/KeywordDetail'
import SurveyWelcome from '@/views/movies/SurveyWelcome'
import RecommendedMovieList from '@/views/movies/RecommendedMovieList'

import UserPage from '@/views/accounts/UserPage'
import Test from '@/views/accounts/Test'
import MyPage from '@/views/accounts/MyPage'


// swiper
import VueAwesomeSwiper from 'vue-awesome-swiper'
import 'swiper/dist/css/swiper.min.css'

Vue.use(VueRouter, VueAwesomeSwiper,)

const routes = [
  {
    path: '/movies',
    name: 'Home',
    component: Home,
  },
  {
    path: '/movies/keyword/:keyword_id',
    name: 'KeywordDetail',
    // component: KeywordDetail,
    component: () => import('@/views/movies/KeywordDetail')
  },
  {
    path: '/movies/RecommendedMovieList',
    name: 'RecommendedMovieList',
    // component: KeywordDetail,
    component: RecommendedMovieList,
  },
  {
    path: '/accounts/test',
    name: 'Test',
    component: Test,
  },
  {
    path: '/accounts/mypage',
    name: 'MyPage',
    component: MyPage,
  },
  {
    path: '/accounts/userpage/:user_id',
    name: 'UserPage',
    component: UserPage,
  },
  {
    path: '/movies/survey',
    name: 'SurveyWelcome',
    component: SurveyWelcome,
  },
  {
    path: '/movies/:movie_id',
    name: 'MovieDetail',
    component: MovieDetail,
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
