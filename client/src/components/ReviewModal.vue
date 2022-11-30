<template>
  <div class="modal-mask" @click="$emit('close-modal')">
    <div class="modal-wrapper">
      <div class="modal-container">
        <div class="vstack">
          <div class="modal-title">
            <p>해당 기능은 로그인이 필요합니다.</p>
            <p>로그인하시겠습니까?</p>
          </div>
          <div class="modal-btn hstack">
            <div>로그인</div>
            <div>취소</div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<style lang="scss" scoped>
* {
  margin: 0;
  padding: 0;
}
.modal-mask{
  position: fixed;
  z-index: 9999;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  transition: opacity 0.3s ease;
}

.modal-wrapper{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;  
  width: 100%;
  height: 100%;
  align-items: center
}

.modal-container{
  width: 30%;
  height: 15%;
  padding: 1rem;
  background: hsla(210,10.8%,14.5%, 0.7);
  border: 1px solid hsla(210,16.7%,97.6%, 0.1);
  // blur
  -webkit-backdrop-filter: blur(8px);
  backdrop-filter: blur(8px);

  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  border-radius: 5px;
  transition: all 0.5s ease;
  overflow: hidden;
  color:#e8eddf;
  .modal-title{
    // border-bottom: 1px solid hsla(210,16.7%,97.6%, 0.1);
    padding-bottom: 1rem;
  }
}
.modal-btn{
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  div{
    width: 100px;
    text-align: justify-all;
    border-radius: 30px;
    border: 1px solid hsla(210,16.7%,97.6%, 0.1);
    padding: .5rem;
    &:hover{
      cursor: pointer;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
    }
  }
}
</style>