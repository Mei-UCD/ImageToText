<template>
  <!-- Title -->
  <div class="header">
    <h3>Result ({{ Object.keys(ocrText).length }})</h3>

    <div class="header-buttons">
      <button class="downloadall-btn" @click="downloadAllTexts">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#333" class="bi bi-download" viewBox="0 0 16 16">
          <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5"/>
          <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708z"/>
        </svg>
        Download All
      </button>

      <button class="startover-btn" @click="$emit('clear')">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-clockwise" viewBox="0 0 16 16">
          <path fill-rule="evenodd" d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2z"/>
          <path d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466"/>
        </svg>
        StartOver
      </button>
    </div>

  </div>

  <!-- Recognition Part -->
  <div v-if="ocrText && Object.keys(ocrText).length > 0" class="result-items">
    <div v-for="(text, filename) in ocrText" :key="filename" class="result-box" >
      <!-- Image and Character Result -->
        <div class="image-container">
          <img :src="imageSrc[filename]" alt="Uploaded Image" class="thumbnail" @click="openPreview(imageSrc[filename])" />
          <p>{{ truncatedFilename(filename) }}</p>
          <!-- Preview the Big Image -->
          <div v-if="showPreview" class="preview-overlay" @click="closePreview">
            <img :src="selectedImage" class="preview-image" />
          </div>
        </div>

        <!-- <div class="text-container">
          <textarea
          :ref="el => {
          if (!textAreaRefs) textAreaRefs = {};
          textAreaRefs[filename] = el;
        }"
        v-model="textMap[filename]"
        class="text-box"
        :class="expandedBoxes[filename] ? 'text-expanded' : 'text-collapsed'"
        @input="adjustHeight"
      />
        </div> -->

        <div class="text-container" style="position: relative; width: 100%; height: 300px; border: 1px solid #ddd; overflow: auto;">
          <span
            v-for="(item, idx) in ocrText[filename]"
            :key="idx"
            class="overlay-text"
            :style="{
              position: 'absolute',
              left: item.x + 'px',
              top: item.y + 'px',
              fontSize: 10 + 'px',
            }"
          >
            {{ item.text }}
          </span>
        </div>


        <!-- Operation Buttons -->
         <div class="action-buttons">
          <button class="copy-btn" @click="copyText(text, filename)" @mouseover="handleCopyMouseOver(filename)" @mouseleave="handleCopyMouseLeave(filename)">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#333" class="bi bi-copy" viewBox="0 0 16 16">
              <path fill-rule="evenodd" d="M4 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2zm2-1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 5a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-1h1v1a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h1v1z"/>
            </svg>
            <span v-if="showCopyTooltip[filename]" class="tooltip">{{ copyTooltipText[filename] }}</span>
          </button>

          <button class="download-btn" @click="downloadText(text, filename)" @mouseover="handleDownloadMouseOver(filename)" @mouseleave="handleDownloadMouseLeave(filename)">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#333" class="bi bi-download" viewBox="0 0 16 16">
              <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5"/>
              <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708z"/>
            </svg>
            <span v-if="showDownloadTooltip[filename]" class="tooltip">{{ downloadTooltipText[filename] }}</span>
          </button>

          <!-- <button class="expand-btn" v-if="!expandedBoxes[filename]" @click="expandBox(filename)" @mouseover="handleExpandMouseOver(filename)" @mouseleave="handleExpandMouseLeave(filename)">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#333" class="bi bi-arrows-angle-expand" viewBox="0 0 16 16">
              <path fill-rule="evenodd" d="M5.828 10.172a.5.5 0 0 0-.707 0l-4.096 4.096V11.5a.5.5 0 0 0-1 0v3.975a.5.5 0 0 0 .5.5H4.5a.5.5 0 0 0 0-1H1.732l4.096-4.096a.5.5 0 0 0 0-.707m4.344-4.344a.5.5 0 0 0 .707 0l4.096-4.096V4.5a.5.5 0 1 0 1 0V.525a.5.5 0 0 0-.5-.5H11.5a.5.5 0 0 0 0 1h2.768l-4.096 4.096a.5.5 0 0 0 0 .707"/>
            </svg>
            <span v-if="showExpandTooltip[filename]" class="tooltip">{{ expandTooltipText[filename] }}</span>
          </button> -->

          <button class="close-btn" v-if="expandedBoxes[filename]" @click="revertBox(filename)" @mouseover="handleCloseMouseOver(filename)" @mouseleave="handleCloseMouseLeave(filename)" >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#333" class="bi bi-arrows-angle-contract" viewBox="0 0 16 16">
              <path fill-rule="evenodd" d="M.172 15.828a.5.5 0 0 0 .707 0l4.096-4.096V14.5a.5.5 0 1 0 1 0v-3.975a.5.5 0 0 0-.5-.5H1.5a.5.5 0 0 0 0 1h2.768L.172 15.121a.5.5 0 0 0 0 .707M15.828.172a.5.5 0 0 0-.707 0l-4.096 4.096V1.5a.5.5 0 1 0-1 0v3.975a.5.5 0 0 0 .5.5H14.5a.5.5 0 0 0 0-1h-2.768L15.828.879a.5.5 0 0 0 0-.707"/>
            </svg>
            <span v-if="showCloseTooltip[filename]" class="tooltip">{{ closeTooltipText[filename] }}</span>
          </button>
         </div>
      
    </div>

  </div>
