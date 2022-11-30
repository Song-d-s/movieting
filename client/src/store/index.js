import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    loginData : {
      username: '',
      email : '',
      imgUrl : '',
      gender : '',
    },
    isLogin : false,
    // modal visibility
    ReviewModal: false,
    surveyItemPick: [],
    surveyCompletedModal : false,
    loginModal : false,
    inputValidModalShow: false,
  },
  getters: {
  },
  mutations: {
    ISLOGIN_CHANGE(state) {
      state.isLogin = !state.isLogin
    },
    LOGINDATA_IN(state, response){
      console.log('뀹')
      console.log(response)
      state.loginData.username = response.kakao_account.profile.nickname
      state.loginData.email = response.kakao_account.email
      state.loginData.imgUrl = response.kakao_account.profile.profile_image_url
      state.loginData.gender = response.kakao_account.gender
    },
    SURVEY_ITEM_PICK(state, movie){
      let idx = state.surveyItemPick.indexOf(movie)
      if (idx == -1) {
        state.surveyItemPick.push(movie)
      }else{
        state.surveyItemPick.splice(idx, 1);
      }
    },
    SURVEY_COMPLETED_MODAL_CLOSE(state){
      state.surveyCompletedModal = false
    },
    SURVEY_COMPLETED_MODAL_OPEN(state){
      state.surveyCompletedModal = true
    },
    LOGIN_MODAL_CLOSE(state){
      state.loginModal = false
    },
    LOGIN_MODAL_OPEN(state){
      state.loginModal = true
    },
    INPUT_VALID_MODAL_CLOSE(state){
      state.inputValidModalShow = false
    },
    INPUT_VALID_MODAL_OPEN(state){
      state.inputValidModalShow = true
    },
  },
  actions: {
  },
  modules: {
  }
})
