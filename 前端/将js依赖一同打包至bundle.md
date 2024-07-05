> 

# 将js依赖一同打包至bundle

背景是这样的, 需要给某个软件写 js 插件, 插件是单文件嘛, 如果要引用第三方包的话, 只能使用 AMD 的方式加载, 要么走 cdn, 要么把依赖一起打包进 bundle, 鉴于免费的 cdn 越来越不稳定, 还是一起打包靠谱一些.

打包使用 rollup 插件 [rollup-plugin-copy](https://github.com/vladshcherbin/rollup-plugin-copy.git)

```bash
yarn add rollup-plugin-copy -D
```

顾名思义, 插件会将配置的目标文件在打包时复制到 dist.

配置例子: 

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import copy from 'rollup-plugin-copy'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), copy({
    targets: [
      { src: 'node_modules/monaco-vim/dist/monaco-vim.js', dest: 'dist' },
    ],
  })],
  ...
})

```