</template>

<script setup>
  // import {ref, watch} from 'vue';
  // import {reactive, watchEffect, nextTick} from 'vue';
  import { ref, reactive, watchEffect, watch, nextTick } from 'vue';
  import { onMounted } from 'vue';
  import { toRaw } from 'vue';

  const showPreview = ref(false);
  const selectedImage = ref(null);
  const props = defineProps(['ocrText', 'imageSrc']);
  defineEmits(["clear"]);

  const truncatedFilename = (filename) => {
    const name = filename.substring(0, filename.lastIndexOf('.'));
    const extension = filename.substring(filename.lastIndexOf('.'));
    const truncatedName = name.length > 10 ? name.substring(0, 10) + '...' : name;
    const result = truncatedName + extension;
    return result;
  };

  const openPreview = (image) => {
    selectedImage.value = image;
    showPreview.value = true;
  };

  const closePreview = () => {
    showPreview.value = false;
  };

  // 定义本地响应式状态对象
  const showCopyTooltip = reactive({})
  const showDownloadTooltip = reactive({})
  const showExpandTooltip = reactive({})
  const showCloseTooltip = reactive({})
  const copyTooltipText = reactive({})
  const downloadTooltipText = reactive({})
  const expandTooltipText = reactive({})
  const closeTooltipText = reactive({})
  const expandedBoxes = reactive({})
  const textMap = reactive({});
  const textAreaRefs = reactive({});

  onMounted(() => {
    console.log('textAreaRefs after mounted:', textAreaRefs);  // 确认 textAreaRefs 在 mounted 后是否正确初始化
  });

  function initStatesFromProps() {
  for (const filename in props.ocrText) {
    showCopyTooltip[filename] ??= false
    showDownloadTooltip[filename] ??= false
    showExpandTooltip[filename] ??= false
    showCloseTooltip[filename] ??= false

    copyTooltipText[filename] ??= 'copy'
    downloadTooltipText[filename] ??= 'download'
    expandTooltipText[filename] ??= 'expand'
    closeTooltipText[filename] ??= 'close'

    expandedBoxes[filename] ??= false
    }
  }
  // 监听 props.ocrText 变化时自动初始化
  watchEffect(() => {
    if (props.ocrText) {
      initStatesFromProps()
    }
  })


  // Result Layout Function
  function generateTextByLayout(ocrItems){
    if (!ocrItems || !ocrItems.length) {
      return "";
    }

    const lineThreshold = 10;
    const lines = [];

    // Step 1: sort by y position
    ocrItems.sort((a, b) => a.y - b.y);
    for (const item of ocrItems){
      let placed = false;
      for (const line of lines){
        const avgY = line.reduce((sum, i) => sum + i.y, 0) / line.length;
        if (Math.abs(item.y - avgY) <= lineThreshold){
          line.push(item);
          placed = true;
          break;
        }
      }
      if (!placed){
        lines.push([item]);
      }
    }

    // Step 2: sort by X position
    const result = lines
      .map((line) => line.sort((a, b) => a.x - b.x).map(i => i.text).join(' '))
      .join('\n');
    
    return result;
  }



  // Action Buttons Functions
  // (1) Copy Button
  function copyText(text, filename) {
    // navigator.clipboard.writeText(text).then(()=>{
    //   copyTooltipText[filename] = "Copied";
    //   showCopyTooltip[filename] = true;
    // })

    const items = props.ocrText[filename];
    const textByLayout = generateTextByLayout(items);
    navigator.clipboard.writeText(textByLayout).then(()=>{
      copyTooltipText[filename] = "Copied";
      showCopyTooltip[filename] = true;
    });
  }
  function handleCopyMouseOver(filename){
    showCopyTooltip[filename] = true
    copyTooltipText[filename] = "Copy"
  }
  function handleCopyMouseLeave(filename){
    showCopyTooltip[filename] = false
  }

  // (2) Download Button
  function downloadText(text, filename){
    // const blob = new Blob([text], {type: "text/plain;charset=utf-8"})
    // const link = document.createElement("a")
    // link.href=URL.createObjectURL(blob)
    // link.download = filename.endsWith('.txt')?filename : `${filename}.txt`
    // link.click()
    // URL.revokeObjectURL(link.href)

    // downloadTooltipText[filename] = "Downloaded"
    // showDownloadTooltip[filename] = true

    const items = props.ocrText[filename];
    const textByLayout = generateTextByLayout(items);
    const blob = new Blob([textByLayout], {type: "text/plain;charset=utf-8"});
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = filename.endsWith(".txt") ? filename : `${filename}.txt`;
    link.click();
    URL.revokeObjectURL(link.href);

    downloadTooltipText[filename] = "Downloaded";
    showDownloadTooltip[filename] = true;
  }
  function handleDownloadMouseOver(filename) {
    showDownloadTooltip[filename] = true
    downloadTooltipText[filename] = "Download"
  }
  function handleDownloadMouseLeave(filename){
    showDownloadTooltip[filename] = false
  }

  // Expand Button
  watch(
    ()=>props.ocrText,
    (newVal) => {
      if (newVal) {
        for (const filename in newVal) {
          textMap[filename] = newVal[filename];
          expandedBoxes[filename] = false;
        }
      }
    },
    {immediate: true}
  )

  function expandBox(filename){
    console.log("Expanding:", filename, "textAreaRefs:", textAreaRefs);
    expandedBoxes[filename] = true;
    nextTick(() =>{
      console.log("After nextTick:", filename, "textAreaRefs:", textAreaRefs);
      adjustHeight(filename);
    });
  }
  function adjustHeight(filename) {
    const el = textAreaRefs[filename];
    console.log("Adjusting height for:", filename, "Element:", el);
    if (el) {
      console.log('Before adjust: ', el.scrollHeight);
      el.style.height = 'auto';
      el.style.height = el.scrollHeight + 'px';
      console.log('After adjust: ', el.scrollHeight);
      console.log('Textarea new height: ', el.style.height);
    }else {
      console.log('No textarea element found for:', filename); // 输出没有找到元素的信息
    }
  }

  function handleExpandMouseOver(filename){
    showExpandTooltip[filename] = true
    expandTooltipText[filename] = "Expand"
  }
  function handleExpandMouseLeave(filename) {
    showExpandTooltip[filename] = false
  }

  // Close Button
  function revertBox(filename){
    expandedBoxes[filename] = false;

    const textarea = textAreaRefs[filename];
    if (textarea){
      textarea.style.height = '6em';
      console.log('收起后的高度:', textarea.offsetHeight, 'px');
    }
  }
  function handleCloseMouseOver(filename) {
    showCloseTooltip[filename] = true
    closeTooltipText[filename] = "Close"
  }
  function handleCloseMouseLeave(filename) {
    showCloseTooltip[filename] = false
  }

  const downloadAllTexts = () => {
    const rawMap = toRaw(textMap); // 确保是普通对象
    for (const [filename, text] of Object.entries(rawMap)) {
      // 提取 base 名字（去掉扩展名）
      const baseName = filename.substring(0, filename.lastIndexOf('.')) || filename;

      // 创建文本 blob
      const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);

      // 创建 <a> 标签模拟点击
      const a = document.createElement('a');
      a.href = url;
      a.download = `${baseName}.txt`;
      document.body.appendChild(a);
      a.click();

      // 清理
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  };


