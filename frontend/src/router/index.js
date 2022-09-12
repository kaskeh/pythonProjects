import { createRouter, createWebHistory } from "vue-router";
// 小说站点页面
import HomeView from "../views/HomeView.vue";
import CateView from "../views/CateView.vue";
// 用户相关页面
import userHome from "../views/userViews/homeView.vue";
import loginView from "../views/userViews/loginView.vue";
import registerView from "../views/userViews/registerView.vue";

const routes = [
  {
    path: "/",
    name: "sitehome",
    component: HomeView,
  },
  {
    path: "/:cate_id",
    name: "Cate",
    component: CateView,
  },
  {
    path: "/userHome",
    name: "userHome",
    component: userHome,
  },
  {
    path: "/login",
    name: "login",
    component: loginView,
  },
  {
    path: "/register",
    name: "register",
    component: registerView,
  },
  // {
  //   path: "/about",
  //   name: "about",
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () =>
  //     import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  // },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
