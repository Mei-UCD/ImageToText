<template>
  <div class="container">
    <h1 class="title">Image to Text Converter</h1>

    <p class="subtitle">
      An online image to text converter to extract text from images.
    </p>

    <div class="upload-container" :class="{'row-layout': showUploader, 'column-layout': !showUploader}">
      <ImageUploader v-if="showUploader" @convert="handleOCRResult" @update:imageSrc="updateImages" />
      <TextResult v-else :ocrText="ocrText" :imageSrc="imageSrc" @clear="handleClear" />
    </div>

    <p class="info-privacy">
      Your privacy is protected! No data is transmitted or stored.
    </p>

    <!-- Anouncement Bottom -->
   <div class="footer">
    <span class="footer-text">Rate your experience:</span>
    <div class="rating">
      <!--Rate your experience: ⭐⭐⭐⭐⭐ -->
      <span
        v-for="star in [5, 4, 3, 2, 1]"
        :key="star"
        class="star"
        :class="{ filled: star <= selectedRating}"
        @click="selectRating(star)"
        @mouseover="hoverRating = star"
        @mouseleave="hoverRating = 0"
      >
        ★
      </span>
    </div>
   </div>

  </div>
</template>

<script setup>
import { ref } from "vue";
import ImageUploader from "./components/ImageUploader.vue";
import TextResult from "./components/TextResult.vue";

const showUploader = ref(true);
const ocrText = ref({});
const imageSrc = ref({});

const handleOCRResult = (text) => {
  console.log("📥 收到 OCR 结果:", text);
  ocrText.value = text; 
  showUploader.value = false;
};

const handleClear =() =>{
  ocrText.value = {};
  showUploader.value = true;
};

// const updateImages = (images) => {
//   imageSrc.value = images;
// };
const updateImages = (images) => {
  Object.assign(imageSrc.value, images);
};


const selectedRating = ref(0);
const hoverRating = ref(0);
const selectRating = (rating) => {
  selectedRating.value = rating;
  console.log("⭐ 你打了分:", rating);
};

</script>

<style>
html, body {
  width: 100%;
  min-height: 100%;
  background-color: #f9f9f9 !important;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: auto;
}
.container{
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0 5vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  min-height: 100%;
}
.title {
  text-align: center;
  width: 100%;
  color: black;
  font-size: 32px;
  font-weight: bold;
  margin: 20px 0 0 0;
}
.subtitle {
  text-align: center;
  font-size: 16px;
  color: gray;
  margin-bottom: 50px;
}

.upload-container {
  width: 100%;
  text-align: center;
  align-items: center;
  display: flex;
  background-color: #ffffff;
  border-radius: 20px;
  overflow-y: auto;
  min-height: 400px;
  overflow-x: hidden;
}
.row-layout {
  flex-direction: row; /* ImageUploader 时 */
}
.column-layout {
  flex-direction: column; /* TextResult 时 */
}

.info-privacy {
  font-size: 13px;
  color: #767676;
}

@media (max-width: 600px) {
  .upload-container{
    width: 90%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    padding: 10px;
  }
}



::-webkit-scrollbar{
  width: 6px;
}
::-webkit-scrollbar-track{
  background: rgb(235, 235, 235);
  margin: 4px;
  border-radius: 6px;
}
::-webkit-scrollbar-thumb{
  background: rgb(198, 239, 198);
  border-radius: 6px;
  /* border: 2px solid transparent; */
  background-clip: content-box;
  min-height: 10px;
}
::-webkit-scrollbar-thumb:hover{
  background: rgb(170, 224, 177);
}

.footer {
  margin-top: 10px;
  margin-bottom: 10px;
  font-size: 14px;
  color: #888;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}
.rating {
  display: flex;
  flex-direction: row-reverse;
  justify-content: center;
}

.star {
  font-size: 24px;
  cursor: pointer;
  color: #ccc;
  transition: color 0.2s;
}

.star.filled,
.star:hover,
.star:hover ~ .star {
  color: gold;
}

/* .star.filled,
.star:hover{
  color: gold;
} */

</style>


