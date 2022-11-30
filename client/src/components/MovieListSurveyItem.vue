<template>
  <div class="card-wrapper" ref="selectVal" @mouseover='changeHeaderBg' @click="cardSelect">
    <div class="poster-img-box">
      <img class="poster-img"
        :src="`https://image.tmdb.org/t/p/original${movie.poster_path}`"
        alt="poster"
      >
      <div id="check-blank"></div>
    </div>
    <div class="poster-text text-truncate">
      <p class="poster-movie-title">{{ movie.original_title }}</p>
      <p class="poster-movie-subtitle">{{ movie.title }}</p>
    </div>

  </div>
</template>

<script>
export default {
  name: 'MovieListSurveyItem',
  data () {
    return {
      modalMsg : '',
      modalShow : false,
    }
  },
  props: {
    movie: Object,
  },
  components : {
  },
  methods: {
    changeHeaderBg() {
      const headerBg = document.getElementById('header-bg')
      const backdrop = `url(https://image.tmdb.org/t/p/original${this.movie.backdrop_path})`
      headerBg.style.backgroundImage = backdrop
    },
    cardSelect(event) {
      const selectedCard = event.currentTarget
      selectedCard.classList.toggle('selected')
      // 선택 / 선택 취소 에밋으로 올려보내주기 위에서 종합할 것.
      this.$store.commit('SURVEY_ITEM_PICK', this.movie)
      console.log(this.movie)
    },
  },
  computed : {
  }
}
</script>

<style lang="scss" scoped>
.card-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 15rem;
  padding-top: 1rem;
  box-sizing: border-box;
}

.selected{
  .poster-img-box{
    border: 2px solid hsla(37.3,97.5%,52.7%, 0.5);
  }
  #check-blank:before {
    position: absolute;
    top: -5px;
    display: block;
    z-index: 10;
    content: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40' fill='orange' class='bi bi-check' viewBox='0 0 16 16'%3E%3Cpath d='M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.267.267 0 0 1 .02-.022z'/%3E%3C/svg%3E");
  }
}

.poster-img-box{
  display: flex;
  position: relative;
  flex-direction: column;
  width: auto;
  // object-fit: cover;
  aspect-ratio: 3/4;
  overflow: hidden;
  margin: 0;
  border: 1px solid hsla(210,16.7%,97.6%, 0.1);
  border-radius: 5px;
  transition: scale 0.3s;
  /* box-shadow: rgba(255, 255, 255, 0.1) 0px 1px 1px 0px inset, rgba(50, 50, 93, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px; */
  box-shadow: rgba(0, 0, 0, 0.2) 0px 20px 30px;
  /* max-height: 20rem; */
}
.poster-img-box:hover{
  scale: 102%;
}

.poster-img {
  margin: 0;
  max-width: 100%;
  aspect-ratio: 3/4;
  border-radius: 5px;
  object-fit: cover;
}

.poster-text {
  margin: 0;
  text-align: left;
  padding: 20px 5px;
  
}

.poster-movie-title {
  margin: 0;
  font-size: 15px;
  line-height: 15px;
  font-weight: bold;
  margin-bottom: 1rem;
}

.poster-movie-subtitle {
  margin: 0;
  padding: 0;
  font-size: 12px;
  line-height: 12px;
  opacity: 50%;
}


#check-blank {
  display: flex;
  position: absolute;
  right: 0;
  width: 30px;
  height: 30px;
  overflow: hidden;
  background: hsla(210,16.7%,14.5%, 0.5);
  box-shadow: inset 2px 2px 2px #212529;
  // opacity: 50%;
  border-radius: 5px;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0.5rem;
  border: 1px solid hsla(210,16.7%,97.6%, 0.1);
}
</style>