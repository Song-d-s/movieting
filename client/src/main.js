import Vue from 'vue'
import App from './App.vue'
import router from './router'
import VueCookies from "vue-cookies"
// bootstrap
import "../node_modules/bootstrap/dist/css/bootstrap.css";
import "../node_modules/bootstrap/dist/js/bootstrap.bundle";
import "@/assets/css/bs-custom.css"
import store from './store'
// import 'bootstrap';
// import 'bootstrap/dist/css/bootstrap.min.css';
// import 'bootstrap/scss/bootstrap'
import VModal from 'vue-js-modal'
Vue.use(VModal, { dynamic: true })

//쿠키를 사용한다.
Vue.use(VueCookies);

//쿠키의 만료일은 7일이다. (글로벌 세팅)
Vue.$cookies.config("7d");


Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

// 카카오에서 발급받은 키 입력
window.Kakao.init('카카오에서 발급 받은 키 입력')