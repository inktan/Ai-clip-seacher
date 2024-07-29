import getComponentRootDom from './getComponentRootDom'
import styles from "./showMessage.module.less"

/**
 * 
 * @param {String} content 消息内容 
 * @param {String} type 消息类型 info error success warn
 * @param {Number} duration 多久后消失,0为不消失
 * @param {HTMLElement} container 容器，消息会显示到该容器的正中；如果不传，则显示到页面正中
 */
export default function (options = {}) {

    const content = options.content || "";
    const type = options.type || "info";
    const duration = options.duration || 2000;
    let container = options.container || document.body;

    // 创建消息元素
    const div = document.createElement('div');
    const iconDom = getComponentRootDom(Icon, { iconType: 'weixin', size: 32 });

    div.innerHTML = `<span class="${styles.icon}">${iconDom.outerHTML}</span><div>${content}</div>`
    // 设置样式

    const typeClassName = styles[`message-${type}`]

    div.className = `${styles.message} ${typeClassName}`
    // console.log(styles)
    if (!container) {
        container = document.body;
    }
    else {
        if (getComputedStyle(container).position === "static") {
            container.style.position = "relative"
        }
    }
    container.appendChild(div)
    // 浏览器强行渲染
    div.clientHeight;

    // console.log(div)
    // 回归到正常位置
    div.style.opacity = 1;
    div.style.transform = `translate(-50%, -50%)`

    // 等一段时间,消失
    setTimeout(() => {
        div.style.opacity = 0;
        div.style.transform = `translate(-50%, -50%)  translateY(35px )`
        div.addEventListener("transitionend", function () {
            div.remove();
            // 运行回调函数
            options.callback && options.callback();
        }, { once: true })
    }, duration);




}