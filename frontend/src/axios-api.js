import axios from 'axios'

const axiosInst = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    timeout: 100000
})

export { axiosInst }