</script>

<!-- <script setup>
import { computed } from "vue";
import {ref, reactive, watch, nextTick} from "vue";

const showPreview = ref(false);
const selectedImage = ref(null);
const showCopyTooltip = reactive({});
const copyTooltipText = reactive({});

const showDownloadTooltip = reactive({});
const downloadTooltipText = reactive({});

const expandedBoxes = reactive({});
const textareaRefs = ref({});

const showExpandTooltip = reactive({});
const expandTooltipText = reactive({});

const showCloseTooltip = reactive({});
const closeTooltipText = reactive({});

const props = defineProps(['ocrText', 'imageSrc']);
defineEmits(["clear"]);
// 使用 reactive 使 editableText 成为响应式对象
//const editableText = reactive({});
const editableText = reactive({ ...props.ocrText });

watch(() => props.ocrText, (newVal) => {
  if (newVal) {
    Object.keys(newVal).forEach((filename) => {
      if (!copyTooltipText[filename]) {
        copyTooltipText[filename] = 'Copy';
      }

       if (!downloadTooltipText[filename]) {
          downloadTooltipText[filename] = "Download";
      }

      if (!expandTooltipText[filename]) {
          expandTooltipText[filename] = "Expand";
      }
      // if (!closeTooltipText[filename]) {
      //     closeTooltipText[filename] = "Close";
      // }
      if (!expandedBoxes[filename]) {
        expandedBoxes[filename] = false;  // ✅ 确保默认值为 false
      }

    });
  }
}, { immediate: true });



