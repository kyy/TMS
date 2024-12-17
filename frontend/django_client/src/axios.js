import axios from "axios";


const apiClient = axios.create({
    baseURL: process.env.VUE_APP_API_URL,
    withCredentials: true,
    xsrfCookieName: "csrftoken",
    xsrfHeaderName: "X-CSRFToken",
});

apiClient.defaults.headers['X-CSRFToken'] = await getCSRFToken()


export async function getCSRFToken() {
    /*
    We get the CSRF token from the cookie to include in our requests.
    This is necessary for CSRF protection in Django.
     */

    await  axios.get('http://localhost:8000/api/user/csrf/')

    const name = 'csrftoken';
    let cookieValue = null;


    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    if (cookieValue === null) {
        throw 'Missing CSRF cookie.'
    }
    console.log('+csrftoken')
    return cookieValue;
}

export default apiClient;