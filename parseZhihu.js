// 解析回答
function parseAnswer() {
    var ansDiv = document.querySelectorAll('#Profile-answers > div')[1];
    var titles = ansDiv.querySelectorAll('h2.ContentItem-title');
    for (let i = titles.length - 1; i >= 0; i--) {
        let aTag = titles[i].querySelector('a');
        let href = aTag.getAttribute('href');
        let text = aTag.innerText;
        href = href.replace('//', 'https://');

        console.log(`[${text}](${href})`);
    }
}

// 解析文章
function parsePost() {
    var postDiv = document.querySelectorAll('#Profile-posts > div')[1];
    var titles = postDiv.querySelectorAll('h2.ContentItem-title');
    for (let i = titles.length - 1; i >= 0; i--) {
        let aTag = titles[i].querySelector('a');
        let href = aTag.getAttribute('href');
        let text = aTag.innerText;
        href = href.replace('//', 'https://');

        console.log(`[${text}](${href})`);
    }
}

// 解析想法
function parseIdea() {
    var ideaDiv = document.querySelectorAll('#Profile-posts > div')[1];
    var items = ideaDiv.querySelectorAll('.List-item');
    for (let i = items.length - 1; i >= 0; i--) {
        let span = items[i].querySelector('div.RichContent-inner > span');
        let text = span.innerText;
        let href = items[i].querySelector('div.ContentItem-time > a').getAttribute('href');
        href = href.replace('//', 'https://');
        let time = items[i].querySelector('div.ContentItem-time > a > span').innerText;
        time = time.split(' ')[1]
        console.log(`${time} - ${text} [link](${href})`);
    }
}

// 解析提问
function parseAsk() {
    var askDiv = document.querySelectorAll('#Profile-asks > div')[1];
    var asks = askDiv.querySelectorAll('h2.ContentItem-title');
    for (let i = asks.length - 1; i >= 0; i--) {
        let aTag = asks[i].querySelector('a');
        let href = aTag.getAttribute('href');
        let text = aTag.innerText;
        href = href.replace('//', 'https://');

        console.log(`[${text}](${href})`);
    }
}

// 解析收藏夹
function parseCollection() {
    var collDivs = document.querySelectorAll('div.SelfCollectionItem');
    for (let i = collDivs.length - 1; i >= 0; i--) {
        let aTag = collDivs[i].querySelector('div > a');
        let href = aTag.getAttribute('href');
        let text = aTag.innerText;
        href = 'https://www.zhihu.com' + href

        console.log(`[${text}](${href})`);
    }
}