const truncatedFilename = (filename) => {
  const name = filename.substring(0, filename.lastIndexOf('.'));
  const extension = filename.substring(filename.lastIndexOf('.'));

  const truncatedName = name.length > 10 ? name.substring(0, 10) + '...' : name;

  const result = truncatedName + extension;
  return result;
};

const openPreview = (image) => {
  selectedImage.value = image;
  showPreview.value = true;
};

const closePreview = () => {
  showPreview.value = false;
};

const copyText = (text, filename) => {
  navigator.clipboard.writeText(text).then(() => {
    tooltipText[filename] = 'Copied!';
    setTimeout(() => {
      tooltipText[filename] = 'Copy';
    }, 1000);
  });
};

const downloadText = (text, filename) => {
  const blob = new Blob([text], {type:"text/plain"});
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `${filename}.txt`;
  link.click();

  downloadTooltipText[filename] = "Downloaded!";
  setTimeout(() => {
    downloadTooltipText[filename] = "Download";
  }, 1000);
}


const setRef = (filename) => {
  return (el) => {
    if (el) {
      textareaRefs.value[filename] = el;  // 动态地将 `textarea` 元素存储到 `textareaRefs` 对象中
    } else {
      delete textareaRefs.value[filename];  // 清理不再存在的元素
    }
  };
};
const expandBox = (filename) => {
  console.log('expanding box for:', filename);
  if (!filename || !(filename in props.ocrText)) {
    console.error(`Error: filename '${filename}' not found in ocrText`, props.ocrText);
    return;
  }
  //expandedBoxes.value[filename] = !expandedBoxes.value[filename];
  expandedBoxes[filename] = true;

  nextTick(() => {
    console.log('textareaRefs.value:', textareaRefs.value); 
    adjustHeight(filename);
    handleExpandMouseLeave(filename);
    handleCloseMouseOver(filename);
  });
}

const adjustHeight = (filename) => {
  nextTick(() => {
    const textarea = textareaRefs.value[filename];
    if (textarea && expandedBoxes[filename]) {
      textarea.style.height = "auto";  // 重置高度
      // textarea.style.height = textarea.scrollHeight + "px";  // 调整为内容的高度
      // textarea.style.paddingTop = "10px";  // 在顶部增加额外的距离
      // textarea.style.paddingBottom = "10px";  
      const contentHeight = textarea.scrollHeight;

      // 给上、下增加额外的边距（比如10px）
      const paddingTop = 10;
      const paddingBottom = 10;

      // 设置新的高度，包含上下的内边距
      textarea.style.height = (contentHeight + paddingTop + paddingBottom) + "px";

      // 设置 padding
      textarea.style.paddingTop = paddingTop + "px";
      textarea.style.paddingBottom = paddingBottom + "px";
    } else {
      console.error(`Textarea for ${filename} not found.`);
    }
  });
};

const revertBox = (filename) => {
  console.log('Reverting box for:', filename);
  if (!filename || !(filename in props.ocrText)) {
    console.error(`Error: filename '${filename}' not found in ocrText`, props.ocrText);
    return;
  }

  expandedBoxes[filename] = false; // 只控制收起框状态
  nextTick(() => {
    adjustHeight(filename);
    handleCloseMouseLeave(filename);
    handleExpandMouseOver(filename);
  });
};

// 鼠标悬浮事件
const handleExpandMouseOver = (filename) => {
  showExpandTooltip[filename] = true;
};

const handleExpandMouseLeave = (filename) => {
  if (!expandedBoxes[filename]) {
    showExpandTooltip[filename] = false;
  }
};

const handleCloseMouseOver = (filename) => {
  showCloseTooltip[filename] = true;
};

