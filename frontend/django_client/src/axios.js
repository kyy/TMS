import axios from "axios";


const apiClient = axios.create({
    baseURL: process.env.VUE_APP_API_URL,
    withCredentials: true,
    withXSRFToken: true,
    xsrfCookieName: "csrftoken",
    xsrfHeaderName: "X-CSRFToken",
});

export default apiClient;