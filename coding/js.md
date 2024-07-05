# js

### 滚动加载
```vue
<template>
  <div class="list-container" @scroll="onScroll">
    <ul>
      <li v-for="item in data" :key="item">
        <p>{{ item }}</p>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';

const data = ref<Array<string>>([]);
const pagination = reactive({
  page: 1,
  size: 20,
});

const isLoading = ref(false);
const isEnd = ref(false);

const getData = async () => {
  isLoading.value = true;
  const offset = (pagination.page - 1) * pagination.size;
  for (let i = 0; i < pagination.size; i++) {
    data.value.push(`Content ${offset + i}`);
  }
  if (pagination.page === 6) {
    isEnd.value = true;
  }
  isLoading.value = false;
};

const onScroll = async (event: any) => {
  const bottom = event.target.scrollHeight - event.target.scrollTop - event.target.clientHeight;
  if (!isLoading.value && !isEnd.value && bottom < 100) {
    pagination.page += 1;
    getData();
  }
};

onMounted(async () => {
  await getData();
});

</script>

<style scoped lang="scss">
ul {
  list-style: none;
}
.list-container {
  overflow-y: scroll;
  height: 100%;
}
</style>
```
