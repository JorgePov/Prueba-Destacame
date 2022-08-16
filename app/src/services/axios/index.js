import axios from "axios";
import router from "@/router"

const Axios = axios.create({
  baseURL: "http://localhost:8000",
});

Axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token") || null;
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  }
);

Axios.interceptors.response.use(
  (config) => {
    return config;
  },

  (error) => {

    switch (error.response.status) {
      case 401: 
        console.error(error.response.status, error.message);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        if(router.history.current.path != "/login") {
          router.push("/login")
        }
        return Promise.reject(error);
      
      case 500: 
        const token = localStorage.getItem("token") || null;
        if (!token) {
          router.push("/login")
        }
        console.error(error.response.status, error.message);
        return Promise.reject(error);
  
    default:
      console.error(error.response.status, error.message);
    }
    return Promise.reject(error);
  }
);

export default Axios;
