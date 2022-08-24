const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true, // 默认情况下 babel-loader 会忽略所有 node_modules 中的文件。如果你想要通过 Babel 显式转译一个依赖，可以在这个选项中列出来。
  assetsDir: 'static', // 放置静态目录 当使用命令npm run build打包项目时，不设置该属性，否则vue包复制到django运行后报找不到js和css文件路径  
})
