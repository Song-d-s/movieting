<template>
  <swiper ref="filterSwiper" :options="swiperOption" role="tablist">
    <swiper-slide role="tab" v-for="actor in actors" :key=actor.id>
      <div id="cast-card">
        <div id="profile-pic">
          <img v-show="actor.profile_path" :src="`http://image.tmdb.org/t/p/original${actor.profile_path}`" alt="">
          <i v-show="!actor.profile_path" class="bi bi-person-circle" style="font-size: 50px"></i>
        </div>
        <p>{{ actor.name }}</p>
      </div>
    </swiper-slide>
    <!-- <div class="swiper-button-prev" slot="button-prev">
      <i class="bi bi-caret-left-fill"></i>
    </div>
    <div class="swiper-button-next" slot="button-next">
      <i class="bi bi-caret-right-fill"></i>
    </div> -->
  </swiper>
</template>

<script>
import { swiper, swiperSlide } from 'vue-awesome-swiper'

export default {
  name: 'CastList',
  data() {
    return {
      swiperOption: {
        slidesPerView: 3,
        spaceBetween: 35, // swiper-slide 사이의 간격 지정
        slidesOffsetBefore: -15, // slidesOffsetBefore는 첫번째 슬라이드의 시작점에 대한 변경할 때 사용
        slidesOffsetAfter: 0, // slidesOffsetAfter는 마지막 슬라이드 시작점 + 마지막 슬라이드 너비에 해당하는 위치의 변경이 필요할 때 사용
        freeMode: true, // freeMode를 사용시 스크롤하는 느낌으로 구현 가능
        centerInsufficientSlides: true, // 컨텐츠의 수량에 따라 중앙정렬 여부를 결정함
        autoplay: {
          disableOnInteraction: false,
        },
        // navigation: {
        //   nextEl: '.swiper-button-next',
        //   prevEl: '.swiper-button-prev'
        // }
      }
    }
  },
  components: {
    swiper,
    swiperSlide,
  },
  props: {
    actors: Array,
  }
}
</script>

<style lang="scss" scoped>
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
}

#cast-card {
  width: 200px;
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
</style>