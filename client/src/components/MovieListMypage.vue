<template>
  <div>
    <div id="title" class="d-flex">
      <h3>보고 싶어요❤️ </h3>
    </div>
    <swiper ref="filterSwiper" :options="swiperOption" role="tablist">
      <swiper-slide role="tab" v-for="(movie, index) in movies" :key=movie.id >
        <MovieListMypageItem :index=index :movie=movie class="swiper-lazy"/>
      </swiper-slide>
      <div class="swiper-button-prev" slot="button-prev">
        <i class="bi bi-caret-left-fill"></i>
      </div>
      <div class="swiper-button-next" slot="button-next">
        <i class="bi bi-caret-right-fill"></i>
      </div>
    </swiper>
  </div>
</template>

<script>
import { swiper, swiperSlide } from 'vue-awesome-swiper'

import MovieListMypageItem from '@/components/MovieListMypageItem'

export default {
  name: 'MovieListMypage',
  data() {
    return {
      swiperOption: {
        slidesPerView: 5,
        spaceBetween: 30, // swiper-slide 사이의 간격 지정
        slidesOffsetBefore: 0, // slidesOffsetBefore는 첫번째 슬라이드의 시작점에 대한 변경할 때 사용
        slidesOffsetAfter: 0, // slidesOffsetAfter는 마지막 슬라이드 시작점 + 마지막 슬라이드 너비에 해당하는 위치의 변경이 필요할 때 사용
        freeMode: false, // freeMode를 사용시 스크롤하는 느낌으로 구현 가능
        // mousewheel: true,
        lazy: true,
        centerInsufficientSlides: true, // 컨텐츠의 수량에 따라 중앙정렬 여부를 결정함
        autoplay: {
          disableOnInteraction: true,
        },
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev'
        }
      }
    }
  },
  props: {
    movies: Array,
  },
  components: {
    MovieListMypageItem,
    swiper,
    swiperSlide,
  },
  methods: {
  },
  created() {
  },
  mounted() {
  }
}
</script>

<style lang="scss" scoped>
.swiper-container {
  padding: 0 30px; // 여백값을 지정할 경우 슬라이드의 시작점과 종점이 이에 영향을 받아 변경됨
  &:before,
  &:after { // 가상선택자를 활용하여 그라데이션 값 추가
    display: block;
    position: absolute;
    top: 0;
    width: 30px; // container에 준 여백값보다 크지 않게 사이즈 지정하기 (swiper-slide의 클릭 이벤트에 영향을 주지 않고, 이렇게 지정해야 그라데이션이 영역 내부에 있는 탭이 스크롤 하기 전엔 영향을 주지 않음)
    height: 100%;
    z-index: 8;
    content: "";
  }
  &:before {
    left: 0;
    background: linear-gradient(90deg, #212529 -10.19%, rgba(33, 37, 41, 0.8) 18.31%, rgba(33, 37, 41, 0) 75%);
  }
  &:after {
    right: 0;
    background: linear-gradient(270deg, #212529 -10.19%, rgba(33, 37, 41, 0.8) 18.31%, rgba(33, 37, 41, 0) 75%);
  }
  //...중략
}

.swiper-container {
  .swiper-wrapper {
    .swiper-slide {
      // width: auto; // auto 값을 지정해야 슬라이드의 width값이 텍스트 길이 기준으로 바뀜
      min-width: 56px; // min-width를 지정하지 않을 경우 텍스트가 1개 내지는 2개가 들어갈 때 탭 모양이 상이할 수 있으므로 넣어준다.
      // padding: 0px 14px;
      font-size: 14px;
      line-height: 36px;
      text-align: center;
      // color: #84868c;
      border: 0;
      // border-radius: 18px;
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

// .swiper-button-next::after,
// .swiper-button-prev::after {
//   display: none;
// }

#title {
  margin: 0rem 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid hsla(210,16.7%,97.6%, 0.1);
}
</style>