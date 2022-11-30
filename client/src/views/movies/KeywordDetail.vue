<template>
  <div>
    <div class="row">
      <div id="keywordTag" class="hstack gap-3 rounded-pill bg-success ms-3 me-3 mb-2 mt-1 d-flex align-items-center col-auto pe-3 shadow ">
        <i class="bi bi-tags-fill ms-3 fs-4"></i>
        <p class="fw-bold fs-3">{{ keyword.name }}</p>
        <div class="vr"></div>
        <p class="opacity-50">{{ movies.length }}편</p>
      </div>
      <div class="w-100 col"></div>
    </div>
    <!-- swiper -->
    <swiper ref="filterSwiper" :options="swiperOption" role="tablist">
      <swiper-slide role="tab" v-for="movie in movies" :key=movie.id>
        <MovieListItem
          :movie=movie
        />
      </swiper-slide>
    </swiper>
  </div>
</template>

<script>
import axios from 'axios'
import { swiper, swiperSlide } from 'vue-awesome-swiper'

import MovieListItem from '@/components/MovieListItem'

const API_URL = 'http://127.0.0.1:8000'

export default {
  name: 'KeywordDetail',
  data() {
    return {
      keyword_id: this.$route.params.keyword_id,
      keyword: null,
      movies: null,
      // swiper
      swiperOption: {
        // direction: 'vertical',
        slidesPerView: 4,
        slidesPerColumn: 2,
        spaceBetween: 35, // swiper-slide 사이의 간격 지정
        slidesOffsetBefore: -15, // slidesOffsetBefore는 첫번째 슬라이드의 시작점에 대한 변경할 때 사용
        slidesOffsetAfter: 0, // slidesOffsetAfter는 마지막 슬라이드 시작점 + 마지막 슬라이드 너비에 해당하는 위치의 변경이 필요할 때 사용
        freeMode: true, // freeMode를 사용시 스크롤하는 느낌으로 구현 가능
        centerInsufficientSlides: false, // 컨텐츠의 수량에 따라 중앙정렬 여부를 결정함
        // mousewheel: true,

        autoplay: {
          disableOnInteraction: false,
        },
      }
    }
  },
  components: {
    swiper,
    swiperSlide,
    MovieListItem,
  },
  methods: {
    change () {
      console.log('에밋 원 됨')
      // this.$emit('change')
    },
    getKeyword() {
      axios({
        method: 'get',
        url: `${API_URL}/movies/keyword/${this.keyword_id}/`
      })
        .then((res) => {
          console.log(res)
          const keyword = {
            'id': res.data.id,
            'name': res.data.name,
          }
          this.keyword = keyword
          this.movies = res.data.movie_keywords
        })
        .catch((err)=>{
          console.log(err)
        })
    }
  },
  mounted() {
    this.getKeyword()
  }
}
</script>

<style lang="scss" scoped>
* {
  padding:0;
  margin: 0;
}

.swiper-container {
  padding: 0 30px;
  &:before,
  &:after {
    display: block;
    position: absolute;
    top: 0;
    width: 30px;
    height: 100%;
    z-index: 8;
    content: "";
  }
  &:before {
    left: 0;
    background: linear-gradient(90deg, #212529 -10%, rgba(33, 37, 41, 0.8) 18.31%, rgba(33, 37, 41, 0) 75%);
  }
  &:after {
    right: 0;
    background: linear-gradient(270deg, #212529 -10%, rgba(33, 37, 41, 0.8) 18.31%, rgba(33, 37, 41, 0) 75%);
  }
}

.swiper-container {
  .swiper-wrapper {
    .swiper-slide {
      width: auto;
      min-width: 50px;
      font-size: 14px;
      line-height: 36px;
      text-align: center;
      border: 0;
      appearance: none;
      cursor: pointer;
      justify-content: center;
      display: flex;
    }
  }
}
.swiper-button-next {
  background: url('https://upload.wikimedia.org/wikipedia/commons/4/48/BLANK_ICON.png') no-repeat;
  background-size: 50% auto;
  background-position: center;
}

.swiper-button-prev {
  background: url('https://upload.wikimedia.org/wikipedia/commons/4/48/BLANK_ICON.png') no-repeat;
  background-size: 50% auto;
  background-position: center;
}
</style>