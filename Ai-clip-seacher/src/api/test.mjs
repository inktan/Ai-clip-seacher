import axios from 'axios';
import FormData from 'form-data';
import fs from 'fs';
import path from 'path';

const formData = new FormData();
formData.append('prompt', 'prompt');
formData.append('imageWeight', String(0.35)); // 确保转换为字符串
formData.append('prompt_img', fs.createReadStream('c:/Users/wang.tan/Pictures/qe.png')); // 假设prompt_img是一个File对象
formData.append('n01', String(53)); // 确保转换为字符串
formData.append('n02', String(57)); // 确保转换为字符串

const url = 'http://10.1.12.30:5001/get_best_images_prompt'

// 设置Axios的配置
// const axiosConfig = {
//     headers: {
//         'Content-Type': 'multipart/form-data'
//     }
// };

// 发送POST请求
axios.post(url, 'formData')
    .then(response => {
        console.log('服务器响应:', response.data);
    })
    .catch(error => {
        console.error('请求出错:', error);
    });