const handleCloseMouseLeave = (filename) => {
  if (expandedBoxes[filename]) {
    showCloseTooltip[filename] = false;
  }
};

const handleCopyMouseOver = (filename) => {
  showCopyTooltip[filename] = true;
};

const handleCopyMouseLeave = (filename) => {
  if (!expandedBoxes[filename]) {
    showCopyTooltip[filename] = false;
  }
};

const handleDownloadMouseOver = (filename) => {
  showDownloadTooltip[filename] = true;
};

const handleDownloadMouseLeave = (filename) => {
  if (!expandedBoxes[filename]) {
    showDownloadTooltip[filename] = false;
  }
};




</script> -->

<style scoped>
/* Header */
.header {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  font-size: 15px;
}
h3 {
  color: black;
  text-align: left;
  margin-left: 10px;
  margin-bottom: 0;
}
.header-buttons {
  display: flex;
  gap: 0.5rem; /* 两个按钮之间的间距 */
}
.startover-btn{
  background-color:rgb(238, 238, 238);
  color: black;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  margin-right: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 10px;
}
.startover-btn svg {
  vertical-align: middle;
}
.startover-btn:hover{
  border-color: #ccc !important;
  background-color: #e0e0e0;
}

.downloadall-btn {
  background-color:rgb(238, 238, 238);
  color: black;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  margin-right: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 10px;
}
.downloadall-btn:hover {
  background-color: #e0e0e0;
}




/* Result */
.result-items{
  width: 100%;
}
.result-box{
  /* height: 100px; */
  /* height: auto !important; */
  position: relative;
  min-height: 100px; /* 避免收缩过小 */
  margin: 10px;
  padding-top: 5px;
  padding-bottom: 5px;
  display: flex;
  flex-direction: row;
  /* align-items: center; */
  background: white;
  border-radius: 8px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}
.image-container{
  flex: 0 0 100px;
  padding-left: 10px;
  padding-right: 10px;
  border-right: 2px solid #e9e9e9;
}
.image-container p{
  margin-top: 0px;
  margin-bottom: 0px;
  color: black;
  font-size: 10px;
}
.thumbnail {
  width: 100px;
  height: 80px;
  object-fit: cover;
  cursor: pointer;
  border-radius: 5px;
  transition: transform 0.2s;
  overflow: hidden;
}
.thumbnail:hover {
  transform: scale(1.1);
}
.preview-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.preview-image {
  max-width: 90vw;   /* 让图片最大宽度是屏幕的 90% */
  max-height: 90vh;  /* 让图片最大高度是屏幕的 90% */
  object-fit: contain;
}

.text-container {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  width: 100%;
  font-size: 10px;
  flex: 1;
  color: #333;
  background-color: #fff;
  justify-content: center;
}
textarea {
  width: 100% !important;
  /* min-height: 80px;  */
  border: none;
  padding: 0 10px;
  font-size: 14px;
  resize: none;
  background-color: #fff; 
  color: #333; 
  box-sizing: border-box; 
  outline: none; 
  overflow-y: auto; /* 启用垂直滚动 */
  overflow-x: hidden; /* 禁用横向滚动 */
  transition: min-height 0.3s ease-in-out;
}
textarea:focus {
  box-shadow: none; 
  border: none; 
}
.text-collapsed {
  height: 6em;  /* 约 3 行的高度 */
  /* overflow: hidden; */
}

.text-expanded {
  min-height: 150px;  /* 展开后设置最小高度 */
  height: auto; /* 自动适应内容的高度 */
}



.action-buttons {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #ccc;
}
button{
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
}
button:focus{
  outline: none;
  box-shadow: none;
}

.copy-btn {
  position: relative;
  cursor: pointer;
}
.download-btn {
  position: relative;
  cursor: pointer;
}
.expand-btn {
  position: relative;
  cursor: pointer;
}
.close-btn {
  position: relative;
  cursor: pointer;
}
.tooltip {
  position: absolute;
  top: -25px;
  left: 50%;
  transform: translateX(-50%);
  background-color: black;
  color: white;
  padding: 5px 8px;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
}

::-webkit-scrollbar{
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-thumb {
  background-color: #c4c4c4;
  border-radius: 4px;
}
::-webkit-scrollbar-track {
  background: #f0f0f0;
  border-radius: 4px;
}



/* .footer {
  margin-top: 10px;
  margin-bottom: 10px;
  font-size: 14px;
  color: #888;
  text-align: center;

} */
</style>