/**
 * 
 * @param {*} width 图片瀑布流的列宽
 * @param {*} gapWidth 图片之间的间隙
 * @param {*} id 图片瀑布流所在div容器
 */
// export default function (width, gapWidth, id) {
//     let divContainer = document.getElementById(id);
//     var parentRect = divContainer.getBoundingClientRect();
//     var containerWidth = divContainer.offsetWidth;

//     var cols = Math.floor(containerWidth / (width + gapWidth));
//     var leftSpace = (containerWidth - cols * (width + gapWidth)) * 0.5;

//     var arr = new Array(cols);
//     arr.fill(0);

//     console.log(divContainer.children.length)

//     for (var i = 0; i < divContainer.children.length; i++) {
//         var imgDiv = divContainer.children[i];
//         var minTop = Math.min(...arr);
//         var index = arr.indexOf(minTop);
//         arr[index] += imgDiv.offsetHeight + gapWidth;

//         var left = leftSpace + index * gapWidth + index * width;

//         var childRect = imgDiv.getBoundingClientRect();
//         var relativePosition = {
//             top: childRect.top - parentRect.top,
//             right: parentRect.right - childRect.right,
//             bottom: parentRect.bottom - childRect.bottom,
//             left: childRect.left - parentRect.left
//         };

//         var moveLeft = left - relativePosition.left;
//         var moveTop = minTop - relativePosition.top;

//         imgDiv.style.transform = `translate(${moveLeft}px, ${moveTop}px)`;
//     }
// }
/**
 * 
 * @param {*} width 图片瀑布流的列宽
 * @param {*} gapWidth 图片之间的间隙
 * @param {*} id 图片瀑布流所在div容器
 */
export default function (width, gapWidth, id) {
    let divContainer = document.getElementById(id);
    var parentRect = divContainer.getBoundingClientRect();
    var containerWidth = divContainer.offsetWidth;

    var cols = Math.floor(containerWidth / (width + gapWidth));
    var leftSpace = (containerWidth - cols * (width + gapWidth)) * 0.5;

    var arr = new Array(cols);
    arr.fill(0);

    for (var i = 0; i < divContainer.children.length; i++) {
        var imgDiv = divContainer.children[i];
        var minTop = Math.min(...arr);
        var index = arr.indexOf(minTop);
        arr[index] += imgDiv.offsetHeight + gapWidth;
        var left = leftSpace + index * gapWidth + index * width;

        imgDiv.style.top = minTop + 'px';
        imgDiv.style.left = left + 'px';
        imgDiv.style.position = 'absolute';
    }
    divContainer.style.height = Math.max(...arr) + 'px';
}