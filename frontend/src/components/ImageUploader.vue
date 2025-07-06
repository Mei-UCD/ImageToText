<template>
  <!-- Upload Box -->
  <label :class="{'upload-box': true, 'shrink': uploadedFiles.length > 0}" @dragover.prevent @drop="handleDrop">
    <input type="file" accept="image/*" multiple @change="handleFileUpload" hidden />
    <img src="/icons/upload.png" alt="Upload Icon" class="upload-icon">
    <p class="info-1" v-if="!previewImage">Drop, Upload or Paste image</p>
    <p class="info-2" v-if="!previewImage">Supported formats: JPG, PNG, GIF, JFIF(JPEG), HEIC, PDF</p>
    <div>
      <input type="file" accept="image/*" multiple ref="fileInput" @change="handleFileUpload" hidden />
      <button class="browse-btn" @click="browseImage">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-upload" viewBox="0 0 16 16">
          <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5"/>
          <path d="M7.646 1.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 2.707V11.5a.5.5 0 0 1-1 0V2.707L5.354 4.854a.5.5 0 1 1-.708-.708z"/>
        </svg>
        Browse
      </button>
    </div>
  </label>

  <!-- Uploaded Files List -->
  <div class="preview-container" v-if="uploadedFiles.length > 0">
    <ul class="image-list">
      <li v-for="(file, index) in uploadedFiles" :key="index" class="image-item">
        <img :src="file.preview" class="preview-thumbnail" @click="openModal(file.preview)"  />
        <span class="file-name">{{ file.name }}</span>

        <!-- <div v-if="file.progress > 0" class="progress-bar-wrapper">
          <div class="progress-bar" :style="{width: file.progress + '%'}"></div>
        </div> -->

        <div v-if="file.loading" class="scrolling-bar-wrapper">
          <div class="scrolling-dot"></div>
        </div>

        <button class="delete-btn" @click="removeImage(index)">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
            <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"/>
          </svg>
        </button>
      </li>
    </ul>

    <!-- Clear All and Convert Button -->
      <div class="action-buttons">
        <button class="clear-btn" @click="clearAll">Clear All</button>
        <button class="convert-btn" @click="convertFiles">
          {{ isConverting ? 'Converting...' : 'Convert' }}
        </button>
      </div>
  </div>

  <!-- Modal for Image Preview -->
  <div v-if="selectedImage" class="modal" @click="closeModal">
  <div class="modal-content">
    <img :src="selectedImage" class="full-image"/>
  </div>
  </div>

</template>

<script setup>
import {ref} from "vue";
import axios from "axios";

const fileInput = ref(null);
const uploadedFiles = ref([]);
const selectedImage = ref(null);

const isConverting = ref(false);

const previewImage = ref(null);
const emit = defineEmits(["convert", "update:imageSrc"]);

const handleFileUpload = (event) =>{
  const files = event.target.files;
  processFile(files);
  event.target.value = null;
};

const handleDrop = (event) => {
  event.preventDefault();
  const files = event.dataTransfer.files;
  processFile(files);
};

const browseImage = () =>{
  fileInput.value.click();
}

const processFile =(files) => {
  let images={};
  for (let file of files) {
    if (file && file.type.startsWith("image/")){
      const previewUrl = URL.createObjectURL(file);
      uploadedFiles.value.push({
        name:file.name,
        file: file,
        preview: previewUrl,
        progress: 0,
      });

      images[file.name] = previewUrl;
    }
  }
  console.log("📸 预览图片:", images);
  emit("update:imageSrc", images);
};

const removeImage = (index) => {
  URL.revokeObjectURL(uploadedFiles.value[index].preview);
  uploadedFiles.value.splice(index, 1);
};

const openModal = (imageSrc) =>{
  selectedImage.value = imageSrc;
}
const closeModal = () =>{
  selectedImage.value = null;
}

