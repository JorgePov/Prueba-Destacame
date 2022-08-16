import Vue from "vue";
import VueRouter from "vue-router";
import store from "@/store"

//pages
import Home from "@/views/Home.vue";
import Login from "@/views/Login.vue";
import Driver from "@/views/driver/Driver.vue";
import Locations from "@/views/seller/Locations.vue";
import Scheduler from "@/views/seller/Scheduler.vue";
import Seller from "@/views/seller/Seller.vue";
import Admin from "@/views/admin/Admin.vue";
import AdminBus from "@/views/admin/AdminBus.vue";
import AdminJourney from "@/views/admin/AdminJourney.vue";
import AdminEmployes from "@/views/admin/AdminEmployes.vue";
//layouts
import GuestLayout from "@/layouts/GuestLayout";
import AuthLayout from "@/layouts/AuthLayout";

Vue.use(VueRouter);

const routes = [
  {
    path: "",
    redirect: "home",
    component: GuestLayout,
    children: [
      {
        path: "/home",
        name: "home",
        component: Home,
        meta: {
          requiresAuth: false,
        },
      },
    ],
  },
  {
    path: "/",
    redirect: "home",
    component: AuthLayout,
    children: [
      {
        path: "/driver",
        name: "driver",
        component: Driver,
        meta: {
          requiresAuth: true,
          rolAuth: "driver",
        },
      },
      {
        path: "/seller",
        name: "seller",
        component: Seller,
        meta: {
          requiresAuth: true,
          rolAuth: "seller",
        },
      },
      {
        path: "/seller/locations",
        name: "seller-locations",
        component: Locations,
        meta: {
          requiresAuth: true,
          rolAuth: "seller",
          processSeller: "locations"
        },
      },
      {
        path: "/seller/schedulers",
        name: "seller-schedulers",
        component: Scheduler,
        meta: {
          requiresAuth: true,
          rolAuth: "seller",
          processSeller: "schedulers"
        },
      },
      {
        path: "/admin",
        name: "admin",
        component: Admin,
        meta: {
          requiresAuth: true,
          rolAuth: "admin",
        },
      },
      {
        path: "/admin/buses",
        name: "admin-buses",
        component: AdminBus,
        meta: {
          requiresAuth: true,
          rolAuth: "admin",
        },
      },
      {
        path: "/admin/journeys",
        name: "admin-journeys",
        component: AdminJourney,
        meta: {
          requiresAuth: true,
          rolAuth: "admin",
        },
      },
      {
        path: "/admin/employes",
        name: "admin-employes",
        component: AdminEmployes,
        meta: {
          requiresAuth: true,
          rolAuth: "admin",
        },
      },
    ],
  },
  {
    path: "/login",
    name: "login",
    component: Login,
    meta: {
      requiresAuth: false,
    },
  },
  /* {
    path: "/about",
    name: "about",
    component: () =>
      import("../views/AboutView.vue"),
  }, */
];

const router = new VueRouter({
  routes,
  linkActiveClass: 'active'
});

router.afterEach(async (to) => {
  if (to.meta.requiresAuth) {
    const isAuthenticated = store.getters.getToken || localStorage.getItem('token')
    if (isAuthenticated) {
      await store.dispatch("setCurrentUser");
    }
  }
});

const pathsValid = {
  driver: { driver: true, login: true  },
  seller: { seller: true, ['seller-schedulers']: true, ['seller-locations']: true, login: true  },
  admin: { admin: true, ['admin-buses']: true, ['admin-journeys']: true, ['admin-employes']: true,login: true },
};

router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    let isAuthenticated = store.getters.getToken || localStorage.getItem('token')
    if (!isAuthenticated) {
      return next({ path: "/login" });
    }
    if (to.meta.rolAuth == localStorage.getItem('rol')) {
      if (pathsValid[to.meta.rolAuth][to.name]) {
        if (to.meta.processSeller) {
          if(to.meta.processSeller == store.getters['aux/getProcessSeller']){

            next();
          }else{
            next({ path: "/seller" })

          }
        }
        next()
      } else {
        return next(false);
      }
    } else {
      next(false);
    }
    
  }else {
    next();
  }
});

export default router;
