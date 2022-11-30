<template>
  <div>
    <div class="row" v-if="commentHave == -1">
      <div id="review-form" class="col d-flex flex-row">
        <!-- create review -->
        <div id="review-btn" @click="setRating(5)">
          <i class="bi bi-hand-thumbs-up-fill"></i>
        </div>
        <div id="review-btn" @click="setRating(0)">
          <i class="bi bi-hand-thumbs-down-fill"></i>
        </div>
        <input type="text"
          v-model="reviewInput"
        >
        <div id="review-btn" @click="createReview">
          <i class="bi bi-pencil-fill" style="font-size: 20px;"></i>
        </div>
      </div>
    </div>
    <!-- comment box -->
    <div class="d-flex flex-column"
      v-for="comment in reverseComments"
        :key="comment.id">
      <div class="vstack gap-3"
        v-if="comment.is_survey==0"
       >
        <div id="review-item">
          <!-- <div ></div> -->
          <div id="review-prof" class="d-flex justify-content-between p-0 pb-2 mb-2">
            <div class="hstack gap-3">
              <div id="profile-pic" class="p-0">
                <!-- 작성자 프로필 -->
                <!-- <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"> -->
                <img :src="comment.imgUrl" alt="">
              </div>
              <div class="vstack">
                <div class="d-flex align-items-center">
                  <div class="hstack gap-2">
                    <p style="font-size: 18px">{{ comment.username }}</p>
                    <div id="rating-tag" v-if="comment.rating!=0" class="bg-success">
                      <i  class="bi bi-hand-thumbs-up-fill"></i>
                    </div>
                    <div id="rating-tag" v-if="comment.rating===0" class="bg-warning">
                      <i class="bi bi-hand-thumbs-down-fill"></i>
                    </div>
                  </div>
                </div>
                <div id="review-date" class="col">
                  {{ new Date(comment.created_at).toDateString() }}
                </div>
              </div>
            </div>

            <div class="hstack gap-3">
              <!-- edit -->
              <div class="col" v-if="comment.user==userId" @click="editReview(comment.content)">
                <i class="bi bi-pencil-square"></i>
              </div>
              <!-- delete -->
              <div class="col" v-if="comment.user==userId" @click="deleteReview(comment)">
                <i class="bi bi-x-lg"></i>
              </div>

            </div>
          </div>

          <!-- edit from -->
          <div v-if="editMode" id="review-form" class="hstack">
            <!-- create review -->
            <div id="review-btn" @click="setRating(5)">
              <i class="bi bi-hand-thumbs-up-fill"></i>
            </div>
            <div id="review-btn" @click="setRating(0)">
              <i class="bi bi-hand-thumbs-down-fill"></i>
            </div>
            <input type="text"
              v-model="reviewInput"
              class="w-100"
            >
            <div id="review-btn" @click="editReviewGo(comment)">
              <i class="bi bi-pencil-fill" style="font-size: 20px;"></i>
            </div>
          </div>

          <!-- <div id="review-form" class="col d-flex flex-row">
            <input type="text" style="width: 100%"
              
            >
          </div> -->
          <div class="row pb-2" style="border-bottom: 1px solid hsla(210,16.7%,97.6%, 0.1);">
            <div class="col" v-if="!editMode">
              {{comment.content}}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
const API_URL = 'http://127.0.0.1:8000'

export default {
  name: 'MovieReview',
  props: {
    movie: Object,
  },
  data() {
    return {
      reviewInput: '',
      rating: null,
      editMode : false,
    }
  },
  methods: {
    createReview(){
      const token = this.$cookies.get('jwt')
      if (this.rating === null || this.reviewInput === '') {
        this.$store.commit('INPUT_VALID_MODAL_OPEN')
        return
      }
      axios({
        method: 'post',
        url: `${API_URL}/movies/${this.movie.id}/comments/`,
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        data: {
          content: this.reviewInput,
          rating: this.rating,
        }
      })
        .then(res=>{
          console.log(res)
        })
        .catch(err=>{
          console.log(err)
        })
      this.rating = null
      this.reviewInput = null
      this.$emit('refresh-request')
    },
    setRating(score) {
      this.rating = score
      console.log(this.rating)
    },
    deleteReview(comment) {
      const token = this.$cookies.get('jwt')
      // const idx = this.movie.comments.findIndex(function(item) {return item.id === comment.id}) // findIndex = find + indexOf
      const idx = this.movie.comments.indexOf(comment) // findIndex = find + indexOf
      if (idx > -1) this.movie.comments.splice(idx, 1)
      axios({
        method: 'delete',
        url: `${API_URL}/movies/comments/${comment.id}/`,
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
      // this.$emit('refresh-request')
    },
    editReview(content) {
      this.editMode = true
      this.reviewInput = content
    },
    editReviewGo(comment){
      if (this.rating === null || this.reviewInput === '') {
        this.$store.commit('INPUT_VALID_MODAL_OPEN')
        return
      }

      const token = this.$cookies.get('jwt')
      axios({
        method: 'put',
        url: `${API_URL}/movies/comments/${comment.id}/`,
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        data: {
          content: this.reviewInput,
          rating: this.rating,
          is_survey : comment.is_survey
        },
      })
      .then(res=>{
        console.log(res)
        this.editMode = false
        comment.content = res.data.content
      })
    }
  },
  computed: {
    commentHave () {
      console.log(this.userId)
      console.log(this.movie.comments)
      for (let i = 0; i < this.movie.comments.length; i ++) {
        if (this.movie.comments[i].user == this.userId) {
          if (this.movie.comments[i].is_survey != 1) {
            return i
          }
        }
      }
      return -1
    },
    reverseComments() {
      let data = this.movie.comments.slice().reverse()
      if(this.commentHave > -1){
        let val = data.splice(this.commentHave, 1)
        data.unshift(val[0])
        return data
      }else{
        return data
      }
    },
    userId () {
      return this.$cookies.get('userId')
    },
  },
  mounted () {
    console.log(this.commentHave)
  }
}
</script>

<style lang="scss" scoped>
  * {
    margin: 0;
    padding: 0;
  }
  #review-form{
    input {
      background-color: #212529;
      color: white;
      border: 1px solid hsla(210,16.7%,97.6%, 0.1);
      border-radius: 5px;
      box-shadow: rgba(0, 0, 0, 0.2) 0px 20px 30px;  
    }

    #review-btn{
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      background-color: #212529;
      width: 3rem;
      height: 3rem;
      border: 1px solid hsla(210,16.7%,97.6%, 0.1);
      box-shadow: rgba(0, 0, 0, 0.2) 0px 20px 30px;    
      border-radius: 50%;
      transition: scale 0.3s;
      overflow: hidden;
      &:hover{
        cursor: pointer;
        scale: 103%;
      }
    }
  }

  #rating-tag{
    display: flex;
    justify-content: center;
    align-items: center;
    aspect-ratio: 1/1;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: 1px solid hsla(210,16.7%,97.6%, 0.1);
    i{
      margin-top: 1px;
      margin-right: 1px;
      font-size: 13px;
    }
  }

  #review-item {
    border-radius: 5px;
    border: 1px solid hsla(210,16.7%,97.6%, 0.1);
    padding: 1rem;
  }

  #profile-pic {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    width: 3rem;
    // min-height: 3rem;
    border: 1px solid hsla(210,16.7%,97.6%, 0.1);
    box-shadow: rgba(0, 0, 0, 0.4) 0px 20px 30px;
    border-radius: 50%;
    img{
      width: 100%;
      aspect-ratio: 1/1;
      object-fit: cover;
    }
  }
  
  #review-prof {
    border-bottom: 1px solid hsla(210,16.7%,97.6%, 0.1);
  }

  #review-date {
    font-size: 11px;
    opacity: 50%;
  }
</style>