const clearAll =() => {
  uploadedFiles.value.forEach(file => URL.revokeObjectURL(file.preview));
  uploadedFiles.value = [];
}

const convertFiles = async() => {
  if (uploadedFiles.value.length === 0){
    alert("Please choose at least one image!");
    return;
  }

  isConverting.value = true;
  const allResults = {};

  for (let file of uploadedFiles.value){
    const formData = new FormData();
    formData.append("images", file.file);

    // file.progress = 1;
    file.loading = true;

    try {
      const response = await axios.post("https://imagetotext-48543926178.asia-northeast1.run.app/ocr", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        // onUploadProgress: (progressEvent) => {
        //   const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        //   file.progress = percentCompleted;
        // },
      });

      //file.progress = 100; // 完成
      allResults[file.name] = response.data[file.name];
    } catch (error) {
      console.error("OCR Failed for", file.name, error);
      //file.progress = 0;
      allResults[file.name] = { error: "Failed to process this image." };
    }

    file.loading = false;
  }

  emit("convert", allResults);
  isConverting.value = false;
};
  


//   let formData = new FormData();
//   uploadedFiles.value.forEach(file => {
//     formData.append("images", file.file);
//     file.progress = 20;
//   });

//   try {
//     const response = await axios.post("http://127.0.0.1:5000/ocr", formData,{
//       headers:{"Content-Type": "multipart/form-data"},
//       onUploadProgress: (progressEvent) => {
//         const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
//         uploadedFiles.value.forEach(file => {
//           file.progress = percentCompleted;
//         });
//       },
//     });

//     uploadedFiles.value.forEach(file => {
//       file.progress = 100;
//     });
//     console.log("📤 OCR 请求成功，返回数据:", response.data);
//     emit("convert", response.data); 
//   } catch (error){
//     console.error("OCR Failed:", error);
//     alert("OCR Detection Failed, Check if backend is running...");
//     uploadedFiles.value.forEach(file => {
//       file.progress = 0;
//     });
//   }finally{
//     isConverting.value = false;
//   }
// };
</script>

<style scoped>


.upload-box {
  width: 100%;
  height: 396px;
  margin: 8px 10px;
  /* margin: auto; */
  border: 2px dashed #ccc;
  border-radius: 15px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: 0.3s;
}

.upload-box.shrink {
  width: 50%;
  margin-left: 20px;
  transition: 0.3s;
}

.upload-box:hover {
  border-color: #5f5f5f;
  background-color: rgba(249, 249, 249, 0.8);
}

.upload-icon{
  width: 80px;
  height: 80px;
  opacity: 0.5;
  display: flex;
}

.info-1 {
  font-size: 18px;
  color: black;
  margin-bottom: 0;
}

.info-2 {
  font-size: 12px;
  color: #ccc;
  margin-top: 0;
}

.browse-btn {
  color: black;
  background-color: rgb(238, 238, 238);
  padding: 8px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 20px;
  margin-bottom: 10px;
}
.browse-btn svg {
  vertical-align: middle;
}
.browse-btn:hover{
  border-color: #ccc !important;
  background-color: #c0c0c0;
}


