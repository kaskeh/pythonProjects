<template>
    <div id="bg">
      <div id="container">
        <h1>个人信息</h1>
      <p><span>姓名：</span>{{sname}}</p>
      <p><span>邮箱:</span>{{smail}}</p>
      <p><span>手机号：</span>{{stel}}</p>
      <button @click.prevent="logout">退出</button>
      </div>
    </div>
</template>
//css
<style scoped>
#container{
  width: 480px;
  height: 300px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%,-50%);
  background:#00000090;
  text-align: center;
  border-radius: 20px;
  margin-top: 10px;
  color: white;
}
#bg{
  width: 100%;
    height: 100%;
    /* background: url("../assets/bg2.jpg"); */
    background-color: blueviolet;
    background-size:100% 100%;
    position: fixed;
    top: 0;
    left: 0;
}
p{
  font-size: 20px;
  margin-top: 20px;
  text-align: left;
  margin-left: 32%;
  
}
button{
  position: relative;
  height: 33px;
  width: 150px;
  background: rgba(35, 19, 252, 0.425);
  border-radius: 10px;
  margin-top: 10px;
  box-shadow: none;
  color: white;
  margin-left: 10px;
}