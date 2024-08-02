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
export async function postBestImagesPrompt(query) {
    const url = 'http://10.1.12.30:5000/get_best_images_prompt'
    // console.log(data01)
    return await request.post(url, query);
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

// 语义解析图片
// erroe axios 不支持流式传输
export async function getAIReadImage(imgUrl) {
    const url = 'http://10.1.12.30:5001/ai_image_description'
    return await request.get(url, {
        // get请求参数
        params: {
            img_url: imgUrl,
        }
    });
}

// 请填写您自己的APIKey
const ZhipuAI_api_key = "6afaa8e936bc8982b107416a390216e3.sSW4FmE17ZKIVldh"
const url = 'https://open.bigmodel.cn/api/paas/v4/chat/completions';

// Ai对话
// erroe axios 不支持流式传输
export async function postZhiPuAiChat(messageList) {
    const data = {
        "model": "glm-4",
        "messages": messageList,
        stream: true,
    }
    return await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${ZhipuAI_api_key}`
        },
        body: JSON.stringify(data),
    });
}