/* RightSide Images List */
.preview-container {
  width: 50%;
  height: 396px;
  margin: auto 20px;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow-y: auto;
  transition: all 0.3s ease;
}
.preview-container.hidden {
  width: 0; 
}
.image-list {
  list-style: none;
  padding: 0;
  margin: 0;
  width: 100%;
  max-height: 100%;
  overflow-y: auto;
  padding-right: 6px; /* 让滚动条和内容有距离 */
  box-sizing: border-box;
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

.progress-bar-wrapper {
  width: 100%;
  background-color: #f0f0f0;
  height: 6px;
  border-radius: 3px;
  margin-top: 4px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background-color: #42b983;
  transition: width 0.3s;
}


.image-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f8f8f8;
  border-radius: 10px;
  padding: 8px;
  margin-bottom: 10px;
  flex-grow: 1;
}
.preview-thumbnail {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 5px;
  cursor: pointer;
  transition: transform 0.2s;
}
.preview-thumbnail:hover {
  transform: scale(1.1);
}
.file-name {
  flex-grow: 1;
  margin-left: 10px;
  font-size: 14px;
  color: black;
  text-align: left;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.delete-btn {
  background: none; 
  border: none;   
  outline: none;  
  padding: 0;   
}
.delete-btn svg{
  color: gray;
  border: none;
  width: 20px;
  height: 20px;
  cursor: pointer;
  margin-right: 5px;
}

/* Modal Style */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-content {
  max-width: 90%;
  max-height: 90%;
}
.full-image {
  max-width: 100%;
  max-height: 100%;
}

/* Clear All and Convert Buttons */
.action-buttons {
  display: flex;
  justify-content: center;
  gap: 50%;
  width: 100%;
  margin-top: auto;
}
.clear-btn{
  background-color:rgb(238, 238, 238);
  color: black;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.convert-btn {
  background-color:black;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.clear-btn:hover{
  background-color: #c0c0c0;
}
.convert-btn:hover {
  background-color: #3a3a3a;
}


.scrolling-bar-wrapper {
  width: 100%;
  height: 6px;
  background-color: #f0f0f0;
  border-radius: 3px;
  margin-top: 6px;
  overflow: hidden;
  position: relative;
}

.scrolling-dot {
  position: absolute;
  width: 30px;
  height: 100%;
  background-color: #42b983; /* 深绿色横条 */
  border-radius: 3px;
  animation: scrollDot 1.2s linear infinite;
}

@keyframes scrollDot {
  0% {
    left: -30px;
  }
  100% {
    left: 100%;
  }
}





.preview {
  max-width: 100%;
  max-height: 180px;
  object-fit: cover;
}

@media (max-width: 1200px) {
  .upload-box{
    width: 100%;
    margin: 10px;
  }
  .action-buttons {
    gap: 40%; 
    margin-top: auto;
  }

  .clear-btn,
  .convert-btn {
    min-width: 0; 
  }
}
@media (max-width: 1000px) {
  .upload-box{
    width: 100%;
    margin: 10px;
  }
  .action-buttons {
    gap: 35%; 
    margin-top: auto;
  }

  .clear-btn,
  .convert-btn {
    min-width: 0; 
  }
}
@media (max-width: 900px) {
  .upload-box{
    width: 100%;
    margin: 10px;
  }
  .action-buttons {
    gap: 25%; 
    margin-top: auto;
  }

  .clear-btn,
  .convert-btn {
    min-width: 0;
  }
}
@media (max-width: 750px) {
  .upload-box{
    width: 100%;
    margin: 10px;
  }
  .action-buttons {
    gap: 15%; 
    margin-top: auto;
  }

  .clear-btn,
  .convert-btn {
    min-width: 0;
  }
}
@media (max-width: 700px) {
  .upload-box{
    width: 100%;
    margin: 10px;
  }
  .action-buttons {
    gap: 10%; 
    margin-top: auto;
  }

  .clear-btn,
  .convert-btn {
    min-width: 0;
  }
}
@media (max-width: 600px) {
  .upload-box{
    width: 100%;
    margin: 2px;
  }
  .upload-box.shrink {
    width: 100%;
    transition: 0.3s;
    margin: auto auto;  /* 保证水平居中 */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    transition: 0.3s;
  }

  .preview-container {
    width: 100%; /* 预览区域占满宽度 */
    height: auto; /* 根据内容调整高度 */
  }

  .image-list {
    flex-grow: 1;
    margin-top: 10px; /* 给图片列表加点间距 */
  }

  .action-buttons {
    flex-direction: column; /* 按钮纵向排列 */
    gap: 10px; /* 减小按钮之间的间距 */
    margin-top: 10px;
    align-items: center;
  }

  .clear-btn,
  .convert-btn {
    max-width: 120px;
  }
}
</style>

