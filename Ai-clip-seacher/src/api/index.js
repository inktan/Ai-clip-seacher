import request from "./request"
import axios from "axios"

// 获取灵感照片
export async function getRandomImages(query_count) {
    return await request.get(`http://10.1.12.30:5000/random_image`, {
        // get请求参数
        params: {
            query_count,
        }
    });
}

// 语义搜索图片
export async function postBestImagesPrompt(data01) {
    const url = 'http://10.1.12.30:5000/get_best_images_prompt'
    return await request.post(url, data01);
}

// 项目详情
export async function getProjectContent(projectPath) {
    const url = 'http://10.1.12.30:5000/project_content'
    return await request.get(url, {
        // get请求参数
        params: {
            project_path: projectPath,
        }
    });
}

