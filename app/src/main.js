import Vue from "vue";
import App from "./App.vue";
import {
  BootstrapVue,
  IconsPlugin,
  InputGroupPlugin,
  FormInputPlugin,
  DropdownPlugin,
  ButtonPlugin,
  CardPlugin,
  SidebarPlugin,
  AvatarPlugin,
  AlertPlugin,
  PopoverPlugin,
  ModalPlugin
} from "bootstrap-vue";
import router from "./router";
import store from "./store";
import Axios from "@/services/axios";

import "@/filters"

import "@/assets/css/main.scss";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.prototype.$axios = Axios;
Vue.config.productionTip = false;

Vue.use(BootstrapVue);
Vue.use(IconsPlugin)
Vue.use(InputGroupPlugin)
Vue.use(FormInputPlugin)
Vue.use(DropdownPlugin)
Vue.use(ButtonPlugin)
Vue.use(CardPlugin)
Vue.use(SidebarPlugin)
Vue.use(AvatarPlugin)
Vue.use(AlertPlugin)
Vue.use(PopoverPlugin)
Vue.use(ModalPlugin)

